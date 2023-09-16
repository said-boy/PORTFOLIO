from rest_framework import generics,permissions
from .serializers import CategorySerializers, Inventoryser, RegisterAccountSerializers, SellerSerializers, AccountSellerSerializers, UserSellerSerializers
from riva_api.models import Category, Inventory, Seller

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from django.shortcuts import get_object_or_404
from rest_framework import status

class Account(generics.ListAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializers
    permission_classes = [permissions.AllowAny]

class AccountUser(generics.ListAPIView):
    queryset = Seller.objects.all()
    serializer_class = AccountSellerSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(username=self.request.user)
    
    def post(self, request):
        if 'image' in request.data and request.data['image'] != '':
            request.data['image'] = request.FILES['image']
            
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.update(validated_data=request.data)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
class DeleteUser(generics.DestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = UserSellerSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(username=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        if 'confirm' not in request.data or request.data['confirm'].lower() != 'yes':
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Please 'confirm' your command"
            })
        serializer = self.serializer_class(data=request.data, context={'request': request})
        instance = serializer.delete()
        return Response(instance)

class RegisterAccountApi(generics.CreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = RegisterAccountSerializers
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if request.data['password'] != request.data['password2']:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={
                "message": "Password fields didn't match."
            })
        if Seller.objects.filter(name=request.data['first_name']+request.data['last_name']).exists():
            return Response(status=status.HTTP_409_CONFLICT, data={
                "message": "Name of account is already exist"
            })
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instanse = self.serializer_class.create(self,request.data)
        return Response(status=status.HTTP_201_CREATED, data={
            "message":"Account added successfully",
            "account": instanse
            })
        

class GetDataApi(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [permissions.AllowAny]

class PostDataInventory(generics.ListCreateAPIView):
    queryset = Inventory.objects.select_related('seller','category').all()
    serializer_class = Inventoryser
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(seller=Seller.objects.get(username=self.request.user))

    def post(self, request, *args, **kwargs):
        seller_username = request.user.username
        seller = get_object_or_404(Seller, username=seller_username)
        request.data['seller'] = seller

        if 'category' not in request.data or request.data['category'] == None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Yo, spill the beans on your item's category."
            })
        category = get_object_or_404(Category, name=request.data['category'])
        request.data['category'] = category

        serializer = self.serializer_class(data=request.data) # input-nested : hilangkan part `data=`
        serializer.is_valid(raise_exception=True)
        self.serializer_class.create(self, request.data)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

class EditDataInventory(generics.RetrieveUpdateAPIView):
    queryset = Inventory.objects.select_related('seller','category').all()
    serializer_class = Inventoryser
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(seller=Seller.objects.get(username=self.request.user))

class DeleteDataInventory(generics.DestroyAPIView):
    queryset = Inventory.objects.select_related('seller','category').all()
    serializer_class = Inventoryser
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(seller=Seller.objects.get(username=self.request.user))
    
    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs)
            return Response({"message":"succes deleted your data"})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                "message":"maybe your data has been deleted, please create a new data frist."
                })

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': user.username,
            'email': user.email,
        })

class LogoutAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            token = Token.objects.get(user=user).delete()
            return Response({
                "message": "Logout Successfully",
            })
        except:
            return Response(status=status.HTTP_408_REQUEST_TIMEOUT, data={
                "message": "Something an error, Please login frist",
            })