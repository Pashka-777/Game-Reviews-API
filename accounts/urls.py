from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.UserListView.as_view(), name='user-list'),            # GET: ყველა მომხმარებელი
    path('register/', views.RegisterView.as_view(), name='register'),    # POST: რეგისტრაცია
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # POST: JWT token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # POST: Token refresh
    path('profile/', views.MeView.as_view(), name='profile'),            # GET/PUT/DELETE: საკუთარი პროფილი
    path('recovery/', views.RecoveryResetView.as_view(), name='recovery'),     # POST: პაროლის აღდგენა
]
