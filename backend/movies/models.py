from django.db import models

# Create your models here.


class MovieData(models.Model):
  
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=500, null=False)
    title_ko = models.TextField(null=False)
    title_en = models.TextField(null=False, db_column='title_en')
    year = models.IntegerField(null=False)
    plot = models.TextField(null=True)
    runtime = models.IntegerField(null=True)
    genre = models.CharField(max_length=30, null=True)
    difficulty = models.IntegerField(null=True)


    class Meta:

        db_table = 'movie_data'  