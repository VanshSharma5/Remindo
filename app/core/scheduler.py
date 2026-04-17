from collections import defaultdict

from apscheduler.schedulers.background import BackgroundScheduler

from app.core.db import SessionLocal
from app.services.task_service import get_next_day_tasks
from app.services.email import send_email
from app.core.config import settings


scheduler = BackgroundScheduler()


def send_daily_emails():
    db = SessionLocal()

    try:
        tasks = get_next_day_tasks(db)

        user_map = defaultdict(list)

        for task in tasks:
            user_map[task.user.email].append(task)
        for email, tasks in user_map.items():
            content = "\n".join(
                [f"- {t.title} at {t.scheduled_at}" for t in tasks]
            )
            # print(email, "Your Tasks for Tomorrow", content)
            
            send_email(email, "Your Tasks for Tomorrow", content)

    finally:
        db.close()


def dummy():
    send_daily_emails()

def start_scheduler():
    scheduler.add_job(send_daily_emails, "cron", hour=settings.CRON_HOUR, minute=settings.CRON_MINUTE)
    scheduler.start()