from django.conf import settings
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle

from .serializers import ContactSerializer

class BurstThrottle(AnonRateThrottle):
    rate = "5/min"

@csrf_exempt            # απλό για αρχή (frontend σε άλλο origin)
@api_view(["POST"])
@throttle_classes([BurstThrottle])
def contact_submit(request):
    ser = ContactSerializer(data=request.data)
    if not ser.is_valid():
        return Response({"errors": ser.errors}, status=status.HTTP_400_BAD_REQUEST)

    data = ser.validated_data
    # honeypot: αν το "website" γέμισε, αγνόησέ το (bot)
    if data.get("website"):
        return Response({"ok": True}, status=status.HTTP_200_OK)

    subject = f"Νέο μήνυμα από {data['name']}"
    body = (
        f"--- Στοιχεία Επικοινωνίας ---\n"
        f"Όνομα: {data['name']}\n"
        f"Επώνυμο: {data['last_name']}\n"
        f"Email: {data['email']}\n"
        f"Τηλέφωνο: {data.get('phone', '-')}\n"
        f"-----------------------------\n\n"
        f"Μήνυμα:\n{data['message']}\n"
    )

    to = [settings.CONTACT_RECIPIENT or settings.EMAIL_HOST_USER]
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
        to=to,
        reply_to=[data["email"]],
    )
    try:
        email.send(fail_silently=False)
        return Response({"ok": True}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"ok": False, "error": "Αποτυχία αποστολής."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
