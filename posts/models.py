from django.db    import models

from users.models import User

class Post(models.Model):
    title     = models.CharField(max_length=50)
    post_user = models.CharField(max_length=50)
    content   = models.CharField(max_length=5000)
    user      = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "posts"