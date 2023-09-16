from rest_framework.test import APITestCase,force_authenticate
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

import json
from riva_api.models import Category, Seller, Inventory

from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image

class Test_Resolve(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.credentials_register = {
            'first_name': 'test',
            'last_name': 'testing',
            'username': 'usertest',
            'email': 'test@testing.com',
            'password': 'strongpassword',
            'password2': 'strongpassword',
        }

        Category.objects.create(name='Some category')

        self.credentials_login = {
            'username': 'usertest',
            'password': 'strongpassword',
        }

        self.data_inventory = {
            'category': 'Some category',
            'name': 'test inventory',
            'stock': 10,
            'price': 10000,
            'description': 'Some description',
            'image': self.get_image(),
        }

    def register_user(self):
        """Helper function to register a user"""
        url = reverse('register-api')
        response = self.client.post(url, self.credentials_register)
        return response

    def login_user(self):
        """Helper function to log in a user and obtain a token"""
        url = reverse('login-api')
        response = self.client.post(url, self.credentials_login)
        return response
    
    def authenticated(self):
        """Helper function to authentication"""
        self.register_user()
        user = self.login_user()
        token = json.loads(user.content)['token']
        auth = self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return auth
    
    def get_image(self):
        """Helper function to generate image"""
        bts = BytesIO()
        img = Image.new("RGB", (100,100))
        img.save(bts, 'jpeg')
        image = SimpleUploadedFile("testing.jpg", bts.getvalue())
        return image
    
    def create_inventory(self):
        """Helper function to create inventory item"""
        """ 
        format='' solve "AttributeError: This QueryDict instance is immutable"
        'json' jika hanya ada teks dan 'multipart' jika ada file pada data 
        """
        url = reverse('post-api')
        response = self.client.post(url, self.data_inventory, format='multipart') 
        return response

    def test_get_is_resolve(self):
        url = reverse('get-api')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_all_seller(self):
        url = reverse('account-api')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_register_seller_succesful(self):
        '''
        semua dict response (mengandung) data yang sama dengan request
        response dict in request dict ? :)
        mengguanakan : self.assertDictContainsSubset()
        '''
        response = self.register_user()
        self.assertDictContainsSubset(json.loads(response.content)['account'], self.credentials_register)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        
    def test_register_seller_unsuccesful(self):
        url = reverse('register-api')
        self.credentials_register['password2'] = 'wrongsamepassword'
        response = self.client.post(url, self.credentials_register)
        self.assertEquals(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_login_to_get_token_seller_succesful(self):
        self.register_user()
        response = self.login_user()
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_login_to_get_token_seller_unsuccesful(self):
        response = self.login_user()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_data_current_logged_in_user_succesful(self):
        self.authenticated()
        url = reverse('user-api')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_data_current_logged_in_user_unsuccesful(self):
        url = reverse('user-api')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_current_logged_in_user_succesful(self):
        self.authenticated()
        url = reverse('delete-user')
        response = self.client.delete(url, data={'confirm': 'yes'})
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_delete_current_logged_in_user_unsuccesful_no_confirm(self):
        self.authenticated()
        url = reverse('delete-user')
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Please 'confirm' your command", json.loads(response.content)['message'])

    def test_delete_current_logged_in_user_unsuccesful(self):
        url = reverse('delete-user')
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_successful_data_inventory_creation(self):
        self.authenticated()
        response = self.create_inventory()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_unsuccessful_data_inventory_creation_without_login(self):
        response = self.create_inventory()
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unsuccessful_data_inventory_creation_missing_category(self):
        self.authenticated()
        self.data_inventory.pop('category', None)
        response = self.create_inventory()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Yo, spill the beans on your item's category.", json.loads(response.content)['message'])

    def test_unsuccessful_data_inventory_creation_nof_found_category(self):
        self.authenticated()
        self.data_inventory['category'] = 'Wrong category'
        response = self.create_inventory()
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unsuccessful_data_inventory_creation_required_field_error(self):
        self.authenticated()
        '''
        We didn't fill out all the required info in some fields.
        '''
        self.data_inventory.pop('name', None)
        self.data_inventory.pop('stock', None)
        response = self.create_inventory()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_successful_edit_data_inventory(self):
        self.authenticated()
        self.create_inventory()
        self.data_inventory['name'] = 'inventory (updated)'
        self.data_inventory['image'] = self.get_image()
        url = reverse('edit-api', args=[3])
        response = self.client.patch(url, self.data_inventory, format='multipart')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_unsuccessful_edit_data_inventory_not_found(self):
        self.authenticated()
        self.create_inventory()
        self.data_inventory['name'] = 'inventory (updated)'
        self.data_inventory['image'] = self.get_image()
        url = reverse('edit-api', args=[10])
        response = self.client.patch(url, self.data_inventory, format='multipart')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_unsuccessful_edit_data_inventory_missing_category(self):
        self.authenticated()
        self.create_inventory()
        self.data_inventory['category'] = 'Wrong category'
        self.data_inventory['name'] = 'inventory (updated)'
        self.data_inventory['image'] = self.get_image()
        url = reverse('edit-api', args=[3])
        response = self.client.patch(url, self.data_inventory, format='multipart')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Not found.", json.loads(response.content)['detail'])

    def test_unsuccessful_edit_data_inventory_without_login(self):
        self.create_inventory()
        self.data_inventory['name'] = 'inventory (updated)'
        self.data_inventory['image'] = self.get_image()
        url = reverse('edit-api', args=[3])
        response = self.client.put(url, self.data_inventory, format='multipart')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unsuccessful_edit_data_inventory_required_field_error(self):
        self.authenticated()
        self.create_inventory()
        url = reverse('edit-api', args=[3])
        response = self.client.put(url, self.data_inventory, format='multipart')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_successful_deleted_data_inventory(self):
        self.authenticated()
        self.create_inventory()
        url = reverse('delete-api', args=[2])
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("succes deleted your data", json.loads(response.content)['message'])

    def test_unsuccessful_deleted_data_inventory_not_found(self):
        self.authenticated()
        self.create_inventory()
        url = reverse('delete-api', args=[404])
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("maybe your data has been deleted, please create a new data frist.", json.loads(response.content)['message'])

    def test_unsuccessful_deleted_data_inventory_without_login(self):
        self.create_inventory()
        url = reverse('delete-api', args=[2])
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_successful_logout(self):
        self.register_user()
        self.login_user()
        url = reverse('logout-api')
        response = self.client.post(url, self.credentials_login)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("Logout Successfully", json.loads(response.content)['message'])

    def test_unsuccessful_logout(self):
        self.register_user()
        self.login_user()
        url = reverse('logout-api')
        self.client.post(url, self.credentials_login)
        response = self.client.post(url, self.credentials_login)
        self.assertEquals(response.status_code, status.HTTP_408_REQUEST_TIMEOUT)
        self.assertIn("Something an error, Please login frist", json.loads(response.content)['message'])
