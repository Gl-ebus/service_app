import time

from celery import shared_task
from celery_singleton import Singleton
from django.db.models import F




# Singleton ставит задачу в очередь только в том случае, если идентичная задача еще не запущена.
# Две задачи считаются идентичными, если обе имеют одинаковое имя и одинаковые аргументы.

@shared_task(base=Singleton)
def set_price(subscription_id):
	from services.models import Subscription #

	time.sleep(7)

	subscription = Subscription.objects.filter(id=subscription_id).annotate(
		annotate_price=F('service__full_price') -
	           F('service__full_price') * F('plan__discount_percent') / 100.00).first()

	subscription.price = subscription.annotate_price
	subscription.save()