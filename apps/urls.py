from django.urls import path

from apps.views import (ProductListCreateAPIView,
                        CategoryListCreateAPIView,
                        RegisterAPIView,
                        LoginAPIView,
                        UserListAPIView,
                        CoffeeAndTeaListCreateAPIView
                        )


from apps.views.order_view import (
                        OrderListCreateAPIView,
                        OrderRetrieveAPIView,
                        OrderDestroyAPIView,
                        OrderItemCreateAPIView,
                        OrderItemRetrieveAPIView,
                        OrderItemUpdateAPIView,
                        OrderItemDestroyAPIView,
                        )




urlpatterns = [
    path('product/', ProductListCreateAPIView.as_view(), name='product'),
    path('category/', CategoryListCreateAPIView.as_view(), name='category'),
    path('coffee/tea/', CoffeeAndTeaListCreateAPIView.as_view(), name='coffee_and_tea'),
    path('user/list/', UserListAPIView.as_view(), name='user-list'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('orders/', OrderListCreateAPIView.as_view()),
    path('orders/<int:order_id>/', OrderRetrieveAPIView.as_view()),
    path('orders/<int:order_id>/delete/', OrderDestroyAPIView.as_view()),
    path('orders/<int:order_id>/items/', OrderItemCreateAPIView.as_view()),
    path('order-items/<int:item_id>/', OrderItemRetrieveAPIView.as_view()),
    path('order-items/<int:item_id>/update/', OrderItemUpdateAPIView.as_view()),
    path('order-items/<int:item_id>/delete/', OrderItemDestroyAPIView.as_view()),

]
