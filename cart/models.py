from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from catalogue.models import Livre

# Create your models here.
class BookPricing(models.Model):
    livre = models.OneToOneField(Livre, on_delete=models.CASCADE,related_name='pricing')
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    discount_start = models.DateField(null=True, blank=True)
    discount_end = models.DateField(null=True, blank=True)
    @property
    def final_price(self):
        from datetime import date
        today = date.today()
        if self.discount_percent > 0:
            if self.discount_start and self.discount_end:
                if not (self.discount_start <= today <= self.discount_end):
                    return self.base_price
            discount = self.base_price * (self.discount_percent / 100)
            return round(self.base_price - discount, 2)
        return self.base_price
    @property
    def is_on_sale(self):
        from datetime import date
        today = date.today()
        if self.discount_percent > 0 and self.discount_start and self.discount_end:
            return self.discount_start <= today <= self.discount_end
        return self.discount_percent > 0
    def __str__(self):  
        return f"{self.livre} - {self.final_price} DT"
class CartItem(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
    def save(self,*args, **kwargs):
        if not self.unit_price: # seulement si pas encore défini
            try:
                self.unit_price = self.livre.pricing.final_price
            except BookPricing.DoesNotExist:
                self.unit_price = 0
        super().save(*args, **kwargs)
    @property #utiliser se fonction comme variable  mahish fi base de donner  teb3a class cahaw 
    def subtotal(self): # utile pour le template
        return self.unit_price * self.quantity
    def __str__(self):
        user_display = self.user.username if self.user else "Guest"
        return f"Cart({self.status}, {user_display}, {self.quantity} x {self.livre.titre})"