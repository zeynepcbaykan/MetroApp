import datetime
import logging
import azure.functions as func
from src.db import connect_db, update_status
from src.scraper import get_status

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('Timer is past due!')

    logging.info(f'Metro status update started at: {utc_timestamp}')

    try:
        if connect_db():
            statuses = get_status()
            update_status(statuses)
            logging.info('Metro status update completed successfully')
        else:
            logging.error('Database connection failed')
    except Exception as e:
        logging.error(f'Error during metro status update: {str(e)}')
        raise
