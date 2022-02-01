from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from utility.api_helper import api_response


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        user = authenticate(**attrs)

        if user is None:
            raise InvalidCredentials(
                api_response(InvalidCredentials.status_code, "Invalid Credentials", None, True),
                InvalidCredentials.status_code
            )
        else:
            data = super().validate(attrs)
            self.get_token(self.user)
            access_token = data.pop('access')
            refresh_token = data.pop('refresh')

            data['access_token'] = access_token
            data['refresh_token'] = refresh_token

        return api_response(status.HTTP_200_OK, "Login Successful", data, True)


class InvalidCredentials(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
