from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('catalog/', Catalog, name = 'catalog'),
    path('get_video/<file_name>', VideoFileView.as_view()),
    path('aboutus', aboutus, name = 'aboutus'),
    path('new_video', NewVideo.as_view(), name = 'new_video'),
    path('new_video', NewVideo.as_view(), name = 'NewYTVideo'),
    path('video/<int:id>/', VideoView2.as_view(), name='video'),
    path('search/', search, name = 'search'),
    path('video/<int:id>/<int:new>/', VideoView2.as_view()),
    # path('test/', updates, name = 'test'),
    # path('getupdates/', updates, name = 'getupdates'),
    # path('watch_history/', watch_history, name = 'watch_history'),
]
