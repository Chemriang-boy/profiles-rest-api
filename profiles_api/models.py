from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

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
