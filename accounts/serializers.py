from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account
from employees.models import Employee
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class CreateAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Account
        fields = ('user', 'employee_id', 'phone_number')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        account = Account.objects.create(user=user, **validated_data)
        return account


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise AuthenticationFailed('Invalid credentials, try again')
        else:
            raise AuthenticationFailed('Please provide username and password both')
        # tokens = user.tokens()
        account = Account.objects.get(user=user)
        return {
            'account_id': account.id,
            'username': account.user.username,
            'email': account.user.email,
            'first_name': account.user.first_name,
            'last_name': account.user.last_name,
            # 'tokens': tokens
        }