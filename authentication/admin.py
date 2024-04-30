from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django import forms

User = get_user_model()

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

    def save(self,commit=True):
        # Save the provided password in hashed format
        try:
            if str(self.instance.id)=='None':
                user = super(UserCreationForm, self).save(commit=False)
                user.set_password(self.cleaned_data["password"])
                if commit:
                    user.save()
                return user
            else:
                user = super(UserCreationForm, self).save(commit=False)
                return user
        except:
            user = super(UserCreationForm, self).save(commit=False)
            return user

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display= ['email','username','is_active']
    search_fields= ['email']
    list_filter= ['email']
    list_per_page = 10
    list_display_links = list_display
    form = UserCreationForm

    
admin.site.unregister(Group)