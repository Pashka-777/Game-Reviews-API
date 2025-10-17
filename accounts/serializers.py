from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password], min_length=8)
    recovery_answer = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('id','email','password','first_name','last_name','bio','profile_image','recovery_question','recovery_answer')

    def create(self, validated_data):
        raw_answer = validated_data.pop('recovery_answer', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        if raw_answer:
            user.set_recovery_answer(raw_answer)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name','bio','profile_image','is_verified')
        read_only_fields = ('email','is_verified')
