from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.routes.repo import sync_commits

from app.database.db import get_db
from app.models.repo import repository


def start_scheduler():

    scheduler = BackgroundScheduler()

    scheduler.add_job(sync_all_repos , "interval" ,minutes = 3 , next_run_time=datetime.now())

    scheduler.start()
    print("scheduler start")


def sync_all_repos():
    db = next(get_db())
    repos = db.query(repository).all()

    for repo in repos:

        try:
            sync_commits(repo_id=repo.id , db = db)

        except Exception as e:
            print("the error is ",e)

