from django.db import models
import datetime
# Create your models here.
class Product(models.Model):
    product_id = models.CharField(max_length=30, unique=True)
    product_name = models.CharField(max_length=30)
    product_description = models.CharField(max_length=400)
    product_category = models.CharField(max_length=100)
    product_img = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.product_id

class Contact_Query(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    message = models.CharField(max_length=400)
    date_time = models.DateTimeField(("Date"), default=datetime.datetime.today)
    def __str__(self):
        return self.email

