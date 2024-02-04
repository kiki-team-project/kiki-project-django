import re
from rest_framework import status
from rest_framework.response import Response


def validate_password(password):
    """비밀번호 유효성 검사"""
    if len(password) < 6:
        return Response(
            {"error": "비밀번호는 6자리 이상이어야 합니다."}, status=status.HTTP_400_BAD_REQUEST
        )
    return password
