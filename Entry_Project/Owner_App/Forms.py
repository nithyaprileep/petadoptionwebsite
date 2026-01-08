from django import forms
from Pets_App.models import Pet, PetBreed

class PetForm(forms.ModelForm):

    new_breed = forms.CharField(
        required=False,
        label="New Breed (optional)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new breed if not listed'
        })
    )

    class Meta:
        model = Pet
        exclude = ['owner', 'approval_status']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'breed': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'colour': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'availability': forms.Select(attrs={'class': 'form-select'}),
        }

    def save(self, commit=True):
        pet = super().save(commit=False)

        new_breed = self.cleaned_data.get('new_breed')
        if new_breed:
            breed, created = PetBreed.objects.get_or_create(
                name=new_breed
            )
            pet.breed = breed

        if commit:
            pet.save()
            self.save_m2m()

        return pet
