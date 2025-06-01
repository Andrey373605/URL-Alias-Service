from django.http import HttpResponseGone, HttpResponseNotFound, HttpResponseRedirect
from distutils.util import strtobool

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError as DRFValidationError

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes

from .models import ShortURL
from .serializers import (
    CreateShortURLSerializer,
    ShortURLSerializer,
    ShortURLStatsSerializer,
    DeactivateResponseSerializer
)
from .pagination import CustomPagination

from .services.create_short_url import CreateShortURLService
from .services.deactivate_short_url import DeactivateShortURLService
from .services.redirect_short_url import RedirectShortURLService, GoneException
from .services.agregate_stats import ShortURLStatsService


class BaseAuthView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name='active',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
            )
        ]
    )
)
class ShortURLListCreateView(BaseAuthView, generics.ListCreateAPIView):
    """
    GET /short-urls/ - get a list (with pagination) of all short links.
    POST /short-urls/ - create a new short link.
    """
    queryset = ShortURL.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        return CreateShortURLSerializer if self.request.method == 'POST' else ShortURLSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        active_param = self.request.query_params.get('active')
        if active_param is not None:
            try:
                is_active = bool(strtobool(active_param))
            except:
                return qs # ignore invalid value
            if is_active:
                return qs.active()
            return qs.filter(is_active=False)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        original_url = serializer.validated_data['original_url']
        custom_key = serializer.validated_data.get('custom_key')
        expires_days = serializer.validated_data.get('expires_days')

        try:
            short_url_obj = CreateShortURLService.execute(
                original_url=original_url,
                custom_key=custom_key,
                expires_days=expires_days
            )
        except (ValueError, DRFValidationError) as e:
            raise DRFValidationError(str(e))
        except Exception as e:
            raise DRFValidationError(str(e))

        output_serializer = ShortURLSerializer(short_url_obj, context=self.get_serializer_context())
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ShortURLRetrieveView(BaseAuthView, generics.RetrieveAPIView):
    """
    GET /short-urls/{short_key}/ - return information about a specific short link.
    """
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    lookup_field = 'short_key'


class RedirectView(APIView):
    """
    GET /{short_key}/ - redirect to the original URL.
        If the short link is not found - 404.
        If it is found, but is not active or has expired - 410 Gone.
        Otherwise, register the click and redirect.
    """
    authentication_classes = []
    permission_classes = []

    @extend_schema(exclude=True)
    def get(self, request, short_key):
        try:
            original_url = RedirectShortURLService.execute(short_key)
        except GoneException as e:
            return HttpResponseGone(str(e))
        except NotFound as e:
            return HttpResponseNotFound(str(e))

        return HttpResponseRedirect(original_url)


class DeactivateShortURLView(BaseAuthView):
    """
    PATCH /short-urls/{short_key}/deactivate/ - deactivate short UR:.
    """
    serializer_class = DeactivateResponseSerializer

    @extend_schema(
        request=None,
        responses={200: DeactivateResponseSerializer},
        operation_id="deactivate_short_url"
    )
    def patch(self, request, short_key):
        try:
            DeactivateShortURLService.execute(short_key)
        except DRFValidationError as e:
            raise e
        except Exception as e:
            raise NotFound(str(e))
        # Возвращаем {"status": "deactivated"}
        return Response({"status": "deactivated"}, status=status.HTTP_200_OK)


class ShortURLStatsView(BaseAuthView):
    """
    GET /short-urls/stats/ - get statistics for all short links.
    """
    serializer_class = ShortURLStatsSerializer
    pagination_class = CustomPagination

    @extend_schema(
        responses={200: ShortURLStatsSerializer(many=True)},
        operation_id="shorturl_stats_list"
    )
    def get(self, request, *args, **kwargs):
        data = ShortURLStatsService.list_all_stats()
        serializer = ShortURLStatsSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShortURLStatsDetailView(BaseAuthView):
    """
    GET /short-urls/stats/{short_key}/ - get statistics for certain short URL.
    """
    serializer_class = ShortURLStatsSerializer

    @extend_schema(
        responses={200: ShortURLStatsSerializer},
        operation_id="shorturl_stats_retrieve"
    )
    def get(self, request, short_key, *args, **kwargs):
        try:
            data = ShortURLStatsService.detail_stats(short_key)
        except NotFound as e:
            raise e
        serializer = ShortURLStatsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
