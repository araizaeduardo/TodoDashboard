import telnyx
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Task

telnyx.api_key = settings.TELNYX_API_KEY

@csrf_exempt
@require_POST
def telnyx_webhook(request):
    payload = request.body
    signature = request.headers.get('Telnyx-Signature-Ed25519', '')
    timestamp = request.headers.get('Telnyx-Timestamp', '')

    try:
        event = telnyx.Webhook.construct_event(
            payload, signature, timestamp
        )
    except ValueError:
        return HttpResponse(status=400)
    except telnyx.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event.type == 'message.received':
        handle_incoming_message(event.data)

    return HttpResponse(status=200)

def handle_incoming_message(message_data):
    from_number = message_data.payload.from_.phone_number
    text = message_data.payload.text

    # Crear una nueva tarea basada en el mensaje
    task = Task.objects.create(
        title=f"SMS de {from_number}",
        description=text,
        state='planned'
    )

    # Enviar una confirmación por SMS
    telnyx.Message.create(
        from_=settings.TELNYX_PHONE_NUMBER,
        to=from_number,
        text=f"Tarea creada con ID: {task.id}"
    )
