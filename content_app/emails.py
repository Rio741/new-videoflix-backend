from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

frontend_url = 'https://web.videoflix.rio-stenger.de'

def send_verification_email(user_email, verification_token):
    subject = "Bestätige deine E-Mail für Videoflix"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    verification_link = f"{frontend_url}/verify-email/{verification_token}"
    
    print(f"🔍 Generierter Verifizierungslink: {verification_link}")

    html_message = render_to_string("emails/verify_email.html", {
        "verification_link": verification_link,
        "username": user_email.split("@")[0]
    })

    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
    email.attach_alternative(html_message, "text/html")
    email.send()


def send_password_reset_email(user_email, reset_token):
    """
    Versendet eine Passwort-Zurücksetzen-E-Mail mit einem Reset-Link.
    """
    subject = "Passwort zurücksetzen – Videoflix"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    reset_link = f"{frontend_url}/reset-password/{reset_token}"
    
    print(f"🔍 Generierter Passwort-Reset-Link: {reset_link}")

    html_message = render_to_string("emails/password_reset.html", {
        "reset_link": reset_link,
        "username": user_email.split("@")[0]
    })

    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
    email.attach_alternative(html_message, "text/html")
    email.send()