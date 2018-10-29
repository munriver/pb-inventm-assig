from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Role(models.Model):
    roles = (
        ('SA', 'Store Assistant'),
        ('SM', 'Store Manager'),
    )	

class Irecord(models.Model):
    pid = models.IntegerField(unique=True, primary_key=True)
    pname = models.CharField(max_length=20)
    vendor = models.CharField(max_length=50)
    mrp = models.IntegerField(default=0)
    batch_num = models.IntegerField()
    batch_date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=0)

class IrecordUnapproved(models.Model):
    pid = models.IntegerField(unique=True, primary_key=True)
    pname = models.CharField(max_length=20)
    vendor = models.CharField(max_length=50)
    mrp = models.IntegerField(default=0)
    batch_num = models.IntegerField()
    batch_date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    edit_of = models.ForeignKey(Irecord)

class IrecordDel(models.Model):
    del_status_of = models.OneToOneField(Irecord, on_delete=models.CASCADE)

class Iuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.PROTECT) 

	
