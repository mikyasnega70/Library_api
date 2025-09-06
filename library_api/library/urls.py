from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, RegisterView, LoginView, checkout_book, return_book, MyBooksView, TransactionListView

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('checkout/<int:book_id>/', checkout_book, name='checkout-book'),
    path('return/<int:book_id>/', return_book, name='return-book'),
    path('mybooks/', MyBooksView.as_view(), name='my-books'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('', include(router.urls)),
]
