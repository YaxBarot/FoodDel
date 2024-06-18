from common.serializers import AuthTokenSerializer


def save_auth_tokens(authentication_tokens):
    auth_token_serializer = AuthTokenSerializer(data=authentication_tokens)
    if auth_token_serializer.is_valid():
        auth_token_serializer.save()
