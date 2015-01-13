from django import forms
from pagedown.widgets import PagedownWidget
from models import Post, Comment

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		exclude = ['author', 'slug']

class CommentForm(forms.ModelForm):
	text = forms.CharField( widget=PagedownWidget(show_preview=True, template="default.html"))
	class Meta:
		model = Comment
		exclude = ['post']
