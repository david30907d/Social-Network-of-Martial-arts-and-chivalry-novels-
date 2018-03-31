from django.core.management.base import BaseCommand, CommandError

# import Social Network
import networkx as nx
# import Django models
from socialNetwork.models import *

class Command(BaseCommand):
    help = 'calculate socialNetwork from DB'

    def handle(self, *args, **options):
        # initialize Graph
        G = nx.Graph()

        # Query edges from DB and insert them into Graph
        G.add_edges_from([(i.source, i.target) for i in Correlation.objects.all()])

        # Showing info of Graph
        print(nx.info(G))
        print('transitivity (global clustering coefficient):' + str(nx.transitivity(G)))
        print('average_clustering (average all local clustering coefficient to get this):' + str(nx.average_clustering(G)))
        self.stdout.write("Finish !")