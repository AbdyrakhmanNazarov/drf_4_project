from celery import shared_task
from django.utils.timezone import now, timedelta
from accounts.models import User
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def delete_inactive_users(self):
    """
    Удаляет пользователей, которые не заходили на свой аккаунт:
    - тест: более 3 минут назад
    - продакшн: более 30 дней назад
    """
    # =========================
    # ТЕСТОВАЯ ВЕРСИЯ
    threshold_date = now() - timedelta(minutes=3)  # 3 минуты
    # =========================

    # =========================
    # ПРОДАКШН ВЕРСИЯ
    # threshold_date = now() - timedelta(days=30)  # 30 дней
    # =========================

    # Находим пользователей, которые не заходили
    inactive_users = User.objects.filter(last_login__lt=threshold_date)

    count = inactive_users.count()
    for user in inactive_users:
        logger.info(f"[delete_inactive_users] Удаляем пользователя: {user.email}, последний визит: {user.last_login}")
        user.delete()
    
    logger.info(f"[delete_inactive_users] Всего удалено пользователей: {count}")






# from celery import shared_task
# import logging

# logger = logging.getLogger(__name__)

# @shared_task(bind=True)
# def sync_data_from_db(self):
#     for i in range(1, 11):
#         logger.info(f"[sync_data_from_db] Счёт: {i}")