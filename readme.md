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

Version 1.4 - Comming Soon (1-2 days)
- Adding alphabay and DDOs Captcha support
