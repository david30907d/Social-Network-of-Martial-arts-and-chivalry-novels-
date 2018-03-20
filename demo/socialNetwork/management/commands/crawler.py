from django.core.management.base import BaseCommand, CommandError

# import lib for Crawler
import requests, json
from bs4 import BeautifulSoup

# import Django models
from socialNetwork.models import *

class Command(BaseCommand):
    help = 'a crawler for Martial arts and chivalry novels'

    def handle(self, *args, **options):
        # Crawler Parts
        ###
        ###

        # Novel parts
        novel = json.load(open('笑傲江湖.json', 'r'))
        ###

        # Do some bullshit
        ###

        # Insert Into DB
        placeHolders = [Correlation(**{'source':'david', 'target':'zhou', 'counts':1}), Correlation(**{'source':'tofu', 'target':'huang', 'counts':2})]
        Correlation.objects.bulk_create(placeHolders)
        self.stdout.write("Finish !")