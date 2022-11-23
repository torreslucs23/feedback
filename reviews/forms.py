from django import forms

class ReviewForm(forms.Form):
    user_name = forms.CharField(label= "Your name", max_length = 100, error_messages={
        "required": "you name must not be empty",
        "Max_length": "Please enter a shorter name"    })