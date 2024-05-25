from django.db import models

class Tag(models.Model):
    caption=models.CharField(max_length=20)

    def __str__(self):
        return self.caption

class Author(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=50)
    email_address=models.EmailField()

    def __str__(self):
        return self.first_name+" "+self.last_name

class Post(models.Model):
    title=models.CharField(max_length=10)
    excerpt=models.CharField(max_length=50)
    slug=models.SlugField(unique=True, db_index=True)
    content=models.TextField()
    image=models.ImageField(upload_to='posts',null=True)
    author=models.ForeignKey(Author, null=True,on_delete=models.SET_NULL,related_name="posts")
    tag=models.ManyToManyField(Tag)
    date=models.DateField(auto_now=True)

class Comment(models.Model):
    user_name=models.CharField(max_length=20)
    user_email=models.EmailField()
    text=models.TextField(max_length=400)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
