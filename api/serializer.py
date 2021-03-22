from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'user']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id','firstName', 'lastName', 'email', 'phone', 'city', 'state']