from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.permissions import AllowAny
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=400)
        user = User.objects.create_user(username=username, password=password)
        token = Token.objects.create(user=user)
        return Response({"token": token.key}, status=201)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permission() for permission in self.permission_classes]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        if not book.is_available:
            return Response({'error': 'Book not available'}, status=400)

        book.is_available = False
        book.save()

        transaction = Transaction.objects.create(user=request.user, book=book)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=201)

    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def return_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        transaction = Transaction.objects.filter(user=request.user, book=book, return_date__isnull=True).first()

        if not transaction:
            return Response({'error': 'No active transaction found for this book'}, status=400)

        book.is_available = True
        book.save()

        transaction.return_date = timezone.now()
        transaction.save()

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)

class MyBooksView(ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(transaction__user=self.request.user, transaction__return_date__isnull=True)
    
class TransactionListView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]