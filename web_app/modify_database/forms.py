from django import forms
import modifyDAO

class ModifyMongoForm(forms.Form):
    modify_data = modifyDAO.ModifyDAO()
    sites = modify_data.get_sites()
    site1 = sites[0]
    site2 = sites[1]
    site3 = sites[2]

    SITES = (
        (site1, site1),
        (site2, site2),
        (site3, site3),
    )
    site = forms.ChoiceField(choices=SITES)
    username = forms.CharField(label="Username xpath", max_length=100)
    password = forms.CharField(label="Password xpath", max_length=100)
