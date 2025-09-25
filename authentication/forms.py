from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re


class CustomUserCreationForm(forms.ModelForm):
    """
    Custom user creation form that allows spaces in usernames
    and provides Arabic labels and help text
    """
    
    # Username field - allows spaces
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل اسم المستخدم'
        }),
        help_text='يمكن أن يحتوي على أحرف وأرقام ومسافات'
    )
    
    # First name field
    first_name = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل الاسم الأول'
        })
    )
    
    # Last name field
    last_name = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل الاسم الأخير'
        })
    )
    
    # Password field
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل كلمة المرور'
        })
    )
    
    # Password confirmation field
    password_confirm = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'أعد إدخال كلمة المرور'
        })
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='هل الحساب نشط'
    )
    
    is_staff = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='هل المستخدم له صلاحية دخول لوحة الإدارة'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'is_active', 'is_staff']

    def clean_username(self):
        """
        Custom validation for username that allows spaces
        """
        username = self.cleaned_data.get('username')
        
        if not username:
            raise ValidationError('اسم المستخدم مطلوب')
        
        # Check if username is only spaces
        if username.strip() == '':
            raise ValidationError('اسم المستخدم لا يمكن أن يكون مسافات فقط')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError('اسم المستخدم موجود بالفعل')
        
        # Check length
        if len(username) > 150:
            raise ValidationError('اسم المستخدم طويل جداً (الحد الأقصى 150 حرف)')
        
        return username
    
    def clean(self):
        """
        Validate password confirmation
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise ValidationError('كلمة المرور وتأكيد كلمة المرور غير متطابقان')
        
        return cleaned_data
    
    def save(self, commit=True):
        """
        Save the user with the validated data
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        return user


class CustomUserEditForm(forms.ModelForm):
    """
    Custom user edit form that allows spaces in usernames
    and provides Arabic labels and help text
    """
    
    # Username field - allows spaces
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل اسم المستخدم'
        }),
        help_text='يمكن أن يحتوي على أحرف وأرقام ومسافات'
    )
    
    # First name field
    first_name = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل الاسم الأول'
        })
    )
    
    # Last name field
    last_name = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل الاسم الأخير'
        })
    )
    
    # Optional password fields
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'كلمة المرور الجديدة'
        }),
        help_text='اتركها فارغة إذا لم ترد تغيير كلمة المرور'
    )
    password_confirm = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'أعد إدخال كلمة المرور الجديدة'
        })
    )
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='هل الحساب نشط'
    )
    
    is_staff = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='هل المستخدم له صلاحية دخول لوحة الإدارة'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'is_active', 'is_staff']

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean_username(self):
        """
        Custom validation for username that allows spaces
        """
        username = self.cleaned_data.get('username')
        
        if not username:
            raise ValidationError('اسم المستخدم مطلوب')
        
        # Check if username is only spaces
        if username.strip() == '':
            raise ValidationError('اسم المستخدم لا يمكن أن يكون مسافات فقط')
        
        # Check if username already exists (exclude current user)
        if self.instance and User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError('اسم المستخدم موجود بالفعل')
        elif not self.instance and User.objects.filter(username=username).exists():
            raise ValidationError('اسم المستخدم موجود بالفعل')
        
        # Check length
        if len(username) > 150:
            raise ValidationError('اسم المستخدم طويل جداً (الحد الأقصى 150 حرف)')
        
        return username
    
    def clean(self):
        """
        Validate password confirmation if password is provided
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password:  # Only validate if password is provided
            if password != password_confirm:
                raise ValidationError('كلمة المرور وتأكيد كلمة المرور غير متطابقان')
        
        return cleaned_data
    
    def save(self, commit=True):
        """
        Save the user with the validated data
        """
        user = super().save(commit=False)
        
        # Only update password if provided
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        return user