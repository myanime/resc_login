from django import forms
import modifyDAO

class LoginForm(forms.Form):
    modify_data = modifyDAO.ModifyDAO()
    sites = modify_data.get_sites()
    SITES = []
    for site in sites:
        SITES.append((site, site))
    SITES = tuple(SITES)
    dropdown_list = forms.ChoiceField(choices=SITES)
