from controllers.scraper import GetFacebookLogo
from models import exceptions as exc
from utils.logger import Logger
import argparse
import json


logger = Logger().get_logger(__name__)


def parse_cli():
 
    msg_example = 'CLI example: python3 --url https://www.facebook.com/...'

    parser = argparse.ArgumentParser()

    parser.add_argument('--url', help='link to Facebook page', default=None)

    parser.add_argument('--proxy', help='proxy adress. Without AUTH: socks5://PROXY_HOST:PROXY_PORT or with AUTH: http://PROXY_USER:PROXY_PASS@PROXY_HOST:PROXY_PORT', default=None)

    try:
        
        args = parser.parse_args()

    except:

        raise exc.NoContent(f"Incorrect page link. {msg_example}")

    if args.url == None:

        raise exc.NoContent(f"You didn't provide a page link. {msg_example}")
    
    if 'facebook' not in args.url:

        raise exc.NoContent(f"Incorrect page link. {msg_example}")
    
    return args



def main():

    try:
        args = parse_cli()

        client = GetFacebookLogo() 

        response = {}

        response['success'] = True
        
        response.update(client.run(args))

    except exc.NoContent as ex:

        logger.error(ex)

        response = {'success': False, 'error': f'{ex}'}

    except Exception as ex:

        logger.critical(ex, exc_info=True)

        response = {'success': False, 'error': f'{ex}'}
    
    return json.dumps(response)



if __name__ == "__main__":

    print (main())

