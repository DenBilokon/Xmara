from django.urls import path

from .views import home, news_war, news_war_show_one


app_name = "news"

urlpatterns = [
    path('', home, name='home'),
    path('news_war/', news_war, name='news_war'),
    path('news_war/<int:_id>', news_war_show_one, name='news_war_show_one'),
]