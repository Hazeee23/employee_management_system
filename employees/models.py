from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    date_hired = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='employee_photos/', blank=True)

    @property
    def years_of_service(self):
        from datetime import date

        return max(0, date.today().year - self.date_hired.year - ((date.today().month, date.today().day) < (self.date_hired.month, self.date_hired.day)))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
