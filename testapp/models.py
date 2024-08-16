from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contract(models.Model):
    contract_number = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contract_number


class CreditApplication(models.Model):
    application_number = models.CharField(max_length=255)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, related_name='credit_application')
    products = models.ManyToManyField(Product, related_name='credit_applications')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.application_number

