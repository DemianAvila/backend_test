from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rooms_crud.functions import functions
from .models import Events, Users, Rooms
import json


def get_events(request):
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
            events = []
            for event in Events.objects.all():
                events.append({
                    "id": event.id,
                    "event_name": event.event_name,
                    "room": event.room.id,
                    "starts": event.starts,
                    "ends": event.ends,
                    "event_type": event.event_type
                })
            return JsonResponse({
                "description": "OK",
                "events": events
            })

    if 'id' in request.GET.keys():
        id_ = request.GET["id"]
        events = []
        for user in Events.objects.filter(id=id_):
            events.append({
                "id": event.id,
                "event_name": event.event_name,
                "room": event.room.id,
                "starts": event.starts,
                "ends": event.ends,
                "event_type": event.event_type
            })
        return JsonResponse({
            "description": "OK",
            "events": events,
        })
        
    data = {
        'description': 'Query params not recognized',
    }
    return JsonResponse(data, status=400)

@csrf_exempt
def post_event(request):
    #CHECK IF METHOD IS RIGHT
    if not functions.correct_method("POST", request.method):
        return JsonResponse({
                "description": "invalid method"
            },
        status = 400 )
    #CHECK BODY
    #EXPECTED PARAMS
    body = json.loads(request.body)
    expected_params = ["event_name", "room", "event_type",
                       "starts", "ends", "created_by"]

    for param in expected_params:
        if param not in body.keys():
            return JsonResponse({
                    "description": f"{param} required in body"
                },
            status = 400 )
        if param=="event_type":
            if body["event_type"] not in ["public", "private"]:
                return JsonResponse({
                        "description": 
                            f"{body['event_type']} is not a valid event type"
                    },
                status = 400 )

    #CHECK THE USER WHO CREATES
    user = Users.objects.filter(id=body["created_by"])
    if len(user)==0:
        return JsonResponse({
            "description":  f"User {body['created_by']} doesn't exist"
            },
        status = 400 )
    #IF USER IS NOT BUSINES ERROR
    if user[0].user_type!="busines":
        return JsonResponse({
            "description":  
                f"User {body['created_by']} is now allowed to create events"
            },
        status = 400 )

    #CHECK IF ROOM EXISTS
    room = Rooms.objects.filter(id=body["room"])
    if len(room)==0:
        return JsonResponse({
            "description":  f"Requiered room doesn't exists"
            },
        status = 400 )

    #vALIDATE IF SAME ROOM IS NOT USED BY OTHER EVENT ATH THE SAME TIME SPAN

    del body['created_by']
    body["room"]=room[0]
    
    try:
        created = Events.objects.create(**body)
    except Exception as e:
        return JsonResponse({
                "description": f"could not create record in database",
                "ex": str(e)
            },
        status = 400 )

    body["id"] = created.id
    body["room"] = body["room"].id

    data = {
        'description': "Record successfully inserted",
        'body': body
    }
    return JsonResponse(data)



def patch_event(request):
    data = {
        'description': 'This alters a event info',
    }
    return JsonResponse(data)

def delete_event(request):
    data = {
        'description': 'This deletes a event info',
    }
    return JsonResponse(data)
