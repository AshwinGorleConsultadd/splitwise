from django.db import models
from django.conf import settings
from groups.models import Group
from django.contrib.auth.models import User


# Create your models here.
class Debt(models.Model):
    from_member = models.ForeignKey('auth.User', related_name='depts_given', on_delete=models.CASCADE)
    to_member = models.ForeignKey('auth.User', related_name='depts_received', on_delete=models.CASCADE)
    group = models.ForeignKey('groups.Group', related_name='depts', null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('from_member', 'to_member', 'group')
    
    def __str__(self):
        return f"{self.from_member.username} owes {self.to_member.username} {self.amount} in {self.group.name if self.group else 'no group'}"