import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("request body : ", data)
            username = data['username']
            email = data['email']
            
            if not username or not email:
                return JsonResponse({"error" : 'username and email are required'}, status = 400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)
            user = User.objects.create(username=username, email=email)
            user.save()
            return JsonResponse({'message' : 'User registered successfully',
                                 'user' :{
                                     'username': user.username,
                                     'email': user.email,
                                     'id': user.id
                                 }
                                 }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


def get_user(request, user_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=user_id)
            if not user:
                return JsonResponse({"error": "User not found"}, status=404)
            return JsonResponse({
                'username': user.username,
                'email': user.email,
                'id': user.id
            })
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Method not allowed"}, status=405)



def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all().values('id', 'username', 'email')
        return JsonResponse(list(users), safe=False, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)