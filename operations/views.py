from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Box
from .serializers import BoxSerializer, BoxSerializerRestricted, StaffSerializer
from decimal import Decimal
from django.http import HttpResponse
from rest_framework.response import Response
from .token_form import TokenObtainForm
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.db.models import Avg
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import PermissionDenied


class Index:
    def get(self, request):
        try:
            instructions = {
                "Add New Box": {
                    "url": "add/",
                    "Authorization": "Token via header(staff-user/super-user)",
                    "post request format": {"length": 1, "breadth": 1, "height": 1},
                },
                "Update Box": {
                    "url": "update/<int:box_id>/",
                    "Authorization": "Token via header(staff-user/super-user)",
                    "update request format": {"length": 1, "breadth": 1},
                    "Note": "You can change anything except for created_by and created_at",
                },
                "Delete Box": {
                    "url": "delete/<int:box_id>/",
                    "Authorization": "Token via header(must be box_creator)",
                },
                "List Boxes": {
                    "url": [
                        "list/",
                        "list/?length-more-than=1",
                        "list/?length-more-than=1&breadth-more-than=40",
                    ],
                    "Authorization": "Token via header(staff)",
                    "filter_by": [
                        "length-more-than",
                        "length-less-than",
                        "breadth-more-than",
                        "breadth-less-than",
                        "height-more-than",
                        "height-less-than",
                        "area-more-than",
                        "area-less-than",
                        "volume-more-than",
                        "volume-less-than",
                        "username",
                        "before-date",
                        "after-date",
                    ],
                    "Note": "Created By and Last Updated Key shall only be available if the requesting user is staff",
                },
                "List My Boxes": {
                    "url": [
                        "list/my/",
                        "list/my/?breadth-more-than=40",
                        "list/my/?length-more-than=1&breadth-more-than=40",
                    ],
                    "Authorization": "Token via header(staff)",
                    "filter_by": [
                        "length-more-than",
                        "length-less-than",
                        "breadth-more-than",
                        "breadth-less-than",
                        "height-more-than",
                        "height-less-than",
                        "area-more-than",
                        "area-less-than",
                        "volume-more-than",
                        "volume-less-than",
                    ],
                },
                "Note": "I have created a README.md file on GitHub that provides instructions on how to test the API using tools, along with screenshot images.",
            }

            return JsonResponse(instructions)

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BoxConditionsMixin:
    A1 = 100
    V1 = 1000
    L1 = 100
    L2 = 50

    def check_conditions(self, user, area, volume):
        try:
            today = datetime.now().date()

            total_boxes_count = Box.objects.all().count()
            avg_area = (
                Box.objects.all().aggregate(avg_area=Avg("area"))["avg_area"] or 0
            )
            # print('*********  ', ((avg_area*total_boxes_count) + area) / (total_boxes_count + 1) , ' - ', total_boxes_count + 1, '  **********')
            if ((avg_area * total_boxes_count) + area) / (
                total_boxes_count + 1
            ) > self.A1:
                raise ValueError("Average area exceeds the limit.")

            user_boxes_count = Box.objects.filter(created_by=user).count()
            user_avg_volume = (
                Box.objects.filter(created_by=user).aggregate(avg_volume=Avg("volume"))[
                    "avg_volume"
                ]
                or 0
            )

            # print(f'************  {((user_avg_volume*user_boxes_count) + volume) / (user_boxes_count + 1)} ***********')
            if ((user_avg_volume * user_boxes_count) + volume) / (
                user_boxes_count + 1
            ) > self.V1:
                raise ValueError("User's average volume exceeds the limit.")

            weekly_count = Box.objects.filter(
                created_at__gte=today - timedelta(days=7)
            ).count()
            # print(f'******* {weekly_count} ******')
            if weekly_count + 1 > self.L1:
                raise ValueError("Weekly box limit exceeded.")

            user_weekly_count = Box.objects.filter(
                created_by=user, created_at__gte=today - timedelta(days=7)
            ).count()
            # print(f'******* {user_weekly_count} ******')
            if user_weekly_count + 1 > self.L2:
                raise ValueError("User's weekly box limit exceeded.")

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return None


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            form = TokenObtainForm(request.data)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]

                response = super().post(request, *args, **kwargs)

                if response.status_code == 200:
                    access_token = response.data.get("access")
                    return Response(f"Access Token : {access_token}", 200)
                else:
                    return HttpResponse("Failed to obtain token. Invalid credentials.")
            else:
                return HttpResponse("Invalid form data.")

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def getUser(request):
    try:
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.split(" ")[1] if "Bearer" in auth_header else None

        if token:
            decoded_token = AccessToken(token)
            user_id = decoded_token.payload["user_id"]

        user = User.objects.get(pk=user_id)

        return user

    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BoxAddApi(BoxConditionsMixin, generics.CreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        try:
            length = self.request.data.get("length")
            breadth = self.request.data.get("breadth")
            height = self.request.data.get("height")

            user = getUser(self.request)
            area = Decimal(length) * Decimal(breadth)
            volume = Decimal(length) * Decimal(height) * Decimal(breadth)
            area = round(area, 3)
            volume = round(volume, 3)

            error_response = self.check_conditions(user, area, volume)
            if error_response:
                return error_response

            serializer.save(area=area, volume=volume, created_by=user)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BoxFilterMixin:
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["length", "breadth", "height", "area", "volume"]

    def apply_filters(self, queryset):
        try:
            filters = {}
            for param, value in self.request.query_params.items():
                if param.endswith("-more-than"):
                    filters[f"{param[:-10]}__gt"] = value
                elif param.endswith("-less-than"):
                    filters[f"{param[:-10]}__lt"] = value
                else:
                    filters[param] = value

            return queryset.filter(**filters)

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BoxUpdateApi(BoxConditionsMixin, generics.UpdateAPIView, BoxFilterMixin):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        length = data.get("length", instance.length)
        breadth = data.get("breadth", instance.breadth)
        height = data.get("height", instance.height)

        area = length * breadth
        volume = length * breadth * height
        area = Decimal(area)
        volume = Decimal(volume)

        data["area"] = area
        data["volume"] = volume

        serializer = self.get_serializer(instance, data=data, partial=True)
        try:
            # serializer.is_valid(raise_exception=True)
            user = getUser(request)
            error_response = self.check_conditions(user, area, volume)
            if error_response:
                return error_response

            serializer.save(created_by=instance.created_by)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class BoxListApi(generics.ListAPIView, BoxFilterMixin):
    queryset = Box.objects.all()

    def get_serializer_class(self):
        try:
            if self.request.user.is_staff:
                return StaffSerializer
            return BoxSerializerRestricted

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        try:
            queryset = super().get_queryset()
            queryset = self.apply_filters(queryset)
            return queryset

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BoxListMyApi(generics.ListAPIView, BoxFilterMixin):
    serializer_class = StaffSerializer

    def get_queryset(self):
        try:
            queryset = Box.objects.filter(created_by=self.request.user)
            queryset = self.apply_filters(queryset)
            return queryset

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BoxDeleteApi(BoxConditionsMixin, generics.DestroyAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        user = getUser(self.request)

        if user != instance.created_by:
            raise PermissionDenied("You do not have permission to delete this box.")

        instance.delete()

    def delete(self, request, *args, **kwargs):
        try:
            print(f"args : {kwargs}")
            return super().delete(request, *args, **kwargs)

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
