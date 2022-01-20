from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

# Create your models here.
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        #emailがないユーザーは存在しないので、エラーを返す
        if not email:
            raise ValueError("User must have an email address")
        #emailアドレスが正規表現になるようにする。
        email = self.normalize_email(email)
        #ユーザーモデルを作る
        user = self.model(email=email, name=name)

        #passwordをハッシュして見えないようにする
        user.set_password(password)
        #Djangoでデータを保存する時に使う構文
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        #上で作ったcreate_userを使う
        #self はどんなclassの中にも自動的に入る
        user = self.create_user(email, name, password)
        user.is_superuser = True
        #userprofileクラスにあるやつ
        user.is_staff = True
        user.save(using=self._db)

        return user

#admin.pyの中で読み込まれている
#serializers.pyの中でも使用している
#大文字と小文字をDjango側が勝手に理解して、区切ってくれる。
#profilesと勝手に複数形にしてくれる。
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """"Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email


#/api/feedでfeed itemを見られるようにする
#システム内でユーザーが自分の情報をアップデート出来るようにする
#python manage.py makemigrationsによって、migrationの中に、profilefeeditem.pyが作られる
class ProfileFeedItem(models.Model):
    """Profile status update"""
    #foreign keyを使うことで、モデル同士をつなぐことが出来る。
    #これにより、デフォルトでUSERPROFILEモデルを使って、必要に応じてDjango のデフォルトに
    #戻すことが可能になる。
    user_profile = models.ForeignKey(
        #USERPROFILEモデル
        #settings.pyにて、AUTH_USER_MODEL = 'profiles_api.UserProfile'と定義
        settings.AUTH_USER_MODEL,
        #on_deleteは、参照されたモデル（今回はUSERPROFILEモデル）を削除する
        #models.cascadeは関連するモデルを全て消去
        on_delete=models.CASCADE
    )
    #status_text は、なんのfeed updateをしたのかを表す
    status_text = models.CharField(max_length=255)
    #auto_now_add=True は、新しいfeed itemを作ったときに、自動的にタイムスタンプを発行する
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text
