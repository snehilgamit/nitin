from django.db import models
class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    qr_code = models.CharField(max_length=255, unique=True, null=False)
    serial_number = models.CharField(max_length=255,null=True)
    model = models.CharField(max_length=255,null=True)
    configuration = models.TextField(null=True)
    working_status = models.CharField(max_length=10, default='working')
    warehouse_location = models.CharField(max_length=255,null=True)
    buy_date = models.DateField(null=True)
    brand_name = models.CharField(max_length=255,null=True)
    office_status = models.CharField(max_length=255, null=False)
    event_name=event_name = models.CharField(max_length=100,default="",null=True)
    def __str__(self):
        return self.name+" - " +self.qr_code