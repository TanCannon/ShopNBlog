from django.db import models

#manually imported
from django.contrib.auth.models import User
from django.utils.timezone import now
from ckeditor.fields import RichTextField #to use the rich text ckeditor
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.

class Blogpost(models.Model):
    post_id = models.AutoField(primary_key= True)
    tilte = models.CharField(max_length=50)
    head0 = models.CharField(max_length=500, default="")
    chead0 = models.CharField(max_length=5000, default="")
    head1 = models.CharField(max_length=500, default="")
    chead1 = models.CharField(max_length=5000, default="")
    head2 = models.CharField(max_length=500, default="")
    # chead2 = models.CharField(max_length=5000, default="")
    chead2 = RichTextUploadingField()
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to='blog/images', default="")

    def __str__(self):
        return self.tilte

'''Djnago has its own models to handel users (by 'User' class) so we don't need to make one of our own'''

class BlogComment(models.Model):
    #comment unique id
    comment_id = models.AutoField(primary_key=True)
    #what is the comment
    comment = models.TextField()
    #who wrote
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #on which post the comment is made
    post = models.ForeignKey(Blogpost,on_delete=models.CASCADE)
    #to which comment its a reply or is it a 1st comment i.e null=True
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    #when comment was posted
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username
    