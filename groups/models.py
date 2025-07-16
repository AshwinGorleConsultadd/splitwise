from django.db import models
from django.conf import settings

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=500, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='created_groups', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name

class Membership(models.Model):
    group = models.ForeignKey(Group, related_name='membership', on_delete=models.CASCADE)
    member = models.ForeignKey('auth.User', related_name='group_memberships', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'member')
    
    def __str__(self):
        return f"{self.member.username} in {self.group.name}"