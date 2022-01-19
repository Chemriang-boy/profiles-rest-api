from django.urls import path, include

from rest_framework.routers import DefaultRouter

#APIViewが入っているviews.pyをimport
from profiles_api import views

router = DefaultRouter()
#router,resister('URLの名前', Viewsファイルから読み込み, retrieveに必要な名前)
#ViewSetを使うときのURL
#router.register によって、ViewSetに関係しているURLのリストを生成している
#api/hello-viewset というURLの時に、”views.HelloViewSet”を参照するようにしている
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
#profiles_projectの中にあるurls.pyで、
#path('api/', include('profiles_api.urls')),となっているため、
#URLの頭に頭にapiが付く
router.register('profile', views.UserProfileViewSet)

urlpatterns = [
    #helloApiViewはviews.pyで作ったApiView
    #path("", views.クラス名.as_view())
    #APIViewの時のURL
    path('hello-view/', views.HelloApiView.as_view()),
    #as_viewはそういう決まりだから
    #ログイン用のAPI
    path('login/', views.UserLoginApiView.as_view()),
    #ViewSetの時のURL
    #router.register によって生成されたURLを、includeは取り込んで、URLパターンに反映させる。
    path('', include(router.urls))

]
