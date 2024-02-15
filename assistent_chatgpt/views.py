from django.http import JsonResponse


def home(request):
    return JsonResponse({
        "status": "success",
        "message": "Welcome to assistent chatgpt",
        "data": {}
    }, status=200)