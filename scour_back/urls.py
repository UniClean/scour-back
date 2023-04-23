from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Scour API",
        default_version='v1',
        description="Scour API documentation",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/', include('customers.urls')),
    path('api/', include('objects.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('employees.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('equipments.urls')),
    path('api/', include('inventory.urls')),
    path('api/', include('inventory_orders.urls')),
    path('api/', include('salary.urls')),
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui')
]
