from django.db import models
from django.conf import settings
from django.utils import timezone


class Item(models.Model):
    TYPE = [
        ('art and music', 'art and music'),
        ('books and stationery', 'books and stationery'),
        ('clothes and shoes', 'clothes and shoes'),
        ('cosmetics and beauty', 'cosmetics and beauty'),
        ('education', 'education'),
        ('electronics and devices', 'electronics and devices'),
        ('food and drink', 'food and drink'),
        ('health and medicine', 'health and medicine'),
        ('household products', 'household products'),
        ('repair', 'repair'),
        ('services', 'services'),
        ('other', 'other'),
    ]
    COUNTTYPE = [
        ('l', 'l'),
        ('kg', 'kg'),
        ('pc', 'pc')
    ]
    ISDONE = [
        ('yes', 'yes'),
        ('no', 'no')
    ]
    
    item_author = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                    on_delete=models.CASCADE)
    item_type = models.CharField(max_length=50, choices=TYPE)
    item_name = models.CharField(max_length=100)
    item_count = models.FloatField()
    item_counttype = models.CharField(max_length=5, choices=COUNTTYPE)
    item_description = models.TextField(blank=True)
    item_created = models.DateTimeField(default=timezone.now)
    item_executed = models.DateField(blank=True, null=True)
    item_isdone = models.CharField(max_length=5, choices=ISDONE)

    def set_date(self):
        self.item_created = timezone.now()
        self.save()

    def __str__(self):
        return self.item_description


class Code(models.Model):

    code_value = models.CharField(max_length=8, default=None)
    code_email = models.EmailField(max_length=254, default=None)
    code_created = models.DateTimeField(default=timezone.now)
    code_token = models.CharField(max_length=130, default=None)
    code_attempt = models.IntegerField(default=0)
    code_step = models.IntegerField(default=0)

    @staticmethod
    def create_code(code_value, code_email, code_created, code_token):
        code = Code.objects.create(code_value=code_value, 
                    code_email=code_email, code_created=code_created, 
                    code_token=code_token, code_attempt=0,
                    code_step=0)
        return code

    def __str__(self):
        return self.code_value
