from django.db import models
from django.utils import timezone

# Create your models here.
class Reg_tbl(models.Model):
    fn=models.CharField(max_length=20)
    ln=models.CharField(max_length=20)
    em=models.EmailField(max_length=20)
    gen=models.CharField(max_length=20)
    un=models.CharField(max_length=20)
    ps=models.CharField(max_length=20)
    is_approved=models.BooleanField(default=False)
    pick=models.CharField(max_length=20,blank=False)

    def __str__(self):
        return f"{self.un} ({self.gen})"
    
class Pass_tbl(models.Model):
    customer = models.ForeignKey(Reg_tbl, on_delete=models.CASCADE, related_name="bookings_as_customer")
    worker = models.ForeignKey(Reg_tbl, on_delete=models.CASCADE, related_name="bookings_as_worker", limit_choices_to={'gen': 'worker'})
    pick=models.CharField(max_length=20)
    drop=models.CharField(max_length=20)
    options=models.CharField(max_length=20)

    def __str__(self):
        return f"{self.customer.un} booked to {self.drop}"
    
class Bike_tbl(models.Model):
    worker = models.ForeignKey(Reg_tbl, on_delete=models.CASCADE, limit_choices_to={'gen': 'worker'})
    bnm=models.CharField(max_length=25)
    bml=models.IntegerField()
    bimg=models.FileField(upload_to='pic')

    def __str__(self):
        return f"{self.bnm} ({self.worker.un})"
    
class Feed_tbl(models.Model):
    user=models.ForeignKey(Reg_tbl,on_delete=models.CASCADE,limit_choices_to={'gen': 'user'})
    message=models.TextField(null=True,blank=True)
    rating = models.IntegerField()  # Use validators for restricting range (e.g., 1-5)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.un}"  
    