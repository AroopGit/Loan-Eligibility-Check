from django.db.models.signals import post_migrate
from django.dispatch import receiver
from loans.tasks import load_initial_data


@receiver(post_migrate)
def trigger_initial_data_load(sender, **kwargs):
    """
    Trigger the initial data load task after migrations have completed.
    """
    if sender.name == 'loans':
        # Schedule the data loading task
        load_initial_data.delay()