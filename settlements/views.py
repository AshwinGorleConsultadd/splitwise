from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import heapq

from decimal import Decimal
from .models import Debt
from django.contrib.auth.models import User

def settle_group_debts(expense, minimized_transactions):

    # Creating mapping from user ID to index
    group = expense.group
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
