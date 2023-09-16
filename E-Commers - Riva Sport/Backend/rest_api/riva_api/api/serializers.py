from rest_framework import serializers
from riva_api.models import Category, Seller, Inventory

from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

'''
ketika one mengakses ke many maka harus menggunakan many=True,
ketika many mengakses ke one maka jangan gunakan many=True 

'''

class SellerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ('name','address','email','image', )

class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )

class Inventoryser(serializers.ModelSerializer):
    seller = SellerSerializers(required=False)
    category = serializers.StringRelatedField()
    class Meta:
        model = Inventory
        fields = '__all__'

    def create(self, validated_data):
        created = Inventory.objects.create(
            seller=validated_data['seller'],
            category=validated_data['category'],
            name=validated_data['name'],
            stock=validated_data['stock'],
            price=validated_data['price'],
            description=validated_data['description'],
            image=validated_data['image'],
            )
        created.save()
        return created


class CategorySerializers(serializers.ModelSerializer):
    items = Inventoryser(many=True)
    class Meta:
        model = Category
        fields = ('id','name','items', )

class RegisterAccountSerializers(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all(), message="This username is already exist.")])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password','password2')
    
    def create(self, validated_data):
        with transaction.atomic():
            user_account = User.objects.create(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                username=validated_data['username']
                )
            user_account.set_password(validated_data['password'])
            seller_account = Seller.objects.create(
                username=user_account,
                name=validated_data['first_name']+' '+validated_data['last_name'],
                email=validated_data['email']
            )
            if user_account == None or seller_account == None:
                return transaction.set_rollback(True)
            user_account.save()
            seller_account.save()
            return {
                'first_name': validated_data['first_name'],
                'last_name': validated_data['last_name'],
                'username': validated_data['username'],
                'email': validated_data['email']
            }
        
class AccountSellerSerializers(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    name = serializers.CharField(required=False)
    class Meta:
        model = Seller
        fields = ('username','name','address','email','image', )

    def update(self, validated_data):
        user = self.context['request'].user
        instance = Seller.objects.get(username=user)
        instance.address=validated_data['address']
        instance.email=validated_data['email']
        instance.image=validated_data['image']
        instance.save()
        return instance
        
class UserSellerSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def delete(self):
        user = self.context['request'].user
        if self.context['request'].data['confirm'].lower() == 'yes':
            try:
                User.objects.get(username=user).delete()
                return {
                    'message': 'Success deleted your account'
                }
            except:
                return {
                    'message': 'maybe your account has been deleted, please create a new account frist.'
                }
            

