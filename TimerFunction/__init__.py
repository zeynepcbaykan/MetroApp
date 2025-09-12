import datetime
import logging
import azure.functions as func

from scraper import get_lines, get_status
from db import connect_db, insert_data, update_status


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    if connect_db():

        insert_data(get_lines())

        update_status(get_status())

        logging.info("Metro data updated successfully.")
