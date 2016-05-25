from sqlalchemy.exc import SQLAlchemyError
from .models_refresh import drop_all_tables, create_all_tables, download_csv, delete_csv, read_csv_and_update_database,\
    has_data


def _routine_process():
    drop_all_tables()
    create_all_tables()
    download_csv()
    read_csv_and_update_database()
    delete_csv()


# run once when service start
def initial_update():
    try:
        if not has_data():
            _routine_process()
            return True
        else:
            return True
    except ConnectionError or FileNotFoundError or SQLAlchemyError:
        print('geoip logic_scheduler.initial_update(): initial update error')
        return False


def monthly_update(app):
    with app.app_context():
        try:
            _routine_process()
        except ConnectionError or FileNotFoundError or SQLAlchemyError:
            print('geoip logic_scheduler.monthly_update(): monthly update error')
