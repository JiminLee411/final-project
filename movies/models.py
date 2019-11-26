from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=150)
    genre_id = models.TextField()
    
    def __str__(self):
        return self.name
        
class Movie(models.Model):
    adult = models.TextField()
    budget = models.TextField()
    genres = models.TextField()
    original_title = models.TextField()
    overview = models.TextField() # description
    popularity = models.TextField() # audience
    poster_path = models.TextField() # post_url
    release_date = models.TextField()
    revenue = models.TextField()
    runtime = models.TextField()
    tagline = models.TextField()
    title = models.CharField(max_length=150)
    vote_average = models.FloatField()
    actor_1 = models.TextField()
    actor_2 = models.TextField()
    actor_3 = models.TextField()
    actor_4 = models.TextField()
    actor_5 = models.TextField()
    director = models.CharField(max_length=45)
    file_path_1 = models.TextField()
    file_path_2 = models.TextField()
    file_path_3 = models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movies")
    
    def __str__(self):
        return self.title
        
class Actor(models.Model):
    actor_id = models.TextField()
    actor_name = models.TextField()
    
    def __str__(self):
        return self.actor_name

        
class Rating(models.Model): # Review
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    comment = models.TextField()
    score = models.IntegerField(default=1,
                validators=[
                    MaxValueValidator(10),
                    MinValueValidator(1)
            ])
    
    def username(self):
        return self.user.username

    def __str__(self):
        return f'{self.movie} | {self.score} | {self.comment}'
© 2019 GitHub, Inc.