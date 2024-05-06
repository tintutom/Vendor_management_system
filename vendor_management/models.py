from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Avg
from django.db.models import F


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True)
    
    def clean(self):
        super().clean()
        if self.order_date and self.delivery_date and self.delivery_date < self.order_date:
            raise ValidationError("Delivery date cannot be before order date")
        
    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)


@receiver([post_save, post_delete], sender=PurchaseOrder)
def update_performance_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    calculate_performance_metrics(vendor)

def calculate_performance_metrics(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    total_completed_orders = completed_orders.count()

    if total_completed_orders > 0:
        on_time_deliveries = completed_orders.filter(delivery_date__lte=F('acknowledgment_date')).count()
        vendor.on_time_delivery_rate = on_time_deliveries / total_completed_orders

        vendor.quality_rating_avg = completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg']

    acknowledged_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    total_acknowledged_orders = acknowledged_orders.count()

    if total_acknowledged_orders > 0:
        avg_response_time = acknowledged_orders.aggregate(avg_response_time=Avg(models.F('acknowledgment_date') - models.F('issue_date')))['avg_response_time']
        vendor.average_response_time = avg_response_time.total_seconds()

    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    if total_orders > 0:
        fulfilled_orders = completed_orders.filter(quality_rating__isnull=False)
        vendor.fulfillment_rate = fulfilled_orders.count() / total_orders

    vendor.save()
    
# Connect signal handlers to the PurchaseOrder model
post_save.connect(update_performance_metrics, sender=PurchaseOrder)
post_delete.connect(update_performance_metrics, sender=PurchaseOrder)
