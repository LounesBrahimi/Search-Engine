from django.db import models

# Book : 
class BookM(models.Model):
    id     = models.IntegerField(primary_key=True)
    title  = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default="unknown")
    lang   = models.CharField(max_length=10)
    body   = models.TextField(default="this is our book body")     

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id','title'], name='unique')
        ]
        ordering = ['id' , 'title']


# Book indexé
# class BookMIndexé(models.Model):
#     id = ...

