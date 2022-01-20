#自分のプロファイルだけ編集できるように変更する
from rest_framework import permissions

#BasePermissionはDjango rest_frameworkが提供している
class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    #has_object_permission関数によって、True, Falseを返り値出力。
    #Trueなら実行権限が与えらえれ、Falseだと制限される
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        #人のプロファイルを見る”GET”とかなら、Trueを返す
        if request.method in permissions.SAFE_METHODS:
            return True
        #objはObjectの事で、アップデートする対象
        #それが、requestしているuserのIDと一致していたらTrueを返すようにする
        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        #updateはSAFE_METHODSではない
        return obj.user_profile.id == request.user.id
