from utils.logger import Logger
from models import exceptions as exc
import json
import cfscrape
import requests
import os
from pathlib import Path
from urllib.parse import urlparse


class GetFacebookLogo():
    def __init__(self) -> None:
        self._loger = Logger().get_logger(__name__)

        self.result_dir = 'output'

        self.check_dir(self.result_dir)


    def get_logo_url(self, src) -> str:

        cut_phrase = '"profile_photo":{'

        if cut_phrase in src:

            cut_dict = '{' + src.split(cut_phrase)[1].split('},')[0] + '}'

            result = json.loads(cut_dict)

            res = result['url']

            return res
        
        raise exc.NoContent("Not received url of Profile photo")
    

    def get_logo_image_url(self, src: str) -> str:

        cut_phrase = '"image":{"uri":"'

        if cut_phrase in src:

            cut = src.split(cut_phrase)[1].split('"')[0]

            cut = cut.replace('\\','')

            return cut

        raise exc.NoContent("Not received image url") 


    def get_content(self, link: str) -> str:

        scraper = cfscrape.create_scraper() 

        scraped_data = scraper.get(url=link)

        res = scraped_data.text

        return res


    def check_dir(self, dir):

        if not Path(dir).is_dir():

            os.mkdir(dir, mode=0o777, dir_fd=None)


    def get_image_name(self, image_path):

        nameImg = image_path.split("/")[-1]

        if '?' in nameImg:

            nameImg = nameImg.split('?')[0]

        return nameImg
    

    def parse_fb_link(self, fb_link: str) -> str:

        parse = urlparse(fb_link).path

        parse = parse.split('/')[1]

        return parse
    

    def get_output_dir(self, fb_link: str) -> str:

        parse = self.parse_fb_link(fb_link)

        if parse == 'profile.php':

            parse = urlparse(fb_link).query

            if 'id=' in parse:

                parse = parse.split('id=')[1]

                if '&' in parse:

                    parse = parse.split('&')[0]

        res = self.result_dir + '/' + parse

        self.check_dir(res)

        return res


    def copy_logo(self, image_path: str, fb_link: str):

        image = requests.get(image_path)

        name_img = self.get_image_name(image_path)

        dir = self.get_output_dir(fb_link)

        filename_to = dir + '/' + name_img

        with open(filename_to, 'wb') as file:

            file.write (image.content)
        
        self._loger.debug(f'Copy logo to {filename_to}')


    def check_fb_link(self, fb_link: str) -> str:

        parse = self.parse_fb_link(fb_link)

        link = 'https://www.facebook.com/' + parse + '/'

        if parse != 'profile.php':

            albums = ['photos_albums', 'photos']
        
        else:

            link = fb_link

            albums = ['&sk=photos']

        for album in albums:

            try:

                url = link + album

                src = self.get_content(url)

                logo = self.get_logo_url(src)

                return logo

            except exc.NoContent as ex:

                continue

        raise exc.NoContent('Not received url of Profile photo')


    def run(self, link: str):

        url = self.check_fb_link(link)

        src = self.get_content(url)

        logo_url = self.get_logo_image_url(src)

        self.copy_logo(logo_url, link)





   
