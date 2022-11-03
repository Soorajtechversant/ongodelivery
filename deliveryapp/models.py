from django.db import models
from django.contrib.auth.models import User
from distutils.command.upload import upload
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    stripeid = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)



class Ongo(models.Model):
    brand = models.CharField(max_length=50)
    product_model = models.CharField(max_length=50)
    material_type = models.CharField(max_length=50)
    price = models.IntegerField()
    picture = models.ImageField(upload_to = 'media',null=True,blank = True)

    def __str__(self):
        return self.product_model

