from django import forms
from pagedown.widgets import PagedownWidget
from crispy_forms.helper import FormHelper
from .models import Post

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget)
    helper = FormHelper()
    helper.form_tag = False
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-3"
    helper.field_class = "col-lg-9"
    
    class Meta:
        model = Post
        fields = [
            'title',
            'body',
            'image',
            'author',
            'draft',
            'publish',
        ]

        
