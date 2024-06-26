from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Category, Post, Comment
from .forms import CommentForm


class PostListView(generic.ListView):
    """
    View for displaying a list of posts, optionally filtered by category.

    Attributes:
        model (Post): The model to use for the queryset.
        queryset (QuerySet): The queryset of posts to be displayed.
        template_name (str): The name of the template to render.
        paginate_by (int): Number of posts to display per page.

    Methods:
        get_queryset: Get the queryset of posts based on the category
        or all posts, and filtered by statue and date created.
        get_context_data: Get additional context data to
        be used in the template.
    """
    model = Post
    template_name = 'post_list.html'
    paginate_by = 4

    def get_queryset(self):
        """
        Get the queryset for the post list view,
        optionally filtered by category.

        If category_name is provided in the URL kwargs,
        filter posts by the specified category.
        If not, return all posts.

        Returns:
            QuerySet: Filtered and ordered queryset of blog posts.
        """
        queryset = Post.objects.filter(status=1).order_by("-created_at")
        category_name = self.kwargs.get('category_name', None)
        if category_name:
            return Post.objects.filter(
                category__name=category_name, status=1
            ).order_by("-created_at")
        else:
            return queryset

    def get_context_data(self, **kwargs):
        """
        Get additional context data for the post list view,
        including all categories

        Returns:
            dict: Additional context data.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostDetail(generic.View):
    """
    View for displaying the details of a single post,
    including comments and like status.

    Methods:
        get: Handle GET requests for viewing a post.
        post: Handle POST requests for submitting comments on a post.
    """

    def get(self, request, slug, *args, **kwargs):
        """
        Handle GET requests for viewing a post.

        Args:
            request: The HTTP request.
            slug (str): The slug of the post.

        Returns:
            HttpResponse: Rendered template with post details.
        """
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        category = post.category
        comments = post.comments.filter(approved=True).order_by("-created_at")
        liked = False

        # Check if the user has liked the post
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "category": category,
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """
        Handle POST requests for submitting comments on a post.

        Args:
            request: The HTTP request.
            slug (str): The slug of the post.

        Returns:
            HttpResponse: Rendered template with updated comments.
        """
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        category = post.category
        comments = post.comments.filter(approved=True).order_by("created_at")
        liked = False

        # Check if the user has liked the post
        if post.likes.filter(id=request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        commented = False

        # Check if a delete comment request was made
        if 'delete_comment_id' in request.POST:
            comment_id_delete = request.POST['delete_comment_id']
            try:
                comment_to_delete = Comment.objects.get(
                    id=comment_id_delete,
                    name=request.user.username
                )
                comment_to_delete.delete()
                messages.success(request, 'Comment deleted successfully.')
            except Comment.DoesNotExist:
                messages.error(
                    request,
                    'Comment not found or permission denied.'
                )

        # Check if an edit comment request was made
        elif 'edit_comment_id' in request.POST:
            comment_id_edit = request.POST['edit_comment_id']
            comment_to_edit = get_object_or_404(
                Comment,
                id=comment_id_edit,
                name=request.user.username
            )

            if comment_form.is_valid():
                comment_to_edit.body = comment_form.cleaned_data['body']
                comment_to_edit.approved = False
                comment_to_edit.save()
                commented = True
                messages.success(
                    request,
                    'Comment updated successfully. Awaiting approval.'
                )
            else:
                error_validation = True
                messages.error(
                    request,
                    'Error updating comment. Please correct the errors below.'
                )

                return render(
                    request,
                    "post_detail.html",
                    {
                        "category": category,
                        "post": post,
                        "comments": comments,
                        "commented": commented,
                        "comment_form": comment_form,
                        "liked": liked,
                        "error_validation": error_validation,
                    },
                )

        # Handle new comment submission
        elif comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            commented = True
            comment.post = post
            comment.save()
            messages.success(
                request,
                'Comment submitted successfully. Awaiting approval.'
            )
        else:
            messages.error(
                request,
                'Error submitting comment. Please correct the errors below.'
            )

        return render(
            request,
            "post_detail.html",
            {
                "category": category,
                "post": post,
                "comments": comments,
                "commented": commented,
                "comment_form": comment_form,
                "liked": liked,
            },
        )


class PostLike(View):
    """
    View for handling post likes.

    Methods:
        post: Handle POST requests for liking/unliking a post.
    """

    def post(self, request, slug, *args, **kwargs):
        """
        Handle POST requests for liking/unliking a post.

        Args:
            request: The HTTP request.
            slug (str): The slug of the post.

        Returns:
            HttpResponseRedirect: Redirect to the post detail page
            after liking/unliking.
        """
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
