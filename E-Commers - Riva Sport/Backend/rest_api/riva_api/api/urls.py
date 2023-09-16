
from django.urls import path
from . import views

urlpatterns = [
    path("", views.GetDataApi.as_view(), name="get-api"),  
    path("account/", views.Account.as_view(), name="account-api"),  
    path("account/register/", views.RegisterAccountApi.as_view(), name="register-api"),  
    path("account/user/", views.AccountUser.as_view(), name="user-api"),  
    path("account/user/delete/", views.DeleteUser.as_view(), name="delete-user"),  
    path("post/", views.PostDataInventory.as_view(), name="post-api"),    
    path("edit/<int:pk>", views.EditDataInventory.as_view(), name="edit-api"),    
    path("delete/<int:pk>", views.DeleteDataInventory.as_view(), name="delete-api"),    
    path("login/", views.CustomAuthToken.as_view(), name="login-api"),    
    path("logout/", views.LogoutAuthToken.as_view(), name="logout-api"),    
]
