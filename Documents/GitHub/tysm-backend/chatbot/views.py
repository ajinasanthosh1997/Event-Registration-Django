import json
import logging
import os
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from .models import Conversation, Message
import requests
import hmac
import hashlib

logger = logging.getLogger(__name__)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def verify_signature(request):
    signature = request.headers.get('X-Hub-Signature-256', '').split('sha256=')[-1]
    expected = hmac.new(
        os.getenv('WHATSAPP_APP_SECRET').encode(),
        request.body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)


@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        
        if mode == 'subscribe' and token == os.getenv('VERIFY_TOKEN'):
            return HttpResponse(challenge)
        return HttpResponse('Verification failed', status=403)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info("Webhook payload:")
            logger.info(json.dumps(data, indent=2))

            # Safely access nested keys
            if 'entry' in data:
                entry = data['entry'][0]
                changes = entry.get('changes', [])[0]
                value = changes.get('value', {})
                messages = value.get('messages', [])

                if messages:
                    message = messages[0]
                    if message.get('type') == 'text':
                        user_id = message.get('from')
                        user_message = message['text']['body']
                        process_message(user_id, user_message)
            else:
                logger.warning("No 'entry' found in webhook payload.")

            return HttpResponse('OK', status=200)

        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}")
            return HttpResponse('Error', status=500)

def process_message(user_id, text):
    # Get or create conversation
    conversation, created = Conversation.objects.get_or_create(
        whatsapp_user_id=user_id
    )
    
    # Save user message
    Message.objects.create(
        conversation=conversation,
        role='user',
        content=text
    )
    
    # Get last 5 messages for context
    messages = Message.objects.filter(
        conversation=conversation
    ).order_by('-timestamp')[:5]
    
    # Format for OpenAI
    openai_messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for msg in reversed(messages):
        openai_messages.append({"role": msg.role, "content": msg.content})
    
    # Get AI response
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=openai_messages,
            max_tokens=200,
            temperature=0.7
        )
        ai_response = response.choices[0].message.content
        
        # Save and send response
        Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=ai_response
        )
        send_whatsapp_message(user_id, ai_response)
    except Exception as e:
        logger.error(f"OpenAI Error: {str(e)}")
        send_whatsapp_message(user_id, "Sorry, I'm having trouble responding right now.")

def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v19.0/{os.getenv('WHATSAPP_PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {os.getenv('WHATSAPP_TOKEN')}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": { "body": message }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f"WhatsApp API Error: {e}")
        logger.error(f"Status Code: {response.status_code}")
        logger.error(f"Response Text: {response.text}")
