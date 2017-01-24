import random
import string
import time

from wheezy.captcha.image import captcha

from wheezy.captcha.image import background
from wheezy.captcha.image import curve
from wheezy.captcha.image import noise
from wheezy.captcha.image import smooth
from wheezy.captcha.image import text

from wheezy.captcha.image import offset
from wheezy.captcha.image import rotate
from wheezy.captcha.image import warp

IMAGE_PATH = "./card/lobby/static/images/"
URL_PATH = "static/images/"

class CaptchaManager(object):

    def generator_image(self, user_id):
        captcha_image = captcha(drawings=[
            background(),
            text(fonts=[
                'card/lobby/static/fonts/CourierNew-Bold.ttf',
                'card/lobby/static/fonts/LiberationMono-Bold.ttf'],
                drawings=[
                    warp(),
                    rotate(),
                    offset()
                ]),
            curve(),
            noise(),
            smooth()
        ], width=200, height=75)

        code_list = random.sample(string.digits, 4)
        image = captcha_image(code_list)
        code = ''.join(code_list)
        image_name = str(int(time.time())) + str(user_id) + ".png"
        image_path = IMAGE_PATH + image_name
        url_path = URL_PATH + image_name
        image.save(image_path, 'PNG', quality=75)

        return code, url_path