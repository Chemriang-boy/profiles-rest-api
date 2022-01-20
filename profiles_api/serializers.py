#データの入出力を扱い、モデルへの橋渡しをするクラス
#APIViewでpostやupdateが行われた際に、コンテンツを受け取る役割を果たす。
from rest_framework import serializers

from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """Serializers a name field for testing our APIView"""
    #serializerでインプットを共用するフィールド
    name = serializers.CharField(max_length=10)


#serializerを使って、APIを作成する
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        #passwordだけはWrite onlyにしたい。
        extra_kwargs = {
            'password':{
                'write_only':True,
                #styleを指定して、パスワードをドットか＊に変えてしまう
                'style':{'input_type':'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        #UserProfileManagerの中の、create_userを使用している。
        #例）create_user(self, email, name, password=None):
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        #上で定義した新しいユーザーを表示
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


#
class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializers profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        #idはお新しいobjectが生成されると自動で新しいIDが振られる
        #created_on はobjectが生成された時間
        #ということで、書き換え可能なのは'user_profile', 'status_text'
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        #'user_profile'はread_onlyに変更したい
        extra_kwargs = {'user_profile': {'read_only':True}}
