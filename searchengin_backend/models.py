from django.db import models

# Book : 
class BookM(models.Model):
    id     = models.IntegerField(primary_key=True)
    title  = models.CharField(max_length=15)
    author = models.CharField(max_length=10, default="unknown")
    body   = models.TextField(default="this is our book body") 
    lang   = models.CharField(max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id','title'], name='unique')
        ]
        ordering = ['id' , 'title']


# Book indexé
# class BookMIndexé(models.Model):
#     id = 

