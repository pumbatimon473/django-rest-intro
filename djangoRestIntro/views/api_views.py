from rest_framework.views import APIView
from djangoRestIntro.models import User
from djangoRestIntro.serializers import UserSerializer
from rest_framework.views import Response, Request


class UserAPIView(APIView):
    def get(self, request: Request) -> Response:
        queryset = User.objects.all()
        serialized = UserSerializer(queryset, many=True)
        return Response(serialized.data)

    def post(self, request: Request) -> Response:
        print(':: DEBUG :: type(request.data): ' + str(type(request.data)))
        deserialized = UserSerializer(data=request.data)
        if not deserialized.is_valid():
            return Response({'error': deserialized.errors}, status=400)
        deserialized.save()
        return Response(deserialized.data, status=201)