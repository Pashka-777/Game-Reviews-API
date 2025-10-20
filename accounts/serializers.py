from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)
    recovery_answer = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'password2',
            'first_name', 'last_name', 'bio',
            'profile_image', 'recovery_question', 'recovery_answer'
        )

    def validate_password(self, value):
        """
        ეს მეთოდი ატარებს Django-ს ჩაშენებულ password validator-ებს
        და აბრუნებს მკაფიო ერორ მესიჯებს.
        """
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise ValidationError({'password': list(e.messages)})
        return value

    def validate(self, attrs):
        # პაროლების შესაბამისობის შემოწმება
        if attrs.get('password') != attrs.get('password2'):
            raise ValidationError({"password2": "პაროლები არ ემთხვევა."})

        # (სურვილისამებრ) email lowercase
        if 'email' in attrs:
            attrs['email'] = attrs['email'].lower()

        return attrs

    def create(self, validated_data):
        raw_answer = validated_data.pop('recovery_answer', None)
        validated_data.pop('password2', None)
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
        fields = (
            'id', 'email', 'first_name', 'last_name',
            'bio', 'profile_image', 'is_verified'
        )
        read_only_fields = ('email', 'is_verified')
