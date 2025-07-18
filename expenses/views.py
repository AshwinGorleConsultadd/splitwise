
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import validate_expense_request, split_expense
from django.contrib.auth.models import User
from .models import Expense, ExpenseShare, ExpensePayer
from groups.models import Group
from settlements.views import minimize_cashflow
from settlements.views import settle_group_debts
import json

# Create your views here.
@csrf_exempt
def expenses_view(request):
    if request.method == 'POST':
        return create_expense(request)
    elif request.method == 'GET':
        return None
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

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
    gorup = Group.objects.get(id=expense['group'])
    new_expense = Expense.objects.create(
        title=expense['title'],
        amount=expense['amount'],
        group=gorup,
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

    
     # expense = json.loads(request.body)
    #expense = Expense.objects.get(id=7)
    print("expense : ",new_expense)
    # dividing expenses amoung participants along with previous debts
    transactions = split_expense(new_expense)
    #minimizing cash flow
    minimized_transactions = minimize_cashflow(transactions)
    # settling debts in the group
    settle_group_debts(expense=new_expense, minimized_transactions=minimized_transactions)
    print('group settlement done')

    return JsonResponse({"message" : "expense created successfully"},status=201)

    print('request body:', expense)
    return JsonResponse({"message" : "expense created successfully"},status=201)