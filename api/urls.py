
from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [

    path('users', UserList.as_view(), name='userList'),
    path('users/<int:id>', UserDetail.as_view(), name='userDetail'),
    path('contacts', ContactList.as_view(), name='contactList'),
    path('contacts/<int:id>', ContactDetail.as_view(), name='contactDetail'),
    path('getToken/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('refreshToken/', TokenRefreshView.as_view(), name="token_refresh"),
    path('verifyToken/', TokenVerifyView.as_view(), name="token_verify"),
    path('send/<str:email>', index, name='send'),
    path('persons', PersonList.as_view(), name="persons"),
    path('person/<int:id>', PersonDetail.as_view(), name="person"),
    path('export_xls/<int:userId>', export_contacts_xls, name='export_contacts_xls'),
    path('export_csv/<int:userId>', export_contacts_csv, name='export_contacts_csv'),

    path('export_xls_selected/<str:ids>', export_contacts_xls_selected, name='export_contacts_xls_selected'),
]