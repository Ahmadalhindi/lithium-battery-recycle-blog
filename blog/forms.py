from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    """
    A form for handling comments.

    This form is used to create and update Comment objects in the database.
    It extends the ModelForm class and specifies the model and fields
    to be used.

    Attributes:
        model (Comment): The model associated with this form.
        fields (tuple): The fields from the model to include in the form.
    """
    class Meta:
        model = Comment
        fields = ('body',)
