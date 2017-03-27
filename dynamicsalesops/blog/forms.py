from django import forms
from .models import BlogPageComment

class CommentForm(forms.ModelForm):
	
	class Meta:
		model = BlogPageComment
		fields = ('comment_author', 'text',)

