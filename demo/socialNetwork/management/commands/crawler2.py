from django.core.management.base import BaseCommand, CommandError

# import lib for Crawler
import requests, json
from bs4 import BeautifulSoup

# import Django models
from socialNetwork.models import *

# import jieba
import jieba
import jieba.posseg as pseg

#this version is operate by jieba
class Command(BaseCommand):
	help = 'a crawler for Martial arts and chivalry novels'

	def handle(self, *args, **options):
        
		# Novel parts
		novel = json.load(open('笑傲江湖.json', 'r'))
		###
		#start to cut and calculate word frequency
		jieba.load_userdict('character.txt')
		
		#person with multiple name
		match={'令狐沖':['令狐','沖兒','風大俠'],'任盈盈':['盈盈','任大小姐','聖姑'],
		'左冷禪':['五嶽劍派盟主','嵩山派掌門'],'東方不敗':['日月神教教主','教主'],
		'岳不群':['華山派掌門','五嶽派掌門','君子劍','華山派掌門岳先生'],'寧中則':['寧女俠'],'藍鳳凰':['五仙教教主'],
		'田伯光':['萬里獨行','採花大盜','不可不戒'],'風清揚':['華山派劍宗前辈','風太師叔','風老前輩'],
		'方證大師':['方證','少林寺方丈'],'沖虛道長':['沖虛','武當派掌門'],'莫大':['莫師伯','衡山派掌門','瀟湘夜雨'],
		'恆山派師尊':['恆山三定'],'梅庄四友':['江南四友'],'林遠圖':['渡元'],'福州福威鏢局鏢頭':['史鏢頭','鄭鏢頭'],
		'福州福威鏢局鏢師':['富鏢頭','錢鏢頭','吳鏢頭''高鏢頭','褚鏢頭','崔鏢頭','祝鏢頭','季鏢頭','霍鏢頭','狄鏢頭'],
		'福州福威鏢局趟子手':['白二','陳七'],'林福':['福州福威鏢局男僕'],'華師傅':['福州福威鏢局廚子'],
		'黃先生':['福州福威鏢局帳房'],'劉鏢頭':['福威鏢局浙江杭州分局主持人'],'易鏢頭':['福威鏢局江西南昌分局主持人'],
		'余滄海':['青城派掌門','松風觀觀主'],'青城四秀':['狗熊野豬','青城四獸'],'魯連榮':['金眼鵰','金眼烏鴉'],
		'劉正風':['劉三爺','衡山派副掌門'],'勞德諾':['薩老頭','勞師弟'],
		'天門道人':['泰山派掌門'],'費彬':['大嵩陽手'],'丁勉':['托塔手'],'陸柏':['仙鶴手'],
		'鍾鎮':['九曲劍','鍾師弟'],'鄧八公':['神鞭'],'高克新':['錦毛獅'],'湯英鶚':['紅白劍'],
		'樂厚':['孝感','大陰陽手'],'卜沉':['白頭仙翁'],'沙天江':['禿鷹'],'史登達':['千丈松'],
		'王仲強':['仲強'],'楊蓮亭':['總管','男寵'],'賈布':['黃面尊者'],'上官雲':['鵰俠'],
		'張乘雲':['白猿神魔'],'張乘風':['金猴神魔'],'范松':['大力神魔'],'趙鶴':['飛天神魔'],
		'王元霸':['金刀無敵','洛陽金刀門掌門','金刀無敵王家爺爺'],
		'解風':['丐幫幫主'],'張金鰲':['丐幫副幫主'],'震山子':['乾坤一劍','崑崙派掌門'],
		'夏老拳師':['鄭州六合門掌門'],'鐵老老':['川鄂三峽神女峰'],'潘吼':['東海海沙幫幫主'],
		'白克':['神刀'],'盧西思':['神筆'],'聞先生':['判官'],'木高峰':['塞北明駝'],'平一指':['殺人名醫'],
		'諸草仙':['毒不死人','百藥門掌門人'],'計無施':['夜貓子'],'嚴三星':['雙蛇惡丐','雙龍神丐'],
		'司馬大':['長鯨島島主'],'黃伯流':['銀髯蛟','天河幫幫主'],'丁堅':['一字電劍'],
		'施令威':['五路神'],'白剝皮':['大財主'],'清曉師太':['龍泉水月庵住持']
		}

		adjacency_list={}

		for chapter in novel:
			if chapter!='後記':
				ch=novel[chapter]
				#start to seperate paragraph between 2。
				#avoid 。in talking
				#。in the end
				ch=ch.replace('。』','』')
				ch=ch.replace('。」','」')
				#。 in the middle
				temp=ch
				while temp.find('「')>0:
					talk=temp[temp.find('「'):temp.find('」')+1]
					if talk.find('。')>0:
						before=temp[temp.find('「'):temp.find('」')]
						after=temp[temp.find('「'):temp.find('」')].replace('。','，')
						ch.replace(before,after)
					temp=temp[temp.find('」')+1:]

				#start to calculate correlations
				while ch.find('。')>0:
					paragraph=ch[:ch.find('。')+1]
					name_list=[]#uniqe list for each paragraph
					
					words=pseg.cut(paragraph)
					name_list=[]#uniqe list for each chapter
					for w in words:
						if w.flag=='name' and w.word not in name_list:#'name' for only in chf.txt
							name_list.append(w.word)			

					if len(name_list)>1:
						#combine same person with diff name
						for each in match:
							for nickname in match[each]:
								if nickname in name_list:
									name_list.remove(nickname)
									if each not in name_list:
										name_list.append(each)
						#produce adjacency list
						for each in name_list:
							if each not in adjacency_list:
								adjacency_list[each]={}
							for other in name_list:
								if other!=each:
									if other not in adjacency_list[each]:
										adjacency_list[each][other]=1
									else:
										adjacency_list[each][other]+=1
							name_list.remove(each)

					ch=ch[ch.find('。')+1:-1]
			else:
				continue

		###

		# Insert Into DB
		#placeHolders = [Correlation(**{'source':'david', 'target':'zhou', 'counts':1}), Correlation(**{'source':'tofu', 'target':'huang', 'counts':2})]
		placeHolders=[]
		for src in adjacency_list:
			for tgt in adjacency_list[src]:
				placeHolders.append(Correlation(**{'source':src, 'target':tgt, 'counts':adjacency_list[src][tgt]})) 
		Correlation.objects.bulk_create(placeHolders)
		self.stdout.write("Finish !")