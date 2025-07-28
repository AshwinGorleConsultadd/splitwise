
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import validate_expense_request, split_expense
from django.contrib.auth.models import User
from .models import Expense, ExpenseShare, ExpensePayer
from groups.models import Group
from settlements.views import minimize_cashflow
from settlements.views import settle_group_debts
from settlements.views import recalculate_group_debts
from .serializers import serialize_payers, serialize_shares
# Create your views here.
@csrf_exempt
def expenses_view(request):
    if request.method == 'POST':
        return create_expense(request)
    elif request.method == 'GET':
        return get_all_expenses(request)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def expense_view(request, expense_id):
    if request.method == 'GET':
        return get_expense(request, expense_id)
    elif request.method == 'DELETE':
        return delete_expense(request, expense_id)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

def get_expense(request, expense_id):
    try:
        expense = Expense.objects.get(id=expense_id)
        expense_data = {
            'id': expense.id,
            'title': expense.title,
            'amount': str(expense.amount),
            'description': expense.description,
            'created_at': expense.created_at.isoformat(),
            'payers': serialize_payers(expense.payers.all()),
            'shares': serialize_shares(expense.shares.all()),
        }
        return JsonResponse(expense_data, status=200)
    except Expense.DoesNotExist:
        return JsonResponse({"error": "Expense not found"}, status=404)
from django.http import JsonResponse
from .models import Expense

def get_all_expenses(request):
    expenses = Expense.objects.all()
    expense_list = []

    for expense in expenses:
        expense_data = {
            'id': expense.id,
            'title': expense.title,
            'amount': str(expense.amount),
            'description': expense.description,
            'created_at': expense.created_at.isoformat(),
            'payers': serialize_payers(expense.payers.all()),
            'shares': serialize_shares(expense.shares.all()),
        }
        expense_list.append(expense_data)

    return JsonResponse({'expenses': expense_list}, status=200, safe=False)



def create_expense(request):
    try:
        expense = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    #validate request body
    validation_result = validate_expense_request(expense)
    if validation_result != 'pass':
        return JsonResponse({'message' : validation_result})

    #create expense
    print('creating new expense')
    group = Group.objects.get(id=expense['group'])
    new_expense = Expense.objects.create(
        title=expense['title'],
        amount=expense['amount'],
        group=group,
    )

    #create expense shares
    print('creating new expense_share')
    for x in expense['participants']:
        user_id = x['user_id']
        share_amount = x['share_amount']
        user = User.objects.get(id=user_id)
        new_expense_share = ExpenseShare.objects.create(
            user = user,
            expense = new_expense,
            share_amount = share_amount
        )
    
    #create expense payers
    print('creating new expense_payer')
    for x in expense['payers']:
        user_id = x['user_id']
        paid_amount = x['paid_amount']
        user = User.objects.get(id=user_id)
        new_expense_payer = ExpensePayer.objects.create(
            expense = new_expense,
            user = user,
            paid_amount = paid_amount
        )
    recalculate_group_debts(group)
    print('group settlement done')

    return JsonResponse({"message" : "expense created successfully"},status=201)


def delete_expense(request, expense_id):
    if request.method != 'DELETE':
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        print('deleting expense')
        expense = Expense.objects.get(id=expense_id)
        group = expense.group
        expense.delete()
        # group = Group.objects.get(id=6)
        recalculate_group_debts(group)
        return JsonResponse({"message": "Expense deleted and debts updated."}, status=200)
    
    except Expense.DoesNotExist:
        return JsonResponse({"error": "Expense not found."}, status=404)
