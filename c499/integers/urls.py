from django.urls import path
from . import views

app_name = 'integers'
urlpatterns = [
    path('set/',views.setAPIv1,name="setAPIv1"),
    path('session/',views.sessionAPIv1,name="sessionAPIv1"),
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



