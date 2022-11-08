from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rooms_crud.functions import functions
import json

def get_users(request):
    data = {
        'description': 'This returns all rooms',
    }
    return JsonResponse(data)

@csrf_exempt
def post_user(request):
    #CHECK IF METHOD IS RIGHT
    if not functions.correct_method("POST", request.method):
        return JsonResponse({
                "description": "invalid method"
            },
        status = 400 )
    #CHECK BODY
    #EXPECTED PARAMS
    body = json.loads(request.body)
    expected_params = ["user_name", "type", "password"]
    user_types = ["client", "business"]
    for param in expected_params:
        if param not in body.keys():
            return JsonResponse({
                    "description": f"{param} required in body"
                },
            status = 400 )
        if param=="type":
            if body["type"] not in user_types:
                return JsonResponse({
                    "description": f"{body['type']} user type not allowed"
                },
                status = 400 )
     

    data = {
        'description': 'This post a room',
        'method': request.method,
        'body': str(request.body)
    }
    return JsonResponse(data)

def patch_user(request):
    data = {
        'description': 'This alters a room info',
    }
    return JsonResponse(data)

def delete_user(request):
    data = {
        'description': 'This deletes a room info',
    }
    return JsonResponse(data)
