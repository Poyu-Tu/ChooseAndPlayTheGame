from django.db import models

# Create your models here.
class Member(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    
# python manage.py shell
    
#查全部的資料
'''
from members.models import Member 
members = Member.objects.all()
for member in members:
    print(f'Username: {member.username}, Password: {member.password}')
'''

#刪除單筆
'''
from members.models import Member 
Member.objects.filter(username='xxx').delete()
'''

#刪除全部
'''
from members.models import Member 
Member.objects.all().delete()
'''