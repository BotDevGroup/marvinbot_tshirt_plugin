# -*- coding: utf-8 -*-

from marvinbot.utils import localized_date, get_message
from marvinbot.handlers import CommandHandler, CallbackQueryHandler
from marvinbot.plugins import Plugin
from marvinbot.models import User

import logging
import ctypes
import time
import re
import textwrap

from io import BytesIO

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import os
import inspect

log = logging.getLogger(__name__)


class MarvinBotTShirtPlugin(Plugin):
    def __init__(self):
        super(MarvinBotTShirtPlugin, self).__init__('marvinbot_tshirt_plugin')
        self.bot = None
        self.path = os.path.dirname(inspect.getfile(self.__class__))

    def get_default_config(self):
        return {
            'short_name': self.name,
            'enabled': True
        }

    def configure(self, config):
        self.config = config
        pass

    def setup_handlers(self, adapter):
        self.bot = adapter.bot
        self.add_handler(CommandHandler('tshirt', self.on_tshirt_command, command_description='T-Shirt Generator')
            .add_argument('--g', help='Girl T-Shirt', action='store_true')
            .add_argument('--b', help='Boy T-shirt', action='store_true')
        )
 
    def setup_schedules(self, adapter):
        pass

    def make_tshirt(self, text, gender="boy"):
        text = text.upper()

        lenght = 37
        size = 40
        fillcolor = "white"
        width = 160 if "boy" == gender else 50

        text = text[:lenght]
        
        font = ImageFont.truetype("{}/OpenSansEmoji.ttf".format(self.path), int(size))
        original = Image.open("{}/{}.jpg".format(self.path, gender))
        draw = ImageDraw.Draw(original)

        imageW, imageH = original.size
        charW, charH = draw.textsize(text[0], font)

        text = "\n".join(textwrap.wrap(text, width=int(width / charW)))

        textW, textH = draw.multiline_textsize(text, font)
        
        x = (imageW-textW)/2
        y = 80

        draw.multiline_text((x,y), text, font=font, fill=fillcolor, align='center')

        img = BytesIO()
        img.seek(0)
        original.save(img, format='PNG')

        return img

    def on_tshirt_command(self, update, *args, **kwargs):
        message = get_message(update)

        gender = "girl" if kwargs.get('g') else "boy"

        text = " ".join(message.text.split(" ")[1:])
        text = text.replace("--","—").replace("—g","").replace("—b","")

        if text:
            try:
                img = BytesIO()
                img.seek(0)
                img = self.make_tshirt(text=text, gender=gender)
                img.seek(0)
                self.adapter.bot.sendPhoto(chat_id=message.chat_id, photo=img) 
            except Exception as err:
                log.error("T-Shirt - make error: {}".format(err))
        else:
            msg = "❌ errr!!! where is the message?"
            self.adapter.bot.sendMessage(chat_id=message.chat_id, text=msg, parse_mode='Markdown')