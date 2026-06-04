# api/authentication.py

# Iako za autentikaciju koristimo Azure, a ne Django (koji nudi nekoliko vlastitih tipova autentikacije),
# uz donju klasu i dalje možemo koristiti primjerice request.user za pristup informacijama o korisniku.

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from jwt import PyJWKClient
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

_jwk_client: PyJWKClient | None = None


def _get_jwk_client() -> PyJWKClient:
    global _jwk_client
    if _jwk_client is None:
        jwks_url = (
            f"https://login.microsoftonline.com/"
            f"{settings.AZURE_AD_TENANT_ID}/discovery/v2.0/keys"
        )
        _jwk_client = PyJWKClient(jwks_url)
    return _jwk_client


class AzureADAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header[7:]
        try:
            signing_key = _get_jwk_client().get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=settings.AZURE_AD_CLIENT_ID,
                issuer=[
                    f"https://login.microsoftonline.com/{settings.AZURE_AD_TENANT_ID}/v2.0",
                    f"https://sts.windows.net/{settings.AZURE_AD_TENANT_ID}/",
                ],
                options={"require": ["exp", "nbf", "iss", "aud", "sub"]},
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError as exc:
            print("Token validation failed:", exc)
            raise AuthenticationFailed(f"Invalid token: {exc}")

        user = self._get_or_create_user(payload)
        return (user, payload)

    @staticmethod
    def _get_or_create_user(payload: dict) -> User:
        sub = payload.get("sub", "")
        if not sub:
            raise AuthenticationFailed("Token missing 'sub' claim.")

        given_name = payload.get("given_name", "")
        family_name = payload.get("family_name", "")
        full_name = payload.get("name", "")

        if given_name or family_name:
            first_name = given_name
            last_name = family_name
        else:
            first_name = full_name
            last_name = ""

        user, created = User.objects.get_or_create(
            username=sub,
            defaults={
                "email": payload.get("preferred_username", ""),
                "first_name": first_name,
                "last_name": last_name,
            },
        )

        if not created:
            # Korisniku u Entra ID može se promijeniti ime ili email; zbog toga po potrebi osvježavamo Django korisnika
            new_email = payload.get("preferred_username", user.email)
            new_first_name = first_name or user.first_name
            new_last_name = last_name or user.last_name
            if (user.email, user.first_name, user.last_name) != (new_email, new_first_name, new_last_name):
                user.email = new_email
                user.first_name = new_first_name
                user.last_name = new_last_name
                user.save(update_fields=["email", "first_name", "last_name"])

        return user
