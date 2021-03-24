from django.urls import path
from . import views

app_name = 'integers'
urlpatterns = [
    path('',views.index,name="index"),
    path('post/set',views.post_set,name="post_set"),
    path('post/session',views.post_session,name="post_session"),
    path('post/operation',views.post_operation,name="post_operation"),
    path('integer-list/',views.integerList,name="integer-list"),
    path('set/<str:set_id>/',views.integerBySet,name="integer_set"),
    path('post_set/',views.post_setV2,name="post_setV2")
]

# GET 
# route to access session: integers/<session_id>
# route to access set: integers/<session_id>/<set_id>
# route to access single number: integers/<session_id>/<set_id>/<index>

# POST
# post new session?
# route to post new set: integers/<set_id>/<x_vals && q_vals>
# route to post operation: integers/<operation_string>

# DELETE
# session



