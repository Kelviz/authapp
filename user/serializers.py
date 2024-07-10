from rest_framework import serializers
from rest_framework.serializers import Serializer, CharField
from .models import User, Organization

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'email', 'firstName', 'lastName', 'phone', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_user_id(self, value):
        if User.objects.filter(user_id=value).exists():
            raise serializers.ValidationError("User ID already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class LoginSerializer(Serializer):
    email = CharField(required=True)
    password = CharField(required=True)
    

class UserSerializer(serializers.ModelSerializer):
        class Meta:
                model = User
                fields = ('user_id', 'email', 'firstName', 'lastName', 'phone',)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['org_id', 'name', 'description']
        read_only_fields = ['org_id']

    def create(self, validated_data):
        # Create and return the organization instance
        return Organization.objects.create(**validated_data)
    

class AddUserToOrganizationSerializer(serializers.Serializer):
    userId = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')