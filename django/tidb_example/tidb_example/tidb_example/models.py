from django.db import models


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=250)
    price = models.FloatField()
