from django.urls import include, path, re_path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'files', views.FileViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('process-file/<id>', views.process_file, name='process-file'),
    re_path(r'^celery-progress/', include('celery_progress.urls')),
]
