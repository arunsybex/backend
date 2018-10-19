# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class message_details(models.Model):
	user_from = models.CharField(max_length=200,null=True)
	user_to = models.CharField(max_length=200,null=True)
	message = models.CharField(max_length=200,null=True)
	nonce = models.CharField(max_length=200,null=True)
	checksum = models.CharField(max_length=200,null=True)
	created = models.DateTimeField(auto_now_add=True)
	acction_pos = models.IntegerField(unique=True)