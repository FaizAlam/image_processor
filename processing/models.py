from django.db import models


from django.db import models
import uuid

class Request(models.Model):
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Image(models.Model):
    request = models.ForeignKey(Request, related_name='images', on_delete=models.CASCADE)
    input_url = models.URLField()
    output_url = models.URLField(blank=True, null=True)
    product_name = models.CharField(max_length=255, default="older_prods")
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

