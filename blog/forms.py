from django import forms
from models import Post, Comment
from django_markdown.widgets import MarkdownWidget

class PostForm(forms.ModelForm):
	text = forms.CharField(widget=MarkdownWidget())
	class Meta:
		model = Post
		exclude = ['author', 'slug']

class CommentForm(forms.ModelForm):
	#text = forms.CharField( widget=PagedownWidget(show_preview=True, template="default.html"))
	text = forms.CharField(widget=MarkdownWidget())
	class Meta:
		model = Comment
		exclude = ['post']
