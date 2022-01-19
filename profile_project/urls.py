"""profile_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#プロジェクト内にあるurls.pyが全てのURLの入口
#アプリ内に、urls.pyをつくって、それを参照してもよい
from django.contrib import admin
#includeを使うと、プロジェクト内にある他のappsのURLを参照することが出来る
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #api/となっているURLがあったら、profiles_apiのurls.pyを参照する
    path('api/', include('profiles_api.urls')),
]
