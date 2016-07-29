Version 1.0: 14hrs
- Main code

Version 1.1: 6hrs
- 2captcha solver implemented
- login method broken
- rescator specific methods removed
- database schema:
    fields:
        checkboxes
        usernames
        passwords
        custom - can enter custom string to be entered into the custom xpath
- dreammarket_document.json demonstrates a bare minimum schema. You can have more
but this is what is needed to generate a login.

Version 1.2: 3.5hrs
- Flagger - sending reminder about case to improve captcha solve rate
- setup_proxy() implemented
- refactored Register and Logon classes to RegisterLogon class
- fixed login method
- removed all rescator specific methods

Version 1.3 0hrs
- Web interface

Version 1.4 6hrs
- Adding alphabay login support (No support for Alphabay registration)
- DDOs Captcha support
- Improved web interface
	http://localhost:8000/
	http://localhost:8000/modify_database
	http://localhost:8000/login_register/login
	http://localhost:8000/login_register/register
- improved proxy support (setup_proxy())
- somewhat improved error handling

Version 1.5 2hrs
- PhantomJS
- new method added: captcha_methods.Captcha.get_captcha_dlm
	This downloads the captcha directly. It is being used for Alphabay, the others use 
	the original screenshot method
- Screenshot Captcha method modified to make it captcha a larger area (PhantomJS reacts differently to chrome
  but the new method should work for both browsers.
- in regards to the  --jsonArray I left it out. It seems to work fine here without it, the documents are actually 
  not a jsonarray, so I cant figgure out why it would complain. But if it works for you, feel free to add it in
- tested the login methods, I will test the register methods over the weekend.
- Cleaned up the code, but lost the changes. Will clean it up a bit again and send you a new version over the weekend
- total time worke = 31.5hrs *5$/hr = $157.50


