from django.contrib import admin
from .models import Category, Post, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Customizes admin interface for the Category model.

    Attributes:
        list_filter (list): Filters displayed categories based on 'name'.
    """
    list_filter = ['name']


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Customizes admin interface for the Post model,
    using Summernote for the 'content' field.

    Attributes:
        list_display (tuple):
        Specifies the fields to be displayed in the change list.
        search_fields (list):
        Enables search functionality for 'title' and 'content'.
        prepopulated_fields (dict):
        Automatically fills the 'slug' field based on 'title'.
        list_filter (tuple):
        Filters displayed posts based on 'status', 'category',
        and 'created_at'.
        summernote_fields (tuple):
        Enables the Summernote WYSIWYG editor for the 'content' field.
    """
    list_display = ('title', 'slug', 'status', 'created_at')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'category', 'created_at')
    summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Customizes admin interface for the Comment model.

    Attributes:
        list_display (tuple):
        Specifies the fields to be displayed in the change list.
        list_filter (tuple):
        Filters displayed comments based on 'approved' and 'created_at'.
        search_fields (tuple):
        Enables search functionality for 'name', 'email', and 'body'.
        actions (list):
        Specifies the available custom actions, such as 'approve_comments'.
    """
    list_display = ('name', 'body', 'post', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        """
        Action method to approve selected comments.
        """
        queryset.update(approved=True)
