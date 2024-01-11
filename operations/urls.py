from django.urls import path
from .views import (
    BoxAddApi,
    BoxUpdateApi,
    BoxListApi,
    BoxListMyApi,
    BoxDeleteApi,
    CustomTokenObtainPairView,
    Index,
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "operations"

urlpatterns = [
    path("", Index().get, name="root"),
    path("add/", BoxAddApi.as_view(), name="box-add"),
    path("update/<int:pk>/", BoxUpdateApi.as_view(), name="box-update"),
    path("list/", BoxListApi.as_view(), name="box-list"),
    path("list/my/", BoxListMyApi.as_view(), name="box-list-my"),
    path("delete/<int:pk>/", BoxDeleteApi.as_view(), name="box-delete"),
    # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
]
