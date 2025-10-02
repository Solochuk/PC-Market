from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from .models import Chat, Message
from .forms import MessageForm

# Create your views here.


def admin_required(view_function):
    return user_passes_test(lambda u: u.is_superuser)(view_function)


@login_required
def chat_view(request):
    chat, created = Chat.objects.get_or_create(user=request.user)
    messages = chat.messages.all().order_by('created_at')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.chat = chat
            msg.sender = request.user
            msg.is_from_admin = False
            msg.save()
            return redirect('chat')
    else:
        form = MessageForm()
    return render(request, 'chat/chat.html', {'chat': chat, 'messages': messages, 'form': form})


@admin_required
def admin_chat_list(request):
    chats = Chat.objects.annotate(
        unread_count_messages=Count('messages', filter=Q(messages__is_read=False, messages__is_from_admin=False))).order_by('-unread_count_messages', '-created_at')
    return render(request, 'chat/admin_chat_list.html', {'chats': chats})


@admin_required
def admin_chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.all().order_by('created_at')
    chat.messages.filter(is_from_admin=False, is_read=False).update(is_read=True)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.chat = chat
            msg.sender = request.user
            msg.is_from_admin = True
            msg.save()
            return redirect('admin_chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()

    return render(request, 'chat/admin_chat_detail.html', {
        'chat': chat,
        'messages': messages,
        'form': form
        })