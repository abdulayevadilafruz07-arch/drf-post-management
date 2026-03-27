from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


# ================== SIGNUP ==================
class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    conf_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'conf_password'
        ]

    def validate(self, data):
        if data['password'] != data['conf_password']:
            raise ValidationError({'message': 'Parollar mos emas'})

        if ' ' in data['password']:
            raise ValidationError({'message': 'Parolda probel bolmasin'})

        return data

    def validate_username(self, username):
        if len(username) < 6:
            raise ValidationError({'message': 'Username kamida 6 ta bolsin'})
        if not username.isalnum():
            raise ValidationError({'message': 'Username faqat harf va raqamdan iborat bolsin'})
        if username[0].isdigit():
            raise ValidationError({'message': 'Username raqam bilan boshlanmasin'})
        return username

    def create(self, validated_data):
        validated_data.pop('conf_password')

        user = User.objects.create_user(**validated_data)
        return user


# ================== PROFILE ==================
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        ]


# ================== UPDATE ==================
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
        ]

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance



# ================== CHANGE PASSWORD ==================
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] == attrs['old_password']:
            raise ValidationError({'message': 'Yangi parol eskisi bilan bir xil bolmasin'})

        if attrs['new_password'] != attrs['confirm_password']:
            raise ValidationError({'message': 'Yangi parollar mos emas'})

        return attrs

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['old_password']):
            raise ValidationError({'message': 'Eski parol notogri'})

        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

