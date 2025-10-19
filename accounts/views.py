import logging
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer

# --- LOGGER ---
logger = logging.getLogger(__name__)

User = get_user_model()


# 🟢 რეგისტრაცია
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(f"New user registered: {user.email}")
        return user


# 🟢 საკუთარი პროფილის ნახვა/განახლება/წაშლა
class MeView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        logger.debug(f"User profile accessed: {self.request.user.email}")
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f"User profile updated: {self.request.user.email}")

    def perform_destroy(self, instance):
        logger.warning(f"User deleted account: {instance.email}")
        instance.delete()


# 🟢 მომხმარებელთა სია (GET)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # ან AllowAny, თუ ყველას შეუძლია ნახვა

    def list(self, request, *args, **kwargs):
        logger.info(f"User list requested by: {request.user}")
        return super().list(request, *args, **kwargs)


# 🟢 პაროლის აღდგენა (recovery)
class RecoveryResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        answer = request.data.get('answer')
        new_password = request.data.get('new_password')

        if not email or not answer or not new_password:
            logger.warning("Incomplete recovery request received")
            return Response(
                {"detail": "email, answer and new_password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.error(f"Password recovery failed: user not found ({email})")
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_recovery_answer(answer):
            logger.warning(f"Wrong recovery answer for user: {email}")
            return Response({"detail": "Wrong recovery answer"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        logger.info(f"Password successfully reset for user: {email}")
        return Response({"detail": "Password reset successful"})

