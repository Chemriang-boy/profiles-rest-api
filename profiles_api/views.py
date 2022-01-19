from rest_framework.views import APIView
from rest_framework.response import Response
#a list of handy HTTP status codes
from rest_framework import status
from rest_framework import viewsets
#TokenAuthenticationは、APIを使用している間、ユーザー自身が権限付与出来るようにする
#仕組みとしては、ユーザーがログインしたら、ランダムトークンが発行されて、それがマッチ
#するか否かで本人確認を行う。
from rest_framework.authentication import TokenAuthentication

#serializerをimport
from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


#APIViewsの良いところは、他のAPIを読み込んだり、ローカルファイルと連携するときに便利


#APIViewはDjango rest_frameworkが提供しているもの
class HelloApiView(APIView):
    """Test API View"""
    #何のデータがいつpost patch, putされたかを知る。APIに対して。
    #selializer_classによって、postが出来るようになる。
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLs',
        ]

        #ResponseはDjango rest_frameworkでは必須
        #Jsonで出力されるので、辞書型かリスト型で書いてあげる
        return Response({'message':'Hello!', 'an_apiview':an_apiview})

    #画面上で入力した値がrequestに代入される
    #post, putなどを、APIViewに追加しているという感覚。
    def post(self, request):
        """Create a hello message with our name"""
        #.serializer_classは、APIViewのもので、serializer_classのものをviewの中に
        #入れるための関数だと定義している。
        #APIにポストリクエストすると、serializer_classに使用する。
        #例）名前を入れてpastする。すると、名前のデータが"serializer"に格納される
        serializer = self.serializer_class(data=request.data)
        #serializers.pyで、nameは10文字以内と規定している。

        #もし上記のserializerがis_validなら、、、
        if serializer.is_valid():
            #get('name')は、serializers.pyで規定した、10文字以下の名前を指す。
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})

        else:
            return Response(
                serializer.errors,
                #４００はAPIに悪いリクエストをしている時のエラーコード
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """Handle updating an object"""
            #HTTP putは、オブジェクト全体のアップデートに利用する。全てを置き換えてしまう。
            #putをするときは特定のPK（プライマリーキー）に対して行う。
            #特定のPKとは、IDがあるものだったり。
        return Response({'method':'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        #一部のみを置き換える点でputと異なる。
        return Response({'method':'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        #オブジェクトの削除を行う
        return Response({'method':"DELETE"})


#ここからはViewSetを使ってHTTPを編集する
#viewsetは単純なcreate, read, update, and deleteをするときに良い。
#早くてシンプルなAPIを使うとき

#viewsetsはDjango rest_frameworkが提供している
class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer

    #VIewSetではactionsを追加していく　⇔　APIView
    #listは表示なのかな？？
    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            'Uses actions(list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message':'Hello!', 'a_viewset':a_viewset})

    def create(self, request):
        """Create a new hello message"""
        #まずは入力されたもの（request）をシリアル化
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    #retrieve関数はViewsetの中のデータから特定のものを取ってくる
    #viewsetの場合は、PUTとかPATCHとかのボタンは、特定のユーザーのページで表れる。
    def retrieve(self, request, pk=None):
        """"Handle getting an object by its ID"""
        return Response({'http_method':'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        #PUTは全体の置き換え
        return Response({' http_method':'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        #patchは一部のアップデート
        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method':'DELETE'})


#modelviewsetはAPIを使ってモデルを管理するためのもの
#ViewSetに似ている
#profile_apiのurls.pyにて、
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    #serializers.pyからクラスをインポート
    serializer_class = serializers.UserProfileSerializer
    #objects = UserProfileManager()
    queryset = models.UserProfile.objects.all()
    #TokenAuthentication, はDjango rest_frameworkが提供している
    authentication_classes = (TokenAuthentication, )
    #UpdateOwnProfile は、permissions.pyで作った、IDが一致しているかの関数
    permission_classes = (permissions.UpdateOwnProfile,)
