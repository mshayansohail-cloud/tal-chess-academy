from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Your name"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-input", "placeholder": "your@email.com"})
    )
    phone = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Phone (optional)"}),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-input", "placeholder": "Tell us about your chess goals…", "rows": 5}
        )
    )
