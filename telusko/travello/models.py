from django.db import models

# Create your models here.


class Destination(models.Model):

    # default_auto_field = 'django.db.models.AutoField'
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name
