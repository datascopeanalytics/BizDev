import os
import ConfigParser
import csv
import sys
import warnings

from trello import util as trello_util
import trello

from setup_trello_oauth import get_trello_config



def write_card_data():

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

    # set up our output writing
    writer = csv.writer(sys.stdout)
    writer.writerow([

        # can get these directly from the API
        'id', 'url', 'opportunity', 'first contact', 'last update',

        # can infer this directly from the API
        'company name',  # from the card name
        'outcome',       # from the list name

        # stuff we can fill in on our own?
        'proposal cost',
        'proposal timeline',

        # stuff that Whitney can get for us
        'client number of employees',
        'approximate annual revenues',
        'client wikipedia page (if exists)',
        'client main contact (linkedin)',
    ])

    # go through all of the lists to determine the outcome of different engagement
    for l in board.open_lists():
        for card in l.list_cards():
            card.fetch()
            sys.stderr.write("%s\n" % card.name)
            writer.writerow([
                card.id,
                card.url,
                card.name,
                card.create_date,
                card.date_last_activity,
                card.name.split(':', 1)[0],
                card.trello_list.name,
            ])


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    write_card_data()
