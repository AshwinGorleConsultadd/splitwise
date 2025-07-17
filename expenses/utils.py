from django.http import JsonResponse
from django.contrib.auth.models import User
from groups.models import Group
def validate_expense_request(expense):
    #validate group
    group = expense.get('group')
    if not group or not Group.objects.filter(id=group).exists():
        return 'group is required and must exist'
    #validate title
    if not expense.get('title'):
        return 'title is required'
    #validate amount
    if not expense.get('amount') or not isinstance(expense['amount'], (int, float)):
        return 'amount is required and must be a number'
    #validate description
    if not expense.get('description'):
        return 'description is required'
    #validate payers
    if(not expense.get('payers') or not expense.get('participants')):
        print('condition meet')
        return  'payers and participants are required'
    #validate existance of payers and participants in db
    print('mooved forward')
    users_id_list = {user['user_id'] for user in expense['payers']} | {user['user_id'] for user in expense['participants']}
    for user_id in users_id_list:
        if User.objects.filter(id=user_id).exists() == False :
            return f'payers or participants with user_id {user_id} not exists!'
    # Validate total amount and paid amount
    total_expense_amount = expense['amount']
    total_paid_amount = sum([payer['paid_amount'] for payer in expense['payers']])
    if total_expense_amount != total_paid_amount:
        return f'Total expense amount ({total_expense_amount}) does not match total paid amount by payers ({total_paid_amount})'
    
    # Validate share amount against total expense amount
    total_shared_amount = sum([user['share_amount'] for user in expense['participants']])
    if total_expense_amount != total_shared_amount:
        return f'Total shared amount ({total_shared_amount}) does not match total paid amount by payers ({total_paid_amount})'
    return 'pass'
    
    #validate participants


#split expense
# def split_expense(expense):
#     group = Group.objects.get(id = expense['group'])
#     memberships = group.membership.all()
#     member_list = sorted([membership.member for membership in memberships],key = lambda user : user.id)
#     index_user_map = {}
#     idx = 0
#     for member in member_list