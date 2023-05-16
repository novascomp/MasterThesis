# https://github.com/okta/samples-python-flask/blob/master/resource-server/helpers.py

import asyncio

from okta_jwt_verifier import AccessTokenVerifier, BaseJWTVerifier

loop = asyncio.get_event_loop()


def is_access_token_valid(token, issuer):
    jwt_verifier = AccessTokenVerifier(issuer=issuer, audience='api://default')
    try:
        loop.run_until_complete(jwt_verifier.verify(token))
        return True
    except Exception:
        return False


def parse_user_token(token, issuer):
    return BaseJWTVerifier(issuer=issuer, audience='api://default').parse_token(token)[1]
