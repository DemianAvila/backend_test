from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rooms_crud.functions import functions
from .models import Events, Users, Attendances
import json


def get_attendances(request):
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
            attendances = []
            for attendance in Events.objects.all():
                attendances.append({
                    "id": attendance.id,
                    "attendance_name": attendance.attendance_name,
                    "room": attendance.room.id,
                    "starts": attendance.starts,
                    "ends": attendance.ends,
                    "attendance_type": attendance.attendance_type
                })
            return JsonResponse({
                "description": "OK",
                "attendances": attendances
            })

    if 'id' in request.GET.keys():
        id_ = request.GET["id"]
        attendances = []
        for user in Events.objects.filter(id=id_):
            attendances.append({
                "id": attendance.id,
                "attendance_name": attendance.attendance_name,
                "room": attendance.room.id,
                "starts": attendance.starts,
                "ends": attendance.ends,
                "attendance_type": attendance.attendance_type
            })
        return JsonResponse({
            "description": "OK",
            "attendances": attendances,
        })
        
    data = {
        'description': 'Query params not recognized',
    }
    return JsonResponse(data, status=400)

@csrf_exempt
def post_attendance(request):
    #CHECK IF METHOD IS RIGHT
    if not functions.correct_method("POST", request.method):
        return JsonResponse({
                "description": "invalid method"
            },
        status = 400 )
    #CHECK BODY
    #EXPECTED PARAMS
    body = json.loads(request.body)
    expected_params = ["user", "event"]

    for param in expected_params:
        if param not in body.keys():
            return JsonResponse({
                    "description": f"{param} required in body"
                },
            status = 400 )

    #CHECK THE USER WHO CREATES
    user = Users.objects.filter(id=body["user"])
    event = Events.objects.filter(id=body["event"])
    if len(user)==0:
        return JsonResponse({
            "description":  f"User {body['user']} doesn't exist"
            },
        status = 400 )
    if len(event)==0:
        return JsonResponse({
            "description":  f"Event {body['event']} doesn't exist"
            },
        status = 400 )
    #IF USER IS NOT BUSINES ERROR
    if user[0].user_type!="client":
        return JsonResponse({
            "description":  
                f"User {body['user']} is now allowed to book for events"
            },
        status = 400 )
    #IF USER IS ALREADY SIGNED UP
    attendances_user_event = Attendances.objects.filter(
            user=user[0]).filter(
                    event=event[0])
    if len(attendances_user_event)>0:
        return JsonResponse({
            "description":  
                f"User already book for this event"
            },
        status = 400 )

    #SUM AL THE ATTENDANCES AND COMPARE TO THE ROOM LEFT
    #IF FULL REJECT
    attendances_for_event = len(Attendances.objects.filter(event=event[0]))
    capacity = event[0].room.room_capacity
    if attendances_for_event == capacity:
        return JsonResponse({
            "description":  
                f"We are sorry, there is no more room for this event"
            },
        status = 400 )

    #IF EVENT IS PRIVATE DENY
    if event[0].event_type=="private":
        return JsonResponse({
            "description":  
                f"You can not book for this event"
            },
        status = 400 )


    body["user"] = user[0]
    body["event"] = event[0]
    try:
        created = Attendances.objects.create(**body)
    except Exception as e:
        return JsonResponse({
                "description": f"could not create record in database",
                "ex": str(e)
            },
        status = 400 )

    body["id"] = created.id
    body["user"] = body["user"].id
    body["event"] = body["event"].id

    data = {
        'description': "Record successfully inserted",
        'body': body
    }
    return JsonResponse(data)



def patch_attendance(request):
    data = {
        'description': 'This alters a attendance info',
    }
    return JsonResponse(data)


@csrf_exempt
def delete_attendance(request):
    #CHECK IF METHOD IS RIGHT
    if not functions.correct_method("DELETE", request.method):
        return JsonResponse({
                "description": "invalid method"
            },
        status = 400 )
    #CHECK BODY
    #EXPECTED PARAMS
    body = json.loads(request.body)
    expected_params = ["user", "event"]

    for param in expected_params:
        if param not in body.keys():
            return JsonResponse({
                    "description": f"{param} required in body"
                },
            status = 400 )
    
    #CHECK THE USER WHO CREATES
    user = Users.objects.filter(id=body["user"])
    event = Events.objects.filter(id=body["event"])
    if len(user)==0:
        return JsonResponse({
            "description":  f"User {body['user']} doesn't exist"
            },
        status = 400 )
    if len(event)==0:
        return JsonResponse({
            "description":  f"Event {body['event']} doesn't exist"
            },
        status = 400 )

    #CHECK THE ATTENDANCE
    attendance = Attendances.objects.filter(
        user=user[0]
    ).filter(
        event=event[0]
    )

    if len(attendance)==0:
        return JsonResponse({
            "description":  f"That user won't attend that event"
            },
        status = 400 )

    else:
        attendance[0].delete()
        return JsonResponse({
            "description":  f"Successfully deleted your attendance"
            })



