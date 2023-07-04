from django .contrib.auth import(
    authenticate,
    get_user_model
)
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Posts

User= get_user_model()
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
        return super(LoginForm, self).clean(*args, **kwargs)

class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']



class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))



