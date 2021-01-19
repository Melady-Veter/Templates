from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    author_raiting = models.IntegerField(default=0)


    def update_raiting(self):
        posts = Post.objects.filter(author=self.id)
        post_raiting = sum([r.post_raiting * 3 for r in posts])
        comment_raiting = sum([r.comment_raiting for r in Comment.objects.filter(author=self.author)])
        all_to_post_comment_raiting = sum([r.comment_raiting for r in Comment.objects.filter(post__in = posts)])
        self.author_raiting = post_raiting + comment_raiting + all_to_post_comment_raiting
        self.save()


    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'

    POST_TYPES = [
        (NEWS, 'News'),
        (ARTICLE, 'Article'),
    ]
    type = models.CharField(max_length=2, choices=POST_TYPES, default=NEWS)
    created_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    article_text = models.TextField()
    post_raiting = models.IntegerField(default=0)

    def preview(self):
        preview = self.article_text[:129] + '...'
        return preview

    def like(self):
        self.post_raiting += 1
        self.save()

    def dislike(self):
        self.post_raiting -= 1
        self.save()

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория поста'
        verbose_name_plural = 'Категории постов'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    comment_raiting = models.IntegerField(default=0)

    def like(self):
        self.comment_raiting += 1
        self.save()

    def dislike(self):
        self.comment_raiting -= 1
        self.save()

    def __str__(self):
        info = str(self.author.username) + ' - ' + str(self.id)
        return info

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'