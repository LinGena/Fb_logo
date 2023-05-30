from controllers.scraper import GetFacebookLogo
from models import exceptions as exc
from utils.logger import Logger
import os


logger = Logger().get_logger(__name__)


def get_tasks():

    filename = 'input.txt'

    tasks = []

    if os.path.exists(filename):

        with open(filename, "r", encoding='utf8') as file:

            tasks = file.read().splitlines()
   
    return tasks


def worker(client, url):

    try:

        client.run(url)

    except exc.NoContent as ex:

        logger.error(ex)

    except Exception as ex:

        logger.critical(ex, exc_info=True)


def main():

    client = GetFacebookLogo() 

    tasks = get_tasks()

    if len(tasks) > 0:

        for url in tasks:

            logger.info(f'Getting logo from {url}')

            worker(client, url)

    else:

        logger.info('There are no links in input.txt file')



           
if __name__ == "__main__":
    main()



