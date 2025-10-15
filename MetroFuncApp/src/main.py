import sys
from src.scraper import get_lines, get_status
from src.db import connect_db, insert_data, update_status


def setup_db():
    """
    Run once to initialize DB with lines.
    """
    if connect_db():
        insert_data(get_lines())
        print("DB setup completed with initial line data.")


def run_status_update():
    """
    Runs every 10 minutes (Azure Function).
    Only updates status of existing lines.
    """
    if connect_db():
        update_status(get_status())


if __name__ == "__main__":
    # If you run "python main.py setup" from the terminal -> setup_db()
    # If you just run "python main.py" -> run_status_update()
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_db()
    else:
        run_status_update()