from django.urls import path

from . import rooms
from . import users

urlpatterns = [
    path('get_rooms', 
        rooms.get_rooms, 
        name='get_rooms'
    ),
    path('post_room', 
        rooms.post_room, 
        name='post_room'
    ),
    path('patch_room', 
        rooms.patch_room, 
        name='patch_room'
    ),
    path('delete_room', 
        rooms.delete_room, 
        name='delete_room'
    ),
    path('get_users', 
        users.get_users, 
        name='get_users'
    ),
    path('post_user', 
        users.post_user, 
        name='post_user'
    ),
    path('patch_user', 
        users.patch_user, 
        name='patch_user'
    ),
    path('delete_user', 
        users.delete_user, 
        name='delete_user'
    ),

]
