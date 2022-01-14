from django.urls import path, include

from rest_framework.routers import DefaultRouter

from profiles_api import views

router = DefaultRouter()
#router,resister('URLの名前', Viesファイルから読み込み, retrieveに必要な名前)
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')


urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('', include(router.urls))

]
