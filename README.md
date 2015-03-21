This project is used to analyze our sales pipeline. For now,
[`trello_export.py`](./sales_pipeline/trello_export.py) just dumps information
from all of our trello cards into a csv.

### getting started

1. `mkvirtualenv bizdev && pip install -r requirements/python`

2. add the following content to `conf/trello.ini`

    ```ini
    [trello]
    api_key        = xxx  # from https://trello.com/app-key
    api_secret     = xxx  # from https://trello.com/app-key
    token          = xxx  # python sales_pipeline/setup_trello_oauth.py
    token_secret   = xxx  # python sales_pipeline/setup_trello_oauth.py
    pipeline_board = xxx  # hash from the sales pipeline trello board url
    ```
