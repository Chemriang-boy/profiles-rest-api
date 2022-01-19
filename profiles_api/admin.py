from django.contrib import admin

#modelを読み込めるようにする
from profiles_api import models

# Register your models here.
#アドミン画面に反映させる処理
#User profileを追加
admin.site.register(models.UserProfile)
