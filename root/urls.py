from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import include, path  
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('users.urls')),
    path('', include('main.urls')),
    path('', include('blog.urls')),
    
    path('comment/', include('comment.urls')),

    # path('trending/', views.trending, name='trending'),
    # path('peep/', views.peep, name = 'peep'),
    # path('test/', views.test3, name = 'test'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns