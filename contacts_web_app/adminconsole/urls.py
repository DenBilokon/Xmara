from django.urls import path


from .views import home, user_data

app_name = "adminconsole"

urlpatterns = [
    path('users/', home, name='home'),
    path('user_data/', user_data, name='user_data'),
    ]
