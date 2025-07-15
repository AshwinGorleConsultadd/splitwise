from django.db import models

# Create your models here.
class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    group = models.ForeignKey('groups.Group', related_name='expenses', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    paid_by = models.ForeignKey('auth.User', related_name='expenses', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f"{self.title} - {self.amount} by {self.paid_by.username}"


class ExpenseShare(models.Model):
    expense = models.ForeignKey(Expense, related_name='shares', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='expense_shares', on_delete=models.CASCADE)
    owned_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_ (self):
        return f"{self.user.username} owes {self.owned_amount} for {self.expense.title}"


class Dept(models.Model):
    from_member = models.ForeignKey('auth.User', related_name='depts_given', on_delete=models.CASCADE)
    to_member = models.ForeignKey('auth.User', related_name='depts_received', on_delete=models.CASCADE)
    group = models.ForeignKey('groups.Group', related_name='depts', null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('from_member', 'to_member', 'group')
    
    def __str__(self):
        return f"{self.from_member.username} owes {self.to_member.username} {self.amount} in {self.group.name if self.group else 'no group'}"