from django.core.management.base import BaseCommand, CommandError

# import lib for Crawler
import requests, json
from bs4 import BeautifulSoup

# import Django models
from socialNetwork.models import *

# import jieba
import jieba
import jieba.posseg as pseg
class Command(BaseCommand):
	help = 'a crawler for Martial arts and chivalry novels'

	def handle(self, *args, **options):
        
		# Novel parts
		novel = json.load(open('笑傲江湖.json', 'r'))
		###
		#start to cut and calculate word frequency
		jieba.load_userdict('charactor.txt')
		adjacency_list={}
		for chapter in novel:
			words=pseg.cut(novel[chapter])
			name_list=[]#uniqe list for each chapter
			for w in words:
				if w.flag=='name' and w.word not in name_list:#'name' for only in chf.txt
					name_list.append(w.word)
			for each in name_list:
				if each not in adjacency_list:
					adjacency_list[each]={}
				for other in name_list:
					if other!=each:
						if other not in adjacency_list[each]:
							adjacency_list[each][other]=1
						else:
								adjacency_list[each][other]+=1
				name_list.remove(each)#avoid duplicate
			#break
		###

		# Insert Into DB
		#placeHolders = [Correlation(**{'source':'david', 'target':'zhou', 'counts':1}), Correlation(**{'source':'tofu', 'target':'huang', 'counts':2})]
		placeHolders=[]
		for src in adjacency_list:
			for tgt in adjacency_list[src]:
				placeHolders.append(Correlation(**{'source':src, 'target':tgt, 'counts':adjacency_list[src][tgt]})) 
		Correlation.objects.bulk_create(placeHolders)
		self.stdout.write("Finish !")