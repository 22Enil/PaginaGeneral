from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import PerfilUsuario


User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    biografia = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    imagen_perfil = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'phone_number',
            'biografia',
            'imagen_perfil',
        )

    def save(self, commit=True):
        # Save the User first
        user = super().save(commit=commit)

        # Then create/update the PerfilUsuario linked to this user
        phone = self.cleaned_data.get('phone_number')
        bio = self.cleaned_data.get('biografia')
        imagen = self.cleaned_data.get('imagen_perfil')

        # Use get_or_create to avoid duplicate profile if any
        perfil, created = PerfilUsuario.objects.get_or_create(usuario=user)
        if phone:
            perfil.phone_number = phone
        if bio:
            perfil.biografia = bio
        if imagen:
            perfil.imagen_perfil = imagen
        perfil.save()

        return user


class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label='Usuario')
    email = forms.EmailField(required=True, label='Correo electrónico')
    first_name = forms.CharField(max_length=150, required=False, label='Nombre')
    last_name = forms.CharField(max_length=150, required=False, label='Apellido')

    class Meta:
        model = PerfilUsuario
        fields = ('phone_number', 'biografia', 'imagen_perfil')

    # imagen_perfil uses the default ModelForm widget (ClearableFileInput).
    # We avoid forcing a custom widget here to keep the default Django behavior
    # (shows existing filename, clear checkbox, and change/select controls).

    def __init__(self, *args, **kwargs):
        # optionally receive a user argument to prefill
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = getattr(user, 'first_name', '')
            self.fields['last_name'].initial = getattr(user, 'last_name', '')
            # prefill username and email from the linked User
            self.fields['username'].initial = getattr(user, 'username', '')
            self.fields['email'].initial = getattr(user, 'email', '')

        # Apply Bootstrap classes to widgets for consistent styling in templates
        widget_map = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Una breve biografía'}),
            'imagen_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        for name, widget in widget_map.items():
            if name in self.fields:
                self.fields[name].widget = widget

    def save(self, user=None, commit=True):
        perfil = super().save(commit=False)
        # update user fields if provided
        if user is not None:
            # username and email are editable here as requested
            username = self.cleaned_data.get('username')
            email = self.cleaned_data.get('email')
            first = self.cleaned_data.get('first_name')
            last = self.cleaned_data.get('last_name')
            if username is not None:
                user.username = username
            if email is not None:
                user.email = email
            if first is not None:
                user.first_name = first
            if last is not None:
                user.last_name = last
            if commit:
                user.save()

        if commit:
            perfil.save()

        return perfil

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # if instance has a linked user, exclude it from uniqueness check
        usuario_actual = None
        if self.instance and getattr(self.instance, 'usuario', None):
            usuario_actual = getattr(self.instance, 'usuario')

        qs = User.objects.filter(username=username)
        if usuario_actual is not None:
            qs = qs.exclude(pk=usuario_actual.pk)

        if qs.exists():
            raise ValidationError('El nombre de usuario ya está en uso por otra cuenta.')

        return username
