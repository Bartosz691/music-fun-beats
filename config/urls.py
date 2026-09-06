from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView

from products.graphql_schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('graphql/',
         csrf_exempt(
             GraphQLView.as_view(schema=schema)
      ),
      name='graphql',
  ),
]