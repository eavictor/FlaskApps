from sqlalchemy.exc import SQLAlchemyError
from .models_refresh import drop_all_tables, create_all_tables, has_data, fetch_data


def _routine_process():
    drop_all_tables()
    create_all_tables()
    fetch_data()


def initial_update():
    try:
        if not has_data():
            _routine_process()
            return True
        else:
            return True
    except SQLAlchemyError:
        print('ads logic_scheduler.initial_update(): initial update error')
        return False


def weekly_update(app):
    with app.app_context():
        try:
            _routine_process()
        except SQLAlchemyError:
            print('ads logic_scheduler.weekly_update(): weekly update error')