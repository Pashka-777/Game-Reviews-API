from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Custom action: კონკრეტული თამაშის ყველა რევიუ
    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def reviews(self, request, pk=None):
        game = self.get_object()
        serializer = ReviewSerializer(game.reviews.all(), many=True)
        return Response(serializer.data)

    # Custom action: ახალი რევიუ მხოლოდ ავტორიზებული მომხმარებლისთვის
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_review(self, request, pk=None):
        game = self.get_object()
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, game=game)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # როცა Review იქმნება, automatically ვამყარებთ current user-ს
        serializer.save(user=self.request.user)
