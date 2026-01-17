from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import schedule, crontab

# -----------------------
# Настройка Django
# -----------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Загружаем настройки Django с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# -----------------------
# Автодискавер задач
# -----------------------
# НЕ импортируем accounts.tasks вручную!
# Celery сам найдет все задачи через @shared_task
app.autodiscover_tasks(['accounts'])

# -----------------------
# Beat расписание
# -----------------------
app.conf.beat_schedule = {
    'delete-inactive-users-every-180-seconds': {
        'task': 'accounts.tasks.delete_inactive_users',
        'schedule': schedule(180),  # каждые 3 минуты для теста
    },
    # Для продакшн:
    # 'delete-inactive-users-daily': {
    #     'task': 'accounts.tasks.delete_inactive_users',
    #     'schedule': crontab(hour=0, minute=0),  # раз в день
    # },
}

# -----------------------
# Отладочная задача
# -----------------------
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
