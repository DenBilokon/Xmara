from django.urls import path

from .views import home, news_war, news_war_show_one, news_prosport, news_prosport_show_one, war_statistic, when_bored


app_name = "news"

urlpatterns = [
    path('', home, name='home'),
    path('news_war/', news_war, name='news_war'),
    path('news_war/<int:_id>', news_war_show_one, name='news_war_show_one'),
    path('news_prosport/', news_prosport, name='news_prosport'),
    path('news_prosport/<int:_id>', news_prosport_show_one, name='news_prosport_show_one'),
    path('war_statistic/', war_statistic, name='war_statistic'),
    path('bored/', when_bored, name='when_bored'),
<<<<<<< HEAD
]
=======
]

>>>>>>> default
