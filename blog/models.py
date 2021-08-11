from django.db import models

# Create your models here.

class blogPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500, default="")
    head0 = models.CharField(max_length=500, default="")
    head0_content = models.CharField(max_length=50000,default="")
    head1 = models.CharField(max_length=500, default="")
    head1_content = models.CharField(max_length=50000,default="")
    head2 = models.CharField(max_length=500, default="")
    head2_content = models.CharField(max_length=50000,default="")
    publish_date = models.DateTimeField(default="")
    thumbnail= models.ImageField(upload_to='blog/images', default="")

    def __str__(self):
        return f"{self.title}"
