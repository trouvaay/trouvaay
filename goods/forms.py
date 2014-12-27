from goods.models import Comment
from django.forms import ModelForm, Textarea, TextInput

class CommentForm(ModelForm):

	class Meta:
		model = Comment
		fields = ['message']
		widgets = {
            'message': TextInput(attrs={'class':'feedback'}),
        }