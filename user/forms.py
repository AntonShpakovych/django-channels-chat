from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CreateUserForm(UserCreationForm):
    photo = forms.ImageField()

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("photo",)

    def save(self, commit=True):
        user = super().save(commit=False)
        print(self.cleaned_data)
        user.profile_image = self.cleaned_data["photo"]
        if commit:
            user.save()
        return user
