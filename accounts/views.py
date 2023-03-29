from rest_framework import generics
from .models import Account
from .serializers import CreateAccountSerializer
from rest_framework import status
from rest_framework.response import Response
from .serializers import LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class AccountCreateView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = CreateAccountSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validate(request.data)

        token_serializer = TokenObtainPairSerializer(data=request.data)
        token_serializer.is_valid(raise_exception=True)
        tokens = token_serializer.validated_data

        data["tokens"] = tokens
        return Response(data, status=status.HTTP_200_OK)