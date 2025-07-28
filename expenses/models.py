from django.db import models

# Create your models here.
class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    group = models.ForeignKey('groups.Group', related_name='expenses', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f"{self.title} - {self.amount} by "


class ExpenseShare(models.Model):
    expense = models.ForeignKey(Expense, related_name='shares', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='expense_shares', on_delete=models.CASCADE)
    share_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('expense', 'user')

    def _str_ (self):
        return f"{self.user.username} owes {self.owned_amount} for {self.expense.title}"
        
class ExpensePayer(models.Model):
    expense = models.ForeignKey(Expense, related_name='payers', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='expense_payers', on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        unique_together = ('expense', 'user')
    def __str__(self):
        return f"{self.user.username} paid {self.paid_amount} for {self.expense.title}"

