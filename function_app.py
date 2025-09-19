import logging
import azure.functions as func

from src.scraper import get_lines, get_status
from src.db import connect_db, insert_data, update_status


def setup_db():
    """
    Run once to initialize DB with lines.
    (Manually executed, not by Function App)
    """
    if connect_db():
        insert_data(get_lines())
        logging.info("DB setup completed with initial line data.")


def run_status_update():
    """
    Runs every 10 minutes (Azure Function).
    Only updates status of existing lines.
    """
    if connect_db():
        update_status(get_status())
        logging.info("DB status updated successfully.")


# Azure Function App instance
app = func.FunctionApp()

@app.timer_trigger(schedule="0 */10 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.warning('The timer is past due!')

    logging.info('Python timer trigger function started.')
    run_status_update()
    logging.info('Python timer trigger function finished.')