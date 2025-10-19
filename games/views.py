import logging
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer

# --- LOGGER ---
logger = logging.getLogger(__name__)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        game = serializer.save()
        logger.info(f"🎮 New game created: {game.title} by {self.request.user}")
        return game

    def perform_update(self, serializer):
        game = serializer.save()
        logger.info(f"🛠️ Game updated: {game.title} by {self.request.user}")
        return game

    def perform_destroy(self, instance):
        logger.warning(f"❌ Game deleted: {instance.title} by {self.request.user}")
        instance.delete()

    # Custom action: კონკრეტული თამაშის ყველა რევიუ
    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def reviews(self, request, pk=None):
        game = self.get_object()
        logger.debug(f"📄 Reviews requested for game: {game.title}")
        serializer = ReviewSerializer(game.reviews.all(), many=True)
        return Response(serializer.data)

    # Custom action: ახალი რევიუ მხოლოდ ავტორიზებული მომხმარებლისთვის
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_review(self, request, pk=None):
        game = self.get_object()
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, game=game)
            logger.info(f"💬 New review added for {game.title} by {request.user}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"⚠️ Invalid review submission for {game.title} by {request.user}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user)
        logger.info(f"📝 Review created by {self.request.user} for {review.game}")
        return review

    def perform_update(self, serializer):
        review = serializer.save()
        logger.info(f"✏️ Review updated by {self.request.user} for {review.game}")
        return review

    def perform_destroy(self, instance):
        logger.warning(f"🗑️ Review deleted by {self.request.user} for {instance.game}")
        instance.delete()
