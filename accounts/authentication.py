import os
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header or not auth_header.startswith('Bearer '):
            # Если заголовок Authorization отсутствует или не начинается с 'Bearer ',
            # аутентификация не проходит, возвращаем None
            return None

        token = auth_header.split(' ')[1]

        try:
            # Декодируем токен
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            # Токен просрочен
            raise AuthenticationFailed('Токен недействителен или просрочен.')
        except jwt.InvalidTokenError:
            # Токен неправильный
            raise AuthenticationFailed('Токен недействителен.')

        user_id = payload.get('user_id')

        if user_id is None:
            # В токене нет user_id — некорректный токен
            raise AuthenticationFailed('Токен недействителен.')

        try:
            # Находим пользователя в базе
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            # Пользователь не найден или неактивен
            raise AuthenticationFailed('Пользователь не найден или неактивен.')

        return (user, token)

    def authenticate_header(self, request):
        return 'Bearer'