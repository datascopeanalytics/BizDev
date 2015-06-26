import os
import ConfigParser
import csv
import sys
import warnings
import pprint
import simplejson as json
from pprint import pprint
import datetime, dateutil.parser

from setup_trello_oauth import get_trello_config
from trello import util as trello_util
import trello


#get dollar label from card
def get_dollar_amount(card):
    dollar_amount = 'na'
    for label in card.labels:
        if ('$' in str(label)):
            dollar_amount = parse_amount(str(label))


#turn <Label $50k - $250k> into $50k-$250k
def parse_amount(label):
    label = label.replace("<Label ", "")
    label = label.replace("k>", "k")
    label = label.replace(" ", "")
    return label


#parse action date
def parse_date(date_string):
    d = dateutil.parser.parse(date_string)
    return d.strftime('%Y-%m-%d')


#write card data to text file in json
def write_cards(cards):
    file_name = 'card_stages.txt'
    with open(file_name, 'w') as f:
        json.dump(cards, f)


#get cards & actions with py_trello
def get_card_list_actions():
    # get the client to login
    config = get_trello_config()
    client = trello.TrelloClient(
        api_key=config.get('trello', 'api_key'),
        api_secret=config.get('trello', 'api_secret'),
        token=config.get('trello', 'token'),
        token_secret=config.get('trello', 'token_secret'),
    )

    # get the board associated with our sales pipeline
    board = client.get_board(config.get('trello', 'pipeline_board'))


    action_filters = ['updateCard', 'createCard']
    cards = {}

    for l in board.open_lists():
        for card in l.list_cards():
            dollar_amount = get_dollar_amount(card)
            cards[card.id] = {'name':card.name,'amount':dollar_amount,'stages':[]}

            #fetch update and create actions for all cards
            card.fetch_actions(action_filters)

            #append list-changing actions to corresponding card
            for action in card.actions:
                if (action['type'] == 'createCard'):
                    date = parse_date(str(action['date']))
                    action_type = action['type']
                    listAfter = action['data']['list']['name']
                    listBefore = "none"
                    cards[card.id]['stages'].append({'listBefore':listBefore, 'listAfter':listAfter, 'date':date, 'type':action_type})
                elif (action['type'] == 'updateCard' and 'listAfter' in action['data']):
                    date = parse_date(str(action['date']))
                    action_type = action['type']
                    listAfter = action['data']['listAfter']['name']
                    listBefore = action['data']['listBefore']['name']
                    cards[card.id]['stages'].append({'listBefore':listBefore, 'listAfter':listAfter, 'date':date, 'type':action_type})
            # print len(cards)
            pprint(cards[card.id])
    #write_cards(cards)


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    get_card_list_actions()
