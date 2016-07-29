from PIL import Image
import StringIO
from pytesseract import image_to_string
import urllib

class Captcha:
    '''Helper Method for Tesseract Captcha Solver'''
    @staticmethod
    def threshold(limit=100):
        #Make text more clear by thresholding all pixels above / below this limit to white / black
        # read in colour channels
        img = Image.open('./captchas/captcha.png')
        # resize to make more clearer
        m = 1.5
        img = img.resize((int(img.size[0]*m), int(img.size[1]*m))).convert('RGBA')
        pixdata = img.load()
        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][0] < limit:
                    # make dark color black
                    pixdata[x, y] = (0, 0, 0, 255)
                else:
                    # make light color white
                    pixdata[x, y] = (255, 255, 255, 255)
        img.convert('L')
        img.save('./captchas/threshold_captcha.png')
        return img.convert('L') # convert image to single channel greyscale
    '''
    Tesseract Captcha Solver - solves the original and
    Thresholded versions of the screenshot.
    Uses Tesserace OCR
    '''
    @staticmethod
    def decode_captcha(imageOriginal,imageThreshold):
        return image_to_string(imageOriginal), image_to_string(imageThreshold)

    '''General Method to get the Captcha Picture'''
    @staticmethod
    def get_captcha(driver, data, ddos=False):
        if ddos:
            captcha_xpath = data.get_captcha_image_xpath_ddos()
        else:
            captcha_xpath = data.get_captcha_image_xpath()
        elem = driver.find_element_by_xpath(captcha_xpath)

        #Download Method
        #img.save('./captchas/fullshot.png', 'PNG')
        #src = elem.get_attribute('src')
        #urllib.urlretrieve(src, "./captchas/dolmcaptcha.png")

        #ScreenShot Method
        loc  = elem.location
        size = elem.size
        left  = loc['x']
        top   = loc['y']-100
        width = size['width']
        height = size['height']+100

        #For Alphabay top = 433

        box = (int(left), int(top), int(left+width), int(top+height))
        screenshot = driver.get_screenshot_as_png()
        img = Image.open(StringIO.StringIO(screenshot))
        area = img.crop(box)
        img.save('./captchas/fullshot.png', 'PNG')
        area.save('./captchas/captcha.png', 'PNG')
        return area
    @staticmethod
    def get_captcha_dlm(driver, data, ddos=False):
        if ddos:
            captcha_xpath = data.get_captcha_image_xpath_ddos()
        else:
            captcha_xpath = data.get_captcha_image_xpath()
        elem = driver.find_element_by_xpath(captcha_xpath)

        #Download Method
        #img.save('./captchas/fullshot.png', 'PNG')
        src = elem.get_attribute('src')
        urllib.urlretrieve(src, "./captchas/captcha.png")
        return True

    @staticmethod
    def length_check(captcha, registration_data):
        required_length = int(registration_data.get_captcha_length())
        if len(captcha[0]) > len(captcha[1]):
            input_captcha = captcha[0]
        else:
            input_captcha = captcha[1]
        if len(input_captcha) != required_length:
            print "Incorrect Captcha length, trying again"
            return False
        return input_captcha
        
