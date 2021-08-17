import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import CustomUser
from account.serializerts import RegisterSerializer, UserLoginSerializer
from account.utils import generate_access_token


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            if new_user:
                access_token = generate_access_token(new_user)
                data = { 'access_token': access_token }
                response = Response(data, status=status.HTTP_201_CREATED)
                response.set_cookie(key='access_token', value=access_token)
                return Response('Successfully registered!', 201)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        email = request.data.get('email', None)
        user_password = request.data.get('password', None)
        if not user_password:
            raise AuthenticationFailed('A user password is needed')
        if not email:
            raise AuthenticationFailed('A user email in needed')

        user_instance = authenticate(email=email, password=user_password)

        if not user_instance:
            raise AuthenticationFailed('User not found')

        if user_instance.is_active:
            user_access_token = generate_access_token(user_instance)
            response = Response()
            response.set_cookie(key='access_token', value=user_access_token)
            response.data = { 'access_token': user_access_token}
            return response
        return Response('Something went wrong')




class UserLogoutViewAPI(APIView):
	authentication_classes = (TokenAuthentication,)

	def get(self, request):
		user_token = request.COOKIES.get('access_token', None)
		if user_token:
			response = Response()
			response.delete_cookie('access_token')
			response.data = {
				'message': 'Logged out successfully.'
			}
			return response
		response = Response()
		response.data = {
			'message': 'User is already logged out.'
		}
		return response



class ActivationView(APIView):

    def get(self, request, email, activation_code):
        user = CustomUser.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response('This user does no exist!', 404)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('MOLODEC!', 200)