#models.py
from django import forms
from .models import Post, Category, Comment
from django_ckeditor_5.widgets import CKEditor5Widget


# choices = Category.objects.values_list('name', flat=True)
# choice_list = [(item, item) for item in choices]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'title_tag', 'author', 'category', 'body', 'snippet', 'header_image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'author'}),
            # 'author': forms.Select(attrs={'class': 'form-control'}),
            # 'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
			'category': forms.Select(attrs={'class': 'form-control'}),
            'body': CKEditor5Widget(attrs={'class': 'form-control django_ckeditor_5'}),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
        }



class EditForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'title_tag', 'body', 'snippet')

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
			#'author': forms.Select(attrs={'class': 'form-control'}),
			'body': CKEditor5Widget(attrs={'class': 'form-control django_ckeditor_5'}),				
			'snippet': forms.Textarea(attrs={'class': 'form-control'}),			
		}


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name','body')

		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'comment-name'}),
			'body': forms.Textarea(attrs={'class': 'form-control'}),	
		}