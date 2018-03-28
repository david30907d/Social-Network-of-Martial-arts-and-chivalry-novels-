from django.core.management.base import BaseCommand, CommandError
from socialNetwork.models import *

class Command(BaseCommand):
    help = 'calculate socialNetwork from DB'

    def handle(self, *args, **options):
        import numpy as np
        from tqdm import tqdm

        peopleSet = set()
        for i in Correlation.objects.all():
            peopleSet.add(i.source)
            peopleSet.add(i.target)

        file = open('martial.csv', 'w', encoding='utf-8')
        name = ','.join(['name'] + [i for i in peopleSet])
        file.write(name+'\n')
        data = np.zeros((len(peopleSet), len(peopleSet)))

        for sindex, source in tqdm(enumerate(peopleSet)):
            for tindex, target in enumerate(peopleSet):
                querySet = Correlation.objects.filter(source=source, target=target)
                if querySet.count() == 1:
                    data[sindex, tindex] = querySet[0].counts
                    data[tindex, sindex] = querySet[0].counts
                querySet = Correlation.objects.filter(source=target, target=source)
                if querySet.count() == 1:
                    data[tindex, sindex] = querySet[0].counts
                    data[sindex, tindex] = querySet[0].counts

        for source, array in zip(peopleSet, data):
            row = ','.join([source] + [str(i) for i in array])
            file.write(row+'\n')

        self.stdout.write("Finish !")