from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
from .models import db
from . import logic_scheduler
from .views import geoip


def init_app(app):
    app.register_blueprint(geoip, url_prefix='/geoip')
    db.init_app(app)
    # let SQLAlchemy knows the current app
    with app.app_context():
        # initial database check
        logic_scheduler.initial_update()
        # register and start monthly update job, perform update on the 2nd day of every month
        scheduler = BackgroundScheduler()
        scheduler.configure(timezone=utc)
        scheduler.add_job(
            func=logic_scheduler.monthly_update, trigger='cron', args=[app], day=3, hour=0, minute=0, second=0,
            id='geoip_monthly_update', replace_existing=True)
        scheduler.start()
