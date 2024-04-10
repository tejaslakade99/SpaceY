from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken import views as auth_views

from . import views

urlpatterns = [
    path('api/v1/products/', views.ProductListView.as_view(), name='product-list'),
    path('api/v1/products/create/', views.ProductCreateView.as_view(), name='create-product'),
    path('api/v1/products/<int:pk>/', views.ProductRetrieveView.as_view(), name='product-detail'),
    path('api/v1/products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('api/v1/products/<int:pk>/delete/', views.ProductDestroyView.as_view(), name='product-delete'),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name= 'api-schema'),
    path('api/v1/schema/docs/', SpectacularSwaggerView().as_view(url_name='api-schema')),
    # AuthToken url
    path('api-token-auth/', auth_views.obtain_auth_token),
    path('api/v1/employees/register/', views.EmployeeRegisterCreateView.as_view(), name='employee-register'),
    path('api/v1/employees/login/', views.EmployeeLoginCreateView.as_view(), name='employee-login'),
    # Add Product to Product Database
    path('api/v1/orders/order-item/', views.OrderCreateView.as_view(), name='order-create'),
]