from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class Posts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    caption = models.CharField(max_length=255)
    postmedia = models.FileField(null=True,upload_to='uploads/post_media')
    publication_date = models.DateTimeField(auto_now_add=True)
    postlocation=models.CharField(max_length=100,blank=True)
    def __str__(self):
        return str(self.user)


