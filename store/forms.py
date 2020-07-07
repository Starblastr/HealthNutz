from django import forms
from .models import Image, Comment
class ImageUpload(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('file',)
        def save(self):
            image = super(ImageUpload, self).save()
            return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class UserCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)

