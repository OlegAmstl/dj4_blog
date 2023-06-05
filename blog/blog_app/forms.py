from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    """
    Форма отправки постов по email.
    """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """
    Форма написания коментария.
    """

    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
