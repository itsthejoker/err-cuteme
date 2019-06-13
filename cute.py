import random

import requests
from errbot import BotPlugin, botcmd


class Cute(BotPlugin):
    cat_api = "http://thecatapi.com/api/images/get?format=json&results_per_page={}"
    pug_api = "http://pugme.herokuapp.com/bomb?count={}"
    fox_api = "https://randomfox.ca/floof/"
    error_img = "https://www.pinclipart.com/picdir/middle/168-1688957_powerpuff-girls-cry-bubbles-clipart.png"

    @botcmd
    def cute(self, msg, args):
        """
        !cute {fox, cat, pug}, or just !cute to get a random picture
        """
        if args:
            self.args = args.split()

        if args:
            if self.args[0] == 'cat':
                return self.get_pic(self.get_cat)
            elif self.args[0] == 'pug':
                return self.get_pic(self.get_pug)
            elif self.args[0] == 'fox':
                return self.get_pic(self.get_fox)

        # if we get here, we either didn't have args or we didn't pass the
        # right args. Just pick an animal at random.
        options = [self.get_cat, self.get_pug, self.get_fox]
        animal = random.choice(options)
        return self.get_pic(animal)

    def get_pic(self, func, extra_args=None):
        try:
            return func(extra_args)
        except:
            return (
                f"Something went horribly wrong and I don't know what!"
                f"\n\n{self.error_img}"
            )

    def get_cat(self, *args):
        # TODO: add picture bomb functionality
        return requests.get(self.cat_api.format(1)).json()[0]['url']

    def get_pug(self, *args):
        return requests.get(self.pug_api.format(1)).json()['pugs'][0]

    def get_fox(self, *args):
        return requests.get(self.fox_api).json().get('image')
