# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework import serializers
# Imports from your apps
from .models import Customer


class SignupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('code', 'nickName', 'avatarUrl', 'city', 'province', 'country', 'gender', 'language')


class SignupResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'point', 'level', 'balance', 'faceExisted')
        read_only_fields = ('id', 'balance', )


class LoginRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'code')
        read_only_fields = ('id', )


class LoginResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'point', 'level', 'balance')
        read_only_fields = ('id', 'balance',)


class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'point', 'level', 'balance')
        read_only_fields = ('id', 'balance',)


class CustomerPaymentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'point', 'level', 'balance')
        read_only_fields = ('id', 'balance',)


class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class EntranceGetInfoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('code',)


class EntranceGetInfoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'avatarUrl', 'nickName', 'level')
