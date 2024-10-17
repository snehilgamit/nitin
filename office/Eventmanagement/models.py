from django.db import models

# Create your models here.
class EventDetails(models.Model):
    event_name = models.CharField(max_length=100,unique=True)
    event_hotel = models.CharField(max_length=150, null=True)
    event_location = models.CharField(max_length=100)
    event_date = models.DateField()
    warehouse_location=models.CharField(max_length=20)
    event_id = models.IntegerField(unique=True)
    person_name=models.CharField(max_length=100,null=True)
    status = models.BooleanField(default=True)
    remark_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.event_name + ' - ' + str(self.event_date)


class EventProduct(models.Model):
    qr_code = models.CharField(max_length=255, null=False)
    event_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    def __str__(self):
        return str(self.event_id) + " --" + self.product_name


class temporaryaddeventdb(models.Model):
    event_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    count = models.CharField(max_length=10,null=True)  # Assuming count is a string like "10"
    serial_number = models.CharField(max_length=50,null=True)
    remark_note = models.CharField(max_length=255, blank=True)  # Adjust max_length as needed

    def __str__(self):
        return self.product_name +" - "+str(self.event_id)