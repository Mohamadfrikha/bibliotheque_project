from django.urls import path
from . import views
app_name = 'cart'  # namespace
urlpatterns = [
   path('browsing/', views.product_list, name='product_list'),
    path('cart/', views.view_cart, name='view_cart'), # name de l'URL pour les redirections
    path('add/<int:livre_id>/', views.add_to_cart,name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart,name='remove_from_cart'),
    path('addqty/<int:livre_id>/', views.add_qty, name='add_qty'),
    path('subqty/<int:livre_id>/', views.sub_qty, name='sub_qty'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]