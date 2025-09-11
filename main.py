from scraper import get_lines, get_status
from db import connect_db, insert_data, update_status

if __name__ == "__main__":
    if connect_db():
        insert_data(get_lines())
        update_status(get_status())
