from django.http import JsonResponse

def get_rooms(request):
    data = {
        'description': 'This returns all rooms',
    }
    return JsonResponse(data)

def post_room(request):
    data = {
        'description': 'This post a room',
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
