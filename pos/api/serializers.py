from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from pos_app.models import TableUser, TableOrder
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny


class TableUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = TableUser
        fields = ('id', 'username', 'phone_number', 'email', 'password', 'role')

class GetTableOrderSerializers(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = TableOrder
        fields = ['id', 'packages', 'weight', 'price', 'status_order', 'created_on', 'user']

    def get_price(self, obj):
        return obj.get_price()

class TableOrderSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=TableUser.objects.all())
    created_on = serializers.DateTimeField(read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = TableOrder
        fields = ('id', 'packages', 'weight', 'price', 'status_order', 'created_on', 'user')

    def get_price(self, obj):
        return obj.get_price()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableUser
        fields = ('id', 'username', 'phone_number', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash password sebelum menyimpan
        validated_data['password'] = make_password(validated_data['password'])
        return TableUser.objects.create(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = TableUser.objects.get(email=email)
        except TableUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid email or password")

        return {
            'user': user,
            'message': 'Login successful',
        }
