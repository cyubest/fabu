from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from .models import Exam, UserInformation
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class ExamSerializers(serializers.ModelSerializer):
    roomName = serializers.CharField(source='rooms.roomName')
    courseName = serializers.CharField(source='course.courseName')

    class Meta:
        model = Exam
        fields = ('id',
                  'date',
                  'time',
                  'seats',
                  'floor',
                  'program',
                  'course',
                  'students',
                  'roomName',
                  'courseName',)


class UserInformationSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        fields = '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'password']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         instance = self.Meta.model(**validated_data)
#         # those two stars are the extended password for the data to be validated
#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#         return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'first_name', 'last_name', 'email')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            if User.objects.filter(username=username).exists():
                print(username, password)
                user = authenticate(request=self.context.get('request'),
                                    username=username, password=password)

            else:
                msg = {'detail': 'username you are trying to login with not exist.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to login with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
