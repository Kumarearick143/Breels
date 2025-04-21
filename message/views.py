from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from .models import Message
import json

@login_required
def chat(request):
    return render(request, 'user/messages.html')


@login_required
def get_messages(request, username):
    try:
        user = request.user
        other = User.objects.get(username=username)
        messages = Message.objects.filter(
            sender__in=[user, other],
            receiver__in=[user, other]
        ).order_by('timestamp')

        message_list = [{
            "sender": m.sender.username,
            "receiver": m.receiver.username,
            "content": m.content,
            "timestamp": m.timestamp.strftime('%Y-%m-%d %H:%M')
        } for m in messages]

        return JsonResponse(message_list, safe=False)

    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def send_message(request):
    try:
        data = json.loads(request.body)
        receiver_username = data.get('receiver')
        content = data.get('content')

        if not receiver_username or not content:
            return HttpResponseBadRequest("Receiver and content are required.")

        receiver = User.objects.get(username=receiver_username)
        msg = Message.objects.create(sender=request.user, receiver=receiver, content=content)

        return JsonResponse({'status': 'sent', 'id': msg.id})

    except User.DoesNotExist:
        return JsonResponse({"error": "Receiver not found."}, status=404)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON.")


# NEW VIEW for chat contacts
@login_required
def chat_contacts(request):
    user = request.user
    sent_to = Message.objects.filter(sender=user).values_list('receiver', flat=True)
    received_from = Message.objects.filter(receiver=user).values_list('sender', flat=True)
    contact_ids = set(sent_to) | set(received_from)
    contacts = User.objects.filter(id__in=contact_ids)

    data = [
        {
            'username': u.username,
            'profile_pic_url': getattr(u.profile, 'profile_pic.url', '/static/default-avatar.png') if hasattr(u, 'profile') else '/static/default-avatar.png'
        }
        for u in contacts
    ]
    return JsonResponse(data, safe=False)