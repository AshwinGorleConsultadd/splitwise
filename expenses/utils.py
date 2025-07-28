
from django.contrib.auth.models import User
import heapq
from django.shortcuts import get_object_or_404
from groups.models import Group
from .models import Expense

import heapq

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
        if User.objects.filter(id=user_id).exists() is False :
            return f'payers or participants with user_id {user_id} not exists!'
    # Validate total amount and paid amount
    total_expense_amount = expense['amount']
    total_paid_amount = sum([payer['paid_amount'] for payer in expense['payers']])
    if total_expense_amount != total_paid_amount:
        return f'Total expense amount ({total_expense_amount}) does not match total paid amount by payers ({total_paid_amount})'
    
    # Validate share amount against total expense amount
    total_shared_amount = sum([user['share_amount'] for user in expense['participants']])
    if abs(total_expense_amount - total_shared_amount) > 2:
        return f'Total shared amount ({total_shared_amount}) does not match total paid amount by payers ({total_paid_amount})'
    return 'pass'
    
    

def update_existing_depts(transactions,member_list,user_id_to_idx_map,group):
    for member in member_list:
        debts = member.depts_received.filter(group=group)
        for debt in debts:
            from_member = debt.from_member.id
            to_member = member.id
            transactions[user_id_to_idx_map[from_member]][user_id_to_idx_map[to_member]] = debt.amount

def split_expense(expense):
    print("Splitting expense for", expense)
    group = get_object_or_404(Group, id=expense.group.id)
    memberships = group.membership.all()
    member_list = sorted([membership.member for membership in memberships], key=lambda user: user.id)

    # Creating mapping from user ID to index
    user_id_to_idx_map = {member.id: idx for idx, member in enumerate(member_list)}

    # Create a transaction matrix with all the members
    size = len(member_list)
    transactions = [[0 for _ in range(size)] for _ in range(size)]

    # Updating transactions from existing debts (safe access with .filter instead of .get)
    update_existing_depts(transactions=transactions, member_list=member_list, user_id_to_idx_map=user_id_to_idx_map, group=group)

    # Updating transactions as per the current expense share
    expense_shares = sorted(expense.shares.all(), key=lambda share: share.user.id)
    expense_payers = sorted(expense.payers.all(), key=lambda pay: pay.user.id)

    creditors = []
    debtors = []

    for member in member_list:
        share_amount = next(
            (share.share_amount for share in expense_shares if share.user.id == member.id),
            0
        )
        paid_amount = next(
            (payer.paid_amount for payer in expense_payers if payer.user.id == member.id),
            0
        )
        net_amount = paid_amount - share_amount

        if net_amount > 0:
            heapq.heappush(creditors, (-net_amount, member.id))
        elif net_amount < 0:
            heapq.heappush(debtors, (-abs(net_amount), member.id))

    # Settling debts using min-cash-flow logic
    while creditors and debtors:
        mc_amount, mc_member_id = heapq.heappop(creditors)
        md_amount, md_member_id = heapq.heappop(debtors)

        mc_amount = -mc_amount
        md_amount = -md_amount

        paid = min(mc_amount, md_amount)
        transactions[user_id_to_idx_map[md_member_id]][user_id_to_idx_map[mc_member_id]] += paid

        if md_amount > mc_amount:
            heapq.heappush(debtors, (-(md_amount - mc_amount), md_member_id))
        elif mc_amount > md_amount:
            heapq.heappush(creditors, (-(mc_amount - md_amount), mc_member_id))

    # Printing the final transaction matrix
    for row in transactions:
        print(' '.join(str(value) for value in row))

    return transactions
