"""
from django.db.models.signals import (
    pre_save          # ? Before saving a model instance (create/update).
    , post_save       # ? After saving a model instance (create/update).
    , pre_delete      # ? Before deleting a model instance.
    , post_delete     # ? After deleting a model instance.
    , pre_migrate     # ? Before applying a migration.
    , post_migrate    # ? After applying a migration.
    , pre_init        # ? Before initializing a model instance. This signal is sent at the beginning of the __init__ method of a model.
    , post_init       # ? After initializing a model instance.This signal is sent at the beginning of the __init__ method of a model.
    , m2m_changed     # ? This signal is sent when a ManyToMany relationship is changed (added/removed).
    , class_prepared  # ? This signal is sent when a model's class is prepared by Django.
)
from django.dispatch import receiver
from .models import UserDetail, UserLog


@receiver(pre_save, sender=UserDetail)
def create_log_on_user_pre_creation(sender, instance, **kwargs):
    # if not instance.pk:
    if instance._state.adding:    # ? User is being created.
        print("Pre-Save Signal: User is being created.")
    else:                         # ? User is being updated.
        print("Pre-Save Signal: User is being updated.")


@receiver(post_save, sender=UserDetail)
def create_log_on_user_post_creation(sender, instance, created, **kwargs):
    '''
    sender: <class 'users.models.UserDetail'>
    instance: <UserDetail: UserDetail object (1)>
    created: True
    kwargs: {'signal': <django.db.models.signals.ModelSignal object at 0x0000012345678950>, 'update_fields': None, 'raw': False, 'using': 'default'}
    '''
    if created:    # ? User is created.
        # If a new UserDetail instance is created, create a new Log instance
        UserLog.objects.create(user_details=instance, comment='New user Created')
    else:          # ? User is updated.
        UserLog.objects.filter(user_details=instance).update(comment='User Updated')

"""
