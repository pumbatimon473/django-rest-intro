from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from djangoRestIntro.models import User, Post
from djangoRestIntro.serializers import UserSerializer


class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id' # default 'pk'
