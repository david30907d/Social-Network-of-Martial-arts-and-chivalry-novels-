from django.shortcuts import render
from django.http import JsonResponse
from socialNetwork.models import *
# Create your views here.

def api(request):
	return JsonResponse([(i.source, i.target, i.counts) for i in Correlation.objects.all()], safe=False)