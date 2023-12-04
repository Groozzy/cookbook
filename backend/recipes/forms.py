from django import forms

from recipes.models import Tag


class TagForm(forms.ModelForm):
    color = forms.CharField(
        label='Цвет',
        max_length=7,
        widget=forms.TextInput(attrs={'type': 'color'})
    )

    class Meta:
        model = Tag
        fields = '__all__'
