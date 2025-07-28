import heapq
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from .models import Debt
from django.contrib.auth.models import User
from expenses.models import Expense
from groups.models import Group

def settle_group_debts(group , minimized_transactions):
    # Creating mapping from user ID to index
    # group = expense.group
    memberships = group.membership.all()
    member_list = sorted([membership.member for membership in memberships], key=lambda user: user.id)
    index_to_user = { idx : member.id for idx, member in enumerate(member_list)}
    
    print("Index to User Mapping:", index_to_user)
    # Deleting existing debt records in this group
    Debt.objects.filter(group=group).delete()

    # Creating updated debts from minimized_transactions
    for i in range(len(minimized_transactions)):
        for j in range(len(minimized_transactions)):
            amount = minimized_transactions[i][j]
            if amount > 0:
                from_member = index_to_user[i]
                to_member = index_to_user[j]
                rounded_amount = Decimal(str(round(amount, 2)))
                
                Debt.objects.create(
                    from_member= User.objects.get(id = from_member),
                    to_member=User.objects.get(id = to_member),
                    group=group,
                    amount=rounded_amount
                )

def minimize_cashflow(transactions):
    print ("Minimizing cash flow for transactions:")
    n = len(transactions)

    # Calculate net amount for each person
    net_amounts = [0] * n
    for p in range(n):
        for i in range(n):
            net_amounts[p] += (transactions[i][p] - transactions[p][i])

    # Creating th heaps for creditors and debtors
    creditors = []
    debtors = []
    for i in range(n):
        if net_amounts[i] > 0:
            heapq.heappush(creditors, (-net_amounts[i], i)) 
        elif net_amounts[i] < 0:
            heapq.heappush(debtors, (net_amounts[i], i))      

    
    minimized_transactions = [[0 for _ in range(n)] for _ in range(n)]

    while creditors and debtors:
        credit_amount, creditor = heapq.heappop(creditors)
        debt_amount, debtor = heapq.heappop(debtors)

        credit_amount = -credit_amount  
        debt_amount = -debt_amount     

        settle_amount = min(credit_amount, debt_amount)
        minimized_transactions[debtor][creditor] = settle_amount

        remaining_credit = credit_amount - settle_amount
        remaining_debt = debt_amount - settle_amount

        if remaining_credit > 0:
            heapq.heappush(creditors, (-remaining_credit, creditor))
        if remaining_debt > 0:
            heapq.heappush(debtors, (-remaining_debt, debtor))

    print("Minimized transactions:")
    for row in minimized_transactions:
        print(' '.join(str(value) for value in row))

    return minimized_transactions


def split_expense_bulk(expenses):
    print( "Splitting expenses for multiple expenses")
    """
    Takes a list of expenses and returns the final transaction matrix.
    """
    # Step 1: Build user index map
    
    user_ids = set()
    for expense in expenses:
        for share in expense.shares.all():
            user_ids.add(share.user.id)
        for payer in expense.payers.all():
            user_ids.add(payer.user.id)
    
    user_id_list = list(user_ids)
    user_to_index = {uid: idx for idx, uid in enumerate(user_id_list)}
    n = len(user_id_list)

    # Step 2: Initialize transaction matrix
    transactions = [[0 for _ in range(n)] for _ in range(n)]

    # Step 3: For each expense, calculate individual debts
    for expense in expenses:
        total_amount = sum([payer.paid_amount for payer in expense.payers.all()])
        payer_map = {payer.user.id: payer.paid_amount for payer in expense.payers.all()}
        shares = expense.shares.all()

        # Calculate each member’s share
        for share in shares:
            owed_by = share.user.id
            share_amount = share.share_amount

            for paid_by, paid_amount in payer_map.items():
                if paid_by == owed_by:
                    continue  # No debt to self
                # how much this payer paid on behalf of owed_by
                paid_share = (paid_amount / total_amount) * share_amount
                transactions[user_to_index[owed_by]][user_to_index[paid_by]] += round(paid_share, 2)
                
    print("Transaction matrix after processing all expenses:")
    for row in transactions:
        print(' '.join(str(value) for value in row))

    return transactions




def recalculate_group_debts(group):
    print('Recalculating debts for group:', group.name)
    expenses = Expense.objects.filter(group=group)
    
    # Get the full transaction matrix
    transactions = split_expense_bulk(expenses)

    # Minimize the cashflow
    minimized_transactions = minimize_cashflow(transactions)

    # Update debts
    settle_group_debts(group=group, minimized_transactions=minimized_transactions)
