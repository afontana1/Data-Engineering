from django import forms
from django.contrib.auth.forms import UserCreationForm

class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Name"
        })
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!"
        })
    )
    
class PostForm(forms.Form):
    # author = forms.CharField(
    #     max_length=60,
    #     widget=forms.TextInput(attrs={
    #         "class": "form-control",
    #         "placeholder": "Your Name"
    #     })
    # )
    title = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Title"
        })
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Blog body"
        })
    )
    categories = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Categories"   
        }
    ))
    
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)