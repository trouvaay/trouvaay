from goods.models import Comment
from django.forms import ModelForm, Textarea, TextInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CommentForm(ModelForm):

	class Meta:
		model = Comment
		fields = ['message']
		widgets = {
            'message': TextInput(attrs={'class':'feedback'}),
        }

	def __init__ (self, *args, **kwargs):
		super(CommentForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit','submit'))