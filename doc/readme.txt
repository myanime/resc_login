Here is the Generic Logon/Register Script it is structured as follows:

register_logon.py - This is the main entry point, it contains the database connector

These Classes are in the register_logon package:

    The Data Access Objects for interacting with mongoDB:
    registerDAO.py
    loginDAO.py

    register_methods.py - Collection of functions used when Registering
            verify_login_creation
            click_checkboxes
            click_submit
            input_fields
            input_captcha_decaptcha - Yet to be implemented
            input_captcha_tesseract - Uses OCR to crack the captcha

            Some of these functions are Rescator/Site specific. To get arround this problem, we would 
            need to add the following fields to the database:
                    captcha_length - standard captcha length
                    verification_string - standard string that appears on page in event of sucessfull/unsucessfull logon


    login_methods.py - Pretty much the same as the register_methods. I probably should have written these two files as one 
                       class, but at least the current arrangement is easy to understand

    capcha_methods.py - Methods used for solving the Captchas

The Basic Flow of the program is as follows:

1. Get Database Connection
2. Create login and register objects for interacting with the database
3. If Registering, functions from the Register class will be used to input the fields, click the checkboxes, etc.
4. Data will be pulled from the database using the registration_data object
3a, 4a. If Loging on, the functions from the Login class will be used

The script works well, but it does need some work. The following needs to be added/modified:

1. Error Handling/Testing. This is actually a pretty big job could take a few hours, so I thought I would give you this version first
and see if it fits what you are trying to accomplish before working on this.
2. Database schema needs to be slightly modified including the following fields:
	captcha_length
	verification_string

	This is not such a big job, but I left it like it is so that you can get a feel for how the script is dependant on 
	the site that it is scraping. The more sites that the script will have to handle, the more more methods will have to 
	be added. For example if a site has a input field for your birthday, a method would have to be added, and a corresponding 
	entry to the db. Then in the main method you would end up doing something like this, including all the methods for the
	different cases. If on a paticular site a birthday doesnt exist, that method would just return none:

	Register.input_fields()
	Register.input_birthday()
	Register.input_radiobutton()

	I made one change to the schema for rescator, I added the field "check_boxes" to the registration section 
 	"check_boxes": "//*[@id=\"login_form\"]/label[7]/input"
	Basically I should go and add a section for captcha_length and verification_string, and make sure the errors 
	are being caught.

In regards to the captcha solver, I had been logging in all day without a problem, but eventually my luck ran out, and
Mickey mouse was banned. Recator bans you after 10 failed log in attempts. This is actually less of a problem than it
sounds - the captcha solver can take sometimes 30 tries to crack the captcha, but rescator only sees the attempts where
the captch length is = 5. The OCR engine usually cracks the captcha in about 2-3 tries, if it gets the length correct.


Let me know your thoughts, and what you would like me to focus on.

Ryan
