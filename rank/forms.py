from django import forms


class DayForm(forms.Form):
    day = forms.IntegerField()


    def clean_day(self):
        day = self.cleaned_data['day']
        if day < 1:
            raise forms.ValidationError('Please enter a positive number.') 
