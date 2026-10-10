from django import forms

from .models import ContactRequest, Service


class QuickQuoteForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسمك الكامل'}),
        label='الاسم الكامل',
    )
    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
        label='رقم الهاتف',
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
        label='البريد الإلكتروني',
    )
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        empty_label='اختر الخدمة المطلوبة',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='الخدمة',
        required=False,
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'اكتب رسالتك هنا...'}),
        label='الرسالة',
    )


class ContactForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        empty_label='اختر الخدمة المطلوبة',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='الخدمة المطلوبة',
        required=False,
    )

    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم الكامل'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'اكتب رسالتك هنا...'}),
        }
        labels = {
            'name': 'الاسم الكامل',
            'phone': 'رقم الهاتف',
            'email': 'البريد الإلكتروني',
            'message': 'الرسالة',
        }
