from errbot import BotPlugin, botcmd
import random
import requests
from xmljson import badgerfish as bf
from json import dumps
from json import loads
from xml.etree.ElementTree import fromstring
from addict import Dict


class Cute(BotPlugin):
    cat_api = "http://thecatapi.com/api/images/get?format=xml&results_per_page={}"
    pug_api = "http://pugme.herokuapp.com/bomb?count={}"
    dog_api = "https://api.thedogapi.co.uk/v2/dog.php?limit={}"

    @botcmd
    def cute(self, msg, args):
        if args:
            self.args = args.split()

        if args:
            if self.args[0] == 'cat':
                return self.get_cat()
            elif self.args[0] == 'pug':
                return self.get_pug()
            elif self.args[0] == 'dog':
                return self.get_dog()

        # if we get here, we either didn't have args or we didn't pass the
        # right args. Just pick an animal at random.
        options = [self.get_cat, self.get_pug, self.get_dog]
        animal = random.choice(options)
        return animal()

    def get_cat(self):
        # TODO: add picture bomb functionality
        count = 1
        result = requests.get(self.cat_api.format(count))
        # is probably a lot more painful than it needs to be, but xml sucks
        json_data = Dict(loads(dumps(bf.data(fromstring(result.content)))))
        return json_data.response.data.images.image.url['$']


    def get_pug(self):
        result = requests.get(self.pug_api)
        return result.json()['pugs'][0]

    def get_dog(self):
        count = 1
        result = requests.get(self.dog_api.format(count))
        json_data = Dict(result.json())
        return json_data.data[0].url
