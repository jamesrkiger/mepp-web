# coding: utf-8

# MEPP - A web application to guide patients and clinicians in the process of
# facial palsy rehabilitation, with the help of the mirror effect and principles
# of motor learning
# Copyright (C) 2021 MEPP <info@mirroreffectplus.org>
#
# This file is part of MEPP.
#
# MEPP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MEPP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MEPP.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import translation
from django_rest_passwordreset.signals import reset_password_token_created

from mepp.api.models.expiring_token import ExpiringToken


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_post_save(instance=None, created=False, **kwargs):
    if created:
        ExpiringToken.objects.create(user=instance)

        # Skip e-mail for dummy dev accounts.
        skip = instance.email.endswith((
            '@mepp.local',
            '@example.org',
            '@example.com',
        ))

        if not skip:

            # send an e-mail to the user
            mepp_host = settings.HTTP_HOST
            context = {
                'first_name': instance.first_name,
                'email': instance.email,
                'mepp_host': mepp_host,
            }

            translation.activate(instance.language)
            template = (
                'staff_registration'
                if instance.is_staff
                else 'user_registration'
            )
            # render email text
            email_html_message = render_to_string(
                f'email/{template}.html', context
            )
            email_plaintext_message = render_to_string(
                f'email/{template}.txt', context
            )

            msg = EmailMultiAlternatives(
                # title:
                translation.gettext('Your profile has been activated'),
                # message:
                email_plaintext_message,
                # from:
                settings.DEFAULT_FROM_EMAIL,
                # to:
                [instance.email]
            )
            msg.attach_alternative(email_html_message, "text/html")
            msg.send()

        if not created and instance.email_has_changed:

            # send an e-mail to the user
            mepp_host = settings.HTTP_HOST
            context = {
                'first_name': instance.first_name,
                'email': instance.email,
                'previous_email': instance.previous_email,
                'mepp_host': mepp_host,
            }

            translation.activate(instance.language)

            # render email text
            email_html_message = render_to_string(
                'email/user_email_changed.html', context
            )
            email_plaintext_message = render_to_string(
                'email/user_email_changed.txt', context
            )

            msg = EmailMultiAlternatives(
                # title:
                translation.gettext('Your e-mail address has been changed'),
                # message:
                email_plaintext_message,
                # from:
                settings.DEFAULT_FROM_EMAIL,
                # to:
                [instance.previous_email]
            )
            msg.attach_alternative(email_html_message, "text/html")
            msg.send()


@receiver(reset_password_token_created)
def password_reset_token_created(
    instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    """

    # send an e-mail to the user
    mepp_host = settings.HTTP_HOST
    context = {
        'first_name': reset_password_token.user.first_name,
        'reset_password_url': f'{mepp_host}/?t={reset_password_token.key}#reset-password',
        'mepp_host': mepp_host,
    }

    translation.activate(reset_password_token.user.language)

    # render email text
    email_html_message = render_to_string(
        'email/user_reset_password.html', context
    )
    email_plaintext_message = render_to_string(
        'email/user_reset_password.txt', context
    )

    msg = EmailMultiAlternatives(
        # title:
        translation.gettext('Your password reset link'),
        # message:
        email_plaintext_message,
        # from:
        settings.DEFAULT_FROM_EMAIL,
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
