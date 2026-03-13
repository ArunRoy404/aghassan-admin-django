from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductPSD(models.Model):
    product = models.ForeignKey(Product, related_name='psd_files', on_delete=models.CASCADE)
    psd_file = models.FileField(upload_to='psds/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PSD for {self.product.name}"
