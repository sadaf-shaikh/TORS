from django.db import models

# Create your models here.

class status(models.Model):
    pk_status = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class tour(models.Model):
    pk_tour = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name

class customer(models.Model):
    pk_customer = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return self.name

class reservation(models.Model):
    pk_reservation = models.AutoField(primary_key=True)
    fk_tour = models.ForeignKey(tour, on_delete=models.CASCADE)
    fk_customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    tour_date = models.DateField()
    status = models.ForeignKey(status, on_delete=models.CASCADE)

    def __str__(self):
        return self.fk_tour.name


    


    