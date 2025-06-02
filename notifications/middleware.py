from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from urllib.parse import parse_qs

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token):
    try:
        UntypedToken(token)

        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_data.get('user_id')

        user = User.objects.get(id=user_id)
        return user
    except (InvalidToken, TokenError, User.DoesNotExist):
        return AnonymousUser()


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        token = None

        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        if 'token' in query_params:
            token = query_params['token'][0]

        if not token:
            headers = dict(scope['headers'])
            if b'authorization' in headers:
                auth_header = headers[b'authorization'].decode()
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]

        if token:
            scope['user'] = await get_user_from_token(token)
        else:
            scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(inner)