from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
from . import logic_scheduler
from .models import db
from .views import ads


def init_app(app):
    app.register_blueprint(ads, url_prefix='/ads')
    # let SQLAlchemy knows the current app
    db.init_app(app)
    with app.app_context():
        # initial database check
        logic_scheduler.initial_update()
        # register and start weekly update job, perform update on every sunday
        scheduler = BackgroundScheduler()
        scheduler.configure(timezone=utc)
        scheduler.add_job(
            func=logic_scheduler.weekly_update, trigger='cron', args=[app], day_of_week=6, hour=12, minute=0, second=0,
            id='ads_weekly_update', replace_existing=True
        )
        scheduler.start()