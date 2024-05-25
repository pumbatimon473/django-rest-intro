from django.http import HttpRequest, HttpResponse
from djangoRestIntro.models import User, Post
import json


# works with all http methods: GET, POST, PUT, PATCH, DELETE
def users_crude(request: HttpRequest) -> HttpResponse:
    all_users = User.objects.all()  # QuerySet: List of all User (object)
    print("type(all_users): " + str(type(all_users)))  # type(all_users): <class 'django.db.models.query.QuerySet'>
    # serializing the object (Converting into string)
    users_dict = [{'username': user.username} for user in all_users]  # still an object
    # NOTE: Object of type QuerySet is not JSON serializable
    return HttpResponse(json.dumps(users_dict))  # HttpResponse accepts str as an input param


# Improvised: v2
def users(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        query_set = User.objects.all()
        serializable = [{'username': user.username, 'email': user.email} for user in query_set]
        return HttpResponse(json.dumps(serializable))

    if request.method == 'POST':
        new_user = json.loads(request.body)  # deserialize str containing a JSON doc into a python obj
        # check if there already exists a user with the given username or email
        if User.objects.filter(username=new_user['username']).first() or User.objects.filter(
                email=new_user['email']).first():
            return HttpResponse(json.dumps({'error': 'Username or email already exists!'}), status=400)
        user = User.objects.create(**new_user)
        user.save()
        return HttpResponse(json.dumps({'id': user.id, 'username': user.username}))


def get_or_replace_or_update_or_delete_user(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == 'GET':
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'User does not exist!'}), status=404)
        return HttpResponse(json.dumps(
            {'id': user.id, 'username': user.username, 'email': user.email, 'first_name': user.first_name,
             'last_name': user.last_name}))

    if request.method == 'PUT':
        user_dict = json.loads(request.body)  # deserialize json str into a python obj
        try:
            user = User.objects.get(id=id)
            user.username = user_dict['username']
            user.email = user_dict['email']
            user.password = user_dict['password']
            user.first_name = user_dict['first_name']
            user.last_name = user_dict['last_name']
        except User.DoesNotExist:
            user = User.objects.create(**user_dict)
            user.id = id
        user.save()
        return HttpResponse(json.dumps(
            {'id': user.id, 'username': user.username, 'email': user.email, 'first_name': user.first_name,
             'last_name': user.last_name}))

    if request.method == 'PATCH':
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'User does not exist!'}), status=404)
        updated_user = json.loads(request.body)
        user.username = updated_user.get('username', user.username)
        user.email = updated_user.get('email', user.email)
        user.password = updated_user.get('password', user.password)
        user.first_name = updated_user.get('first_name', user.first_name)
        user.last_name = updated_user.get('last_name', user.last_name)
        user.save()
        return HttpResponse(json.dumps(
            {'id': user.id, 'username': user.username, 'email': user.email, 'first_name': user.first_name,
             'last_name': user.last_name}))

    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=id)
            user.delete()
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'User does not exist!'}), status=404)
        return HttpResponse(json.dumps({'message': 'Deleted user with id ' + str(id)}))
