from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Group, Membership
# Create your views here.
def group_view (request):
    if request.method == 'POST':
        return create_group(request)
    elif request.method == 'GET':
        return get_groups(request)
    elif request.method == 'PUT':
        return update_group(request)
    else :
        return JsonResponse({"error": "Method not allowed"}, status=405)

    
def create_group(request):
    try:
        data = json.loads(request.body)
        if('created_by' not in data or 'name' not in data):
            return JsonResponse({"error": "Missing required fields"}, status=400)
        if(Group.objects.filter(name=data['name']).exists()):
            return JsonResponse({"error": "Group with this name already exists"}, status=400)
        if(User.objects.filter(id=data['created_by']).exists() == False):
            return JsonResponse({"error": "User does not exist"}, status=400)   
        group = Group.objects.create(
            name=data['name'],
            description=data.get('description', ''),
            created_by=data['created_by']
        )
        return JsonResponse({"message": "Group created successfully", "group": group}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

def get_groups(request):
    groups = Group.objects.all().values('id', 'name', 'description', 'created_by__username', 'created_at', 'updated_at')
    return JsonResponse(list(groups), safe=False, status=200)