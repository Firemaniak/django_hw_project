
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Task


@receiver(pre_save, sender=Task, dispatch_uid='task_pre_save_status_check')
def task_pre_save_status_check(sender, instance, **kwargs):

    try:
        old_instance = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:

        instance._status_changed = False
        return

    instance._status_changed = old_instance.status != instance.status
    instance._old_status = old_instance.status


@receiver(post_save, sender=Task, dispatch_uid='task_post_save_notify')
def task_post_save_notify(sender, instance, created, **kwargs):

    if created:
        return

    status_changed = getattr(instance, '_status_changed', False)
    if not status_changed:
        return

    old_status = getattr(instance, '_old_status', None)
    owner_email = getattr(instance.owner, 'email', None)

    if not owner_email:
        return

    send_mail(
        subject=f'Статус задачи "{instance.title}" изменён',
        message=(
            f'Задача "{instance.title}" изменила статус:\n'
            f'{old_status} → {instance.status}'
        ),
        from_email='noreply@taskmanager.local',
        recipient_list=[owner_email],
        fail_silently=False,
    )

    instance._status_changed = False