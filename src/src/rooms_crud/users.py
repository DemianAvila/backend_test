from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rooms_crud.functions import functions
from .models import Users
import json

def get_users(request):
    #/?all=true
    #/?id=N
    #/?user_type=xxx
    #CHECK IF METHOD IS RIGHT
    if not functions.correct_method("GET", request.method):
        return JsonResponse({
                "description": "invalid method"
            },
        status = 400 )
    #CHECK PARAMS
    if 'all' in request.GET.keys():
        if request.GET["all"]:
            users = []
            for user in Users.objects.all():
                users.append({
                    "id": user.id,
                    "user_type": user.user_type,
                    "user_name": user.user_name
                })
            return JsonResponse({
                "description": "OK",
                "users": users
            })

    if 'id' in request.GET.keys():
        id_ = request.GET["id"]
        users = []
        for user in Users.objects.filter(id=id_):
            users.append({
                "id": user.id,
                "user_type": user.user_type,
                "user_name": user.user_name
            })
        return JsonResponse({
            "description": "OK",
            "users": users,
        })
        
    if 'user_type' in request.GET.keys():
        user_type = request.GET["user_type"]
        users = []
        for user in Users.objects.filter(user_type=user_type):
            users.append({
                "id": user.id,
                "user_type": user.user_type,
                "user_name": user.user_name
            })
        return JsonResponse({
            "description": "OK",
            "users": users,
        })

    data = {
        'description': 'Query params not recognized',
    }
    return JsonResponse(data, status=400)

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
    expected_params = ["user_name", "user_type", "password"]
    user_types = ["client", "business"]
    for param in expected_params:
        if param not in body.keys():
            return JsonResponse({
                    "description": f"{param} required in body"
                },
            status = 400 )
        if param=="type":
            if body["user_type"] not in user_types:
                return JsonResponse({
                        "description": f"{body['user_type']} user type not allowed"
                    },
                status = 400 )
     
    try:
        created = Users.objects.create(**body)
    except Exception as e:
        return JsonResponse({
                "description": f"could not create record in database",
                "ex": str(e)
            },
        status = 400 )

    del body["password"]
    body["id"] = created.id

    data = {
        'description': "Record successfully inserted",
        'body': body
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
