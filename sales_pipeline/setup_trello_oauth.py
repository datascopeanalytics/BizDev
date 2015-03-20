import os
import ConfigParser

from trello import util as trello_util
import trello


def get_trello_config():
    trello_ini = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        'conf',
        'trello.ini',
    ))
    config = ConfigParser.ConfigParser()
    config.read(trello_ini)
    return config

def setup_trello_oauth():
    config = get_trello_config()
    if not config.get('trello', 'token'):
        os.environ['TRELLO_API_KEY'] = config.get('trello', 'api_key')
        os.environ['TRELLO_API_SECRET'] = config.get('trello', 'api_secret')
        os.environ['TRELLO_EXPIRATION'] = "never"
        trello_util.create_oauth_token()

        print "^^^^ PUT THAT IN YOUR conf/trello.ini"

if __name__ == '__main__':
    setup_trello_oauth()
