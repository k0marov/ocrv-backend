from rest_framework.response import Response

def error_response(detail: str, status_code: int):
    return Response({'detail': detail}, status=status_code)