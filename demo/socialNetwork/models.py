from django.db import models

class Correlation(models.Model):
    source = models.CharField(max_length=10, default='')
    target = models.CharField(max_length=10, default='')
    counts = models.IntegerField(default=0)

    def __str__(self):
        return '{}-{}:{}'.format(self.source, self.target, str(self.counts))