from django.shortcuts import render
import modifyDAO
from .forms import ModifyMongoForm

def add_to_database(request):
    if request.method == 'POST':
        form = ModifyMongoForm(request.POST)
        username =  form.data['username']
        password = form.data['password']
        site = form.data['site']
        modify_data = modifyDAO.ModifyDAO(site)
        modify_data.set_registration_username_xpath(username)
        modify_data.set_registration_password_xpath(password)
        updated = "Sucessfully Updated"
        return render(request, 'modify_database/index.html', {"form": form, "updated_message":updated})
    else:
        form = ModifyMongoForm()

    return render(request,'modify_database/index.html', {"form":form})
