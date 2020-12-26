from django.http.response import JsonResponse
from rest_framework import status


token_dict = {"Token":""}

def login_view_decorator(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            request_token = request.META['HTTP_TOKEN']
        except KeyError:
            return JsonResponse(data={"message": "Not authorizable"}, status=status.HTTP_403_FORBIDDEN)

        if token_dict.get("Token") == request_token:
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse(data={"message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
    return wrapper