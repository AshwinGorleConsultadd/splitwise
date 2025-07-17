from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Group, Membership
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .utils import serialize_group
# Create your views here.
@csrf_exempt
def groups_view (request):
    if request.method == 'POST':
        return create_group(request)
    elif request.method == 'GET':
        return get_groups(request)
    elif request.method == 'PUT':
        return update_group(request)
    else :
        return JsonResponse({"error": "Method not allowed"}, status=405)
@csrf_exempt
def group_view(request, group_id):
    if request.method == 'GET':
        return group_detail_view(request, group_id)
    elif request.method == 'DELETE':
        return delete_group(request, group_id)
    elif request.method == 'PUT':
        return update_group(request, group_id)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

def group_detail_view(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        if(not group):
            return JsonResponse({"error": "Group not found"}, status=404)
        return JsonResponse(serialize_group(group), status=200)
    except Group.DoesNotExist:
        return JsonResponse({"error": "Group not found"}, status=404)
    

def update_group(request, group_id=None):
    try:
        data = json.loads(request.body)
        if not group_id:
            return JsonResponse({"error": "Group ID is required"}, status=400)
        
        group = Group.objects.filter(id=group_id).first()
        if not group:
            return JsonResponse({"error": "Group not found"}, status=404)

        if 'name' in data:
            group.name = data['name']
        if 'description' in data:
            group.description = data['description']
        group.save()

        return JsonResponse({"message": "Group updated successfully", "group": serialize_group(group)}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_groups(request):
    try:
        groups = Group.objects.select_related('created_by').all()
        groups = [serialize_group(group) for group in groups]
        return JsonResponse(list(groups), safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)  
    
def create_group(request):
    try:
        data = json.loads(request.body)
        if('created_by' not in data or 'name' not in data):
            return JsonResponse({"error": "Missing required fields"}, status=400)
        if(Group.objects.filter(name=data['name']).exists()):
            return JsonResponse({"error": "Group with this name already exists"}, status=400)
        if(User.objects.filter(id=data['created_by']).exists() == False):
            return JsonResponse({"error": "User does not exist"}, status=400)  
        print('request.body: '  ,data)
        try:
            user = User.objects.get(id=data['created_by'])
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404) 
        group = Group.objects.create(
            name=data['name'],
            description=data.get('description', ''),
            created_by = user
        )
        return JsonResponse({"message": "Group created successfully", 
            "group": serialize_group(group)}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

def delete_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        if not group:
            return JsonResponse({"error": "Group not found"}, status=404)
        group.delete()
        return JsonResponse({"message": "Group deleted successfully"}, status=204)
    except Group.DoesNotExist:
        return JsonResponse({"error": "Group not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def join_group(request, group_id, user_id):
    try:
        group = Group.objects.get(id=group_id)
        user = User.objects.get(id=user_id)
        if not group or not user:
            return JsonResponse({"message" : "group_id and user_id is required"},status=402)
        membership = Membership.objects.create(group = group, member = user)
        return JsonResponse({
            "message" :  "membership created successfully!",
            "membership" : {
                "member" : user.id,
                "group" : group.id
            }
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)