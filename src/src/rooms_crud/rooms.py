from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rooms_crud.functions import functions
from .models import Rooms
import json


def get_rooms(request):
    #/?all=true
    #/?id=N
    #CHECK IF METHOD IS RIGHT
    if not functions.correct_method("GET", request.method):
        return JsonResponse({
                "description": "invalid method"
            },
        status = 400 )
    #CHECK PARAMS
    if 'all' in request.GET.keys():
        if request.GET["all"]:
            rooms = []
            for room in Rooms.objects.all():
                rooms.append({
                    "id": room.id,
                    "room_name": room.room_name,
                    "room_capacity": room.room_capacity
                })
            return JsonResponse({
                "description": "OK",
                "rooms": rooms
            })

    if 'id' in request.GET.keys():
        id_ = request.GET["id"]
        rooms = []
        for user in Rooms.objects.filter(id=id_):
            rooms.append({
                "id": room.id,
                "room_name": room.room_name,
                "room_capacity": room.room_capacity
            })
        return JsonResponse({
            "description": "OK",
            "rooms": rooms,
        })
        
    data = {
        'description': 'Query params not recognized',
    }
    return JsonResponse(data, status=400)

@csrf_exempt
def post_room(request):
    #CHECK IF METHOD IS RIGHT
    if not functions.correct_method("POST", request.method):
        return JsonResponse({
                "description": "invalid method"
            },
        status = 400 )
    #CHECK BODY
    #EXPECTED PARAMS
    body = json.loads(request.body)
    expected_params = ["room_name", "room_capacity"]
    for param in expected_params:
        if param not in body.keys():
            return JsonResponse({
                    "description": f"{param} required in body"
                },
            status = 400 )
     
    try:
        created = Rooms.objects.create(**body)
    except Exception as e:
        return JsonResponse({
                "description": f"could not create record in database",
                "ex": str(e)
            },
        status = 400 )

    body["id"] = created.id

    data = {
        'description': "Record successfully inserted",
        'body': body
    }
    return JsonResponse(data)



def patch_room(request):
    data = {
        'description': 'This alters a room info',
    }
    return JsonResponse(data)

def delete_room(request):
    data = {
        'description': 'This deletes a room info',
    }
    return JsonResponse(data)
