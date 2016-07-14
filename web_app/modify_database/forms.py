from django import forms
import modifyDAO

class ModifyMongoForm(forms.Form):
    modify_data = modifyDAO.ModifyDAO()
    sites = modify_data.get_sites()
    SITES = []
    for site in sites:
        SITES.append((site, site))
    SITES = tuple(SITES)

    site = forms.ChoiceField(choices=SITES)
    username = forms.CharField(label="Username xpath", max_length=100)
    password = forms.CharField(label="Password xpath", max_length=100)
