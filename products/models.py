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
    image_without_warp = models.ImageField(upload_to='psd_thumbnails/', null=True, blank=True)
    structure_json = models.JSONField(null=True, blank=True)
    psd_type = models.CharField(max_length=20, choices=[('preview', 'Preview'), ('mockup', 'Mockup')], default='preview')
    name = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PSD for {self.product.name}"

class MockupResult(models.Model):
    product = models.ForeignKey(Product, related_name='mockup_results', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='mockups/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mockup for {self.product.name} ({self.id})"
