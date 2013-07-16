from django import forms
from challenge import models as db


class ProfileForm(forms.ModelForm):
    class Meta:
        model = db.Challenge_User
        fields = ['bio', 'homepage_url']
        widgets = {
          'bio': forms.Textarea(attrs={'placeholder': 'please add a bio'}),
        }

    username = forms.RegexField(
        widget=forms.TextInput(attrs={'placeholder': 'username'}),
        label="Username", max_length=30, regex=r'^[a-zA-Z0-9]{3,30}$',
        help_text="Required. Letters and digits only and 3-30 characters.",
        error_messages={'invalid': ("Please enter letters and digits only.  "
        "Minimum 3 characters and max 30.")})


    def clean_username(self):
        username = self.data.get('username')
        if not self.instance.added_username:
            if db.User.objects.filter(username__iexact=username).count():
                raise forms.ValidationError("Username is taken")
        return username

    def save(self):
        model = super(ProfileForm, self).save(commit=False)
        if not model.added_username:
            model.added_username = True
            user = model.user
            user.username = self.cleaned_data.get('username')
            user.save()
        model.save()


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = db.Challenge
        fields = ["title", "content", "category"]
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'please add content'}),
            'title': forms.TextInput(attrs={'placeholder': 'please add a title'})
        }

class ClaimForm(forms.ModelForm):
    class Meta:
        model = db.Claim
        fields = ['content', 'proof_url', 'project_url']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'please add content'}),
        }
