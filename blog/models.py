from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Draft"), (1, "Published"))


class Category(models.Model):
    """
    Represents a category for blog posts.

    Attributes:
        name (str): The name of the category.

    Methods:
        __str__: Returns a string representation of the category.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns the name of the category as its string representation.
        """
        return self.name


class Post(models.Model):
    """
    Represents a blog post.

    Attributes:
        title (str): The title of the post.
        slug (str): A unique slug for the post's URL.
        author (User): The author of the post (ForeignKey to User model).
        category (Category): The category to which the post belongs (ForeignKey to Category model).
        content (str): The main content of the post.
        featured_image (CloudinaryField): The featured image of the post.
        likes (QuerySet): The users who liked the post.
        created_at (datetime): The timestamp when the post was created.
        updated_at (datetime): The timestamp when the post was last updated.
        status (int): The status of the post (Draft or Published).
        excerpt (str): A short excerpt from the post.

    Meta:
        ordering (List[str]): The default ordering for the posts based on the creation timestamp.

    Methods:
        __str__: Returns a string representation of the post.
        number_of_likes: Returns the count of users who liked the post.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)

    class Meta:
        """
        The default ordering for the posts based on the creation timestamp.
        """
        ordering = ['created_at']

    def __str__(self):
        """
        Returns the title of the post as its string representation.
        """
        return self.title

    def number_of_likes(self):
        """
        Returns the count of users who liked the post.
        """
        return self.likes.count()


class Comment(models.Model):
    """
    Represents a comment on a blog post.

    Attributes:
        post (Post): The post to which the comment belongs (ForeignKey to Post model).
        name (str): The name of the commenter.
        email (str): The email of the commenter.
        body (str): The content of the comment.
        created_at (datetime): The timestamp when the comment was created.
        approved (bool): Indicates whether the comment is approved or not.

    Meta:
        ordering (List[str]): The default ordering for the comments based on the creation timestamp.

    Methods:
        __str__: Returns a string representation of the comment.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=90)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        """
        The default ordering for the comments based on the creation timestamp.
        """
        ordering = ['created_at']

    def __str__(self):
        """
        Returns a string representation of the comment, including the post title and commenter's name.
        """
        return f"commented on {self.post.title} by {self.name}"
