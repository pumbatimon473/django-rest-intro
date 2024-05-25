from rest_framework.views import APIView
from djangoRestIntro.models import User
from djangoRestIntro.serializers import UserSerializer
from rest_framework.views import Response, Request
from djangoRestIntro.utils import log
from django.shortcuts import get_object_or_404
from rest_framework import status


# Reference:
# Class-based Views: https://www.django-rest-framework.org/api-guide/views/#class-based-views
# Status Codes: https://www.django-rest-framework.org/api-guide/status-codes/
class UserAPIView(APIView):
    def get(self, request: Request) -> Response:
        queryset = User.objects.all()
        serialized = UserSerializer(queryset, many=True)    # <class 'rest_framework.serializers.ListSerializer'>
        log('type(serialized):', type(serialized))
        log('type(serialized.data):', type(serialized.data))
        return Response(serialized.data)    # <class 'rest_framework.utils.serializer_helpers.ReturnList'>

    def post(self, request: Request) -> Response:
        log('type(request.data):', type(request.data))  # <class 'dict'>
        deserialized = UserSerializer(data=request.data)
        log('type(deserialized):',  type(deserialized)) # <class 'djangoRestIntro.serializers.UserSerializer'>
        if not deserialized.is_valid():
            return Response({'error': deserialized.errors}, status=400)
        deserialized.save()
        # <class 'rest_framework.utils.serializer_helpers.ReturnDict'>
        log('type(deserialized.data):', type(deserialized.data))
        return Response(deserialized.data, status=201)


class UserGetReplaceUpdateDeleteAPIView(APIView):
    def get(self, request: Request, id: int) -> Response:
        user = get_object_or_404(User, id=id)   # Raises Http404 exception if the object is not found
        serialized = UserSerializer(user)
        log('type(serialized):', type(serialized))
        log('type(serialized.data):', type(serialized.data))
        return Response(serialized.data)

    def put(self, request: Request, id: int) -> Response:
        try:
            user = User.objects.get(id=id)
            log('type(user):', type(user))  # <class 'djangoRestIntro.models.User'>
            user.username = request.data['username']
            user.email = request.data['email']
            user.password = request.data['password']
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            response_status = status.HTTP_200_OK
        except User.DoesNotExist:
            user = User.objects.create(**request.data)
            user.id = id
            response_status = status.HTTP_201_CREATED
        user.save()
        return Response({'id': user.id, 'username': user.username, 'email': user.email, \
                         'first_name': user.first_name, 'last_name': user.last_name}, status=response_status)

    def patch(self, request: Request, id: int) -> Response:
        user = get_object_or_404(User, id=id)
        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)
        user.password = request.data.get('password', user.password)
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.save()
        serialized = UserSerializer(user)
        return Response(serialized.data)

    def delete(self, request: Request, id: int) -> Response:
        user = get_object_or_404(User, id=id)
        user.delete()
        return Response({'message': 'Deleted user with id ' + str(id)})

