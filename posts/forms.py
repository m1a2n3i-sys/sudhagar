from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post


class PostForm(forms.ModelForm):
    """
    A ModelForm auto-generates form fields from the Post model.
    We only expose the fields a user should be able to fill in.
    """
    class Meta:
        model = Post
        fields = ['title', 'caption', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Give your post a title',
            }),
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a caption...',
                'rows': 3,
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        # Custom validation: strip whitespace and reject empty titles
        title = self.cleaned_data['title'].strip()
        if not title:
            raise forms.ValidationError('Title cannot be empty or just spaces.')
        return title

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Limit uploads to 5 MB
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file too large ( > 5MB ).')
            # Only allow common image types
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            if not any(image.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError('Unsupported file type. Use JPG, PNG, GIF or WEBP.')
        return image


class RegisterForm(UserCreationForm):
    """
    Extends Django's built-in UserCreationForm to also collect an email
    address and apply Bootstrap CSS classes to every field.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email
