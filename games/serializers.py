from rest_framework import serializers
from .models import Game, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class GameSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Game
        fields = ('id','title','slug','genre','description','release_date','average_rating')


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # ახლა DRF-ს სჭირდება ნამდვილი queryset
        write_only=True,
        required=False
    )

    class Meta:
        model = Review
        fields = ('id','user','user_id','game','title','body','score','created_at','updated_at')
        read_only_fields = ('id','user','created_at','updated_at')

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Score must be between 1 and 10.")
        return value

    def create(self, validated_data):
        # ყოველთვის ვაყენებთ request.user-ს
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
