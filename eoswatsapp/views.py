from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
import json
from .models import message_details
from django.contrib.auth.models import User
import requests as req
from django.db.models import Max,Q


def notify_user():
	max_pos = message_details.objects.all().aggregate(Max('acction_pos'))
	print max_pos["acction_pos__max"]
	max_pos = int(max_pos["acction_pos__max"]) if (max_pos["acction_pos__max"] is not None) else 11;
	max_pos1 = max_pos + 1
	data = {
		"pos" : max_pos1,
		"offset" : 1,
		"account_name":"watsapptest1"
	}
	data = req.post("http://junglehistory.cryptolions.io:18888/v1/history/get_actions",data=json.dumps(data))
	if data.status_code == 200:
		for actions in json.loads(data.text)["actions"]:
			print actions["action_trace"]["act"]["data"]
			if "msg" in actions["action_trace"]["act"]["data"].keys():
				print actions["action_trace"]["act"]["data"]["msg"]
				msg_data  = json.loads(actions["action_trace"]["act"]["data"]["msg"])
				message   = msg_data["message"]
				nonce     = msg_data["nonce"]
				checksum  = msg_data["checksum"]
				user_from = str(actions["action_trace"]["act"]["data"]["from"])
				user_to   = str(actions["action_trace"]["act"]["data"]["to"])
				try:
					message_details(acction_pos=max_pos1,message = message,user_from=user_from,user_to=user_to,\
						nonce=nonce,checksum=checksum).save()
				except:
					pass
					# print "yes"
	else:
		print data


def getmsg(request):
	if request.method == "GET":
		notify_user()
		user_from = str(request.GET.get("user_from",""))
		user_to = str(request.GET.get("user_to",""))
		limit = int(request.GET.get("limit",10))
		pages = int(request.GET.get("pages",0))
		if user_to != "":
			data = message_details.objects.filter(Q(Q(user_from = user_from) & Q(user_to = user_to)) | Q(Q(user_from = user_to) & Q(user_to = user_from))).order_by("-created")[pages:limit]
			data = serializers.serialize("json", data, fields=('message', 'user_from','user_to','acction_pos','nonce','checksum','created'))
			return JsonResponse(data, safe=False)
		else:
			data = message_details.objects.filter(Q(user_from = user_from) | Q(user_to = user_from)).order_by("-created")
			data = serializers.serialize("json", data)
			return JsonResponse(data, safe=False)
	else:
		return JsonResponse({'error': 'Invalid request method'},decoder, safe=False, mimetype="application/json")
