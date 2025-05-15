from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    name = models.CharField(_("tag name"), max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Post(models.Model):
    title = models.CharField(_("post title"), max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="posts",
        verbose_name=_("author"),
        null=True,
        on_delete=models.SET_NULL,
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts_list")
    content = models.TextField(_("post content"))
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="posts_likes",
        verbose_name=_("likes"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="post_comments",
        verbose_name=_("author"),
        null=True,
        on_delete=models.SET_NULL,
    )
    content = models.TextField(_("comment content"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def __str__(self):
        return f"{self.body[:20]}... by {self.author.username}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
