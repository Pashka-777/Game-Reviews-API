from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


# 🟢 რეგისტრაცია
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


# 🟢 საკუთარი პროფილის ნახვა/განახლება/წაშლა
class MeView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# 🟢 მომხმარებელთა სია (GET)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # ან AllowAny, თუ ყველას შეუძლია ნახვა


# 🟢 პაროლის აღდგენა (recovery)
class RecoveryResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        answer = request.data.get('answer')
        new_password = request.data.get('new_password')

        if not email or not answer or not new_password:
            return Response(
                {"detail": "email, answer and new_password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_recovery_answer(answer):
            return Response({"detail": "Wrong recovery answer"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password reset successful"})
