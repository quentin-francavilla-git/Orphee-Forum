from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.safestring import mark_safe
from .mailer import send_grid_mailer
from .forms import DeleteForm, RegistrationForm, \
CustomAuthenticationForm, TopicForm, MessageForm, ResetPasswordForm, \
ResetPasswordFormToken
from .models import TopicList, TopicsMsg, PrivateMessages, Tokens
from django.db.models import Q
from .api import mail
from datetime import datetime, timedelta
import secrets

def index(request):
    return render(request, 'main/index.html')

def cgu(request):
    return render(request, 'main/cgu.html')

def send_mail(to, reason, data):
    if reason == 'NEW_MESSAGE':
        send_grid_mailer(to, mail.message_topic)
    if reason == 'NEW_ACCOUNT':
        send_grid_mailer(to, mail.message_account)
    if reason == 'DELETE_ACCOUNT':
        send_grid_mailer(to, mail.message_delete)
    if reason == 'GET_TOKEN':
        send_grid_mailer(to, mail.message_token(data))


def register_request(response):
    error = None
    if response.method == "POST":
        form = RegistrationForm(response.POST)
        if form.is_valid():
            try:
                pseudo = form.cleaned_data["pseudo"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                User.objects.create_user(username=pseudo,
                                    email=email,
                                    password=password)
                send_mail(email, 'NEW_ACCOUNT', None)
                error = False
            except:
                error = True
                form = RegistrationForm()
    else:
        form = RegistrationForm()

    return render(response, "main/register.html", {"registration_form": form, "formError" : error})


def delete_request(request):
    if request.method == "POST":
        form = DeleteForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form_password = form.cleaned_data.get('password')
            user = authenticate(username=request.user, password=form_password)
            if user is not None:
                user_to_delete = User.objects.get(username = request.user)
                user_mail = user_to_delete.email
                send_mail(user_mail, 'DELETE_ACCOUNT', None)
                user_to_delete.delete()
    form = DeleteForm()
    return render(request, "main/delete.html", {"delete_form":form})

def login_request(request):
    error = False 
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            form_username = form.cleaned_data.get('username')
            form_password = form.cleaned_data.get('password')
            user = authenticate(username=form_username, password=form_password)
            if user is not None:
                login(request, user)
                return redirect("main:index")
            else:
                error = True
        else:
            error = True
    form = CustomAuthenticationForm()
    return render(request, "main/login.html", {"login_form" : form, "formError" : error})

def send_token(email):
    uuid = secrets.token_hex(16)
    token = Tokens(token = uuid, user_mail = email, valid_until = datetime.now() + timedelta(hours=8))
    token.save()
    print("send mail to: [", email, "], with uuid [", uuid, "] ")
    send_mail(email, 'GET_TOKEN', uuid)

def reset_password_step2(request):
    success = None
    form = ResetPasswordFormToken()
    if request.method == "POST":
        form = ResetPasswordFormToken(request.POST)
        if form.is_valid():
            token = form.cleaned_data["token"]
            password = form.cleaned_data['password']
            bdd_token = Tokens.objects.filter(token=token)
            usr = User.objects.get(email=bdd_token[0].user_mail)
            usr.set_password(password)
            usr.save()
            bdd_token.delete()
            success = True

    return render(
        request, "main/reset_password.html",
        {"reset_form" : form, "success" : success }
    )


def reset_password(request):
    next_step = False
    if request.method == "POST":
        form = ResetPasswordForm(request.POST) 
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email)
            print("send token!")
            if (user):
                print("user!")
                send_token(email)
            else:
                print("no user")
            form = ResetPasswordFormToken()
            next_step = True
    else:
        form = ResetPasswordForm()
    return render(
        request, "main/reset_password.html",
        {"reset_form" : form, "next_step" : next_step }
    )

def account(request):
    return render(request, 'main/account.html')

def topics(request):
    topicList = TopicList.objects.all()
    return render(request, 'main/topics.html', {'topics' : topicList})

class Msg:
  def __init__(self):
    self.name = None
    self.date = None

def messages(request):
    formatted_messages = []
    names = []

    if (request.user.is_authenticated):
        messagesList = PrivateMessages.objects.filter(Q(sender=request.user.username) | Q(receiver=request.user.username))

        for msg in messagesList:
            tmp = Msg()
            if msg.receiver == request.user.username:
                tmp.name = msg.sender
            else:
                tmp.name = msg.receiver
            tmp.date = msg.date
            
            if (tmp.name not in names):
                formatted_messages.append(tmp)
                names.append(tmp.name)
    else:
        return render(request, 'main/messages.html')

    return render(request, 'main/messages.html', {'messages' : formatted_messages})

def new_topic(request):
    return render(request, 'main/new_topic.html', {'new_topic' : TopicForm})


def personal_topics(request):
    if request.user.is_authenticated:
        topicList = TopicList.objects.filter(author=request.user.username)
    return render(request, 'main/personal_topics.html', {'topics' : topicList})

def private_message(request, pseudo):
    if (request.user.is_authenticated == False):
        return render(request, 'main/private_message.html', {'notConnected' : True})
    if (pseudo == request.user.username):
        return render(request, 'main/private_message.html', {'sameAuthor' : True})
    messages = PrivateMessages.objects.filter(
            (Q(sender=request.user.username) & Q(receiver=pseudo)) |
            (Q(sender=pseudo) & Q(receiver=request.user.username))
        )

    return render(request, 'main/private_message.html', {'pseudo' : pseudo, 'messageform' : MessageForm, 'messages' : messages})


def post_private_message(response, pseudo):
    if response.method == "POST":
        form = MessageForm(response.POST)
        if form.is_valid() and response.user.is_authenticated:
            msg = form.cleaned_data["message"]

            new_message = PrivateMessages(sender = response.user.username, receiver = pseudo, date = datetime.now(), message = msg)
            new_message.save()

            #print("\n\n>>message posted : ", formMessage, " to: ", pseudo, "\n\n")




    #return render(response, 'main/index.html')
    return HttpResponseRedirect(response.META.get('HTTP_REFERER','/'))


def get_topic(request, id_topic):
    try:
        topic = TopicList.objects.get(id=id_topic)
        messages = TopicsMsg.objects.filter(idTopic=id_topic)
        return render(
            request, 'main/topic.html',
            {
                'id_topic' : id_topic,
                'is_anonymous' : topic.anonymous,
                'author' : topic.author,
                'title' : topic.title,
                'message' : topic.message,
                'date' : topic.date,
                'new_message' : MessageForm,
                'messages' : messages,
            }
        )
    except:
        return render(request, 'main/404.html')


def delete_topic(request, id_topic, confirm):
    topic = TopicList.objects.get(id=id_topic)
    if confirm == 'execute':
        messages = TopicsMsg.objects.filter(idTopic=id_topic)
        messages.delete()
        topic.delete()
        return render(request, 'main/delete_topic.html',
        {'id' : topic.id, 'title' : topic.title, 'deleted' : True})
    return render(request, 'main/delete_topic.html', {'id' : topic.id, 'title' : topic.title})


def delete_message(request, id_message, id_topic):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        message = TopicsMsg.objects.get(id=id_message)
        if (message.author == username):
            message.delete()
    return HttpResponseRedirect('/topic/%i' % id_topic)


def post_topic_request(response):
    if response.method == "POST":
        form = TopicForm(response.POST)
        if form.is_valid() and response.user.is_authenticated:
            try:
                formTitle = form.cleaned_data["title"]
                formMessage = form.cleaned_data["message"]
                formIsAnonymous = form.cleaned_data["anonymous"]
                formUser = response.user
                new_topic = TopicList(author = formUser, title = formTitle, message = formMessage, anonymous = formIsAnonymous)
                new_topic.save()
                return render(response, 'main/new_topic.html', {'topic_success' : True})
            except:
                form = TopicForm()
    return render(response, 'main/new_topic.html', {'new_topic' : TopicForm})

def post_answer_request(response):
    if response.method == "POST":
        form = MessageForm(response.POST)
        if form.is_valid() and response.user.is_authenticated:
            try:
                formUser = response.user
                formMessage = form.cleaned_data["message"]
                id = response.POST.get('idTopic')
                new_message = TopicsMsg(idTopic = id, author = formUser, message = formMessage)
                new_message.save()
                topic = TopicList.objects.get(id=id)
                author = topic.author
                user = User.objects.get(username=author)
                send_mail(user.email, "NEW_MESSAGE", None)
                return HttpResponseRedirect(response.META.get('HTTP_REFERER','/'))
            except:
                form = TopicForm()
    return HttpResponseRedirect(response.META.get('HTTP_REFERER','/'))



def post_edit_topic(request, id_topic):

    topic = TopicList.objects.get(id=id_topic)
    if request.method == "POST":
        form = MessageForm(request.POST)
        topic.message = form.data["message"]
        topic.date = datetime.now()
        topic.save()

    topic = TopicList.objects.get(id=id_topic)
    return HttpResponseRedirect('/topic/%i' % id_topic)


def logout_request(request):
    logout(request)
    return redirect("main:index")

def edit_topic(request, id_topic):

    topic = TopicList.objects.get(id=id_topic)

    return render(
        request, 'main/edit_topic.html',
        {
            'id_topic' : id_topic,
            'is_anonymous' : topic.anonymous,
            'author' : topic.author,
            'title' : topic.title,
            'message' : topic.message,
            'date' : topic.date,
        }
    )



def post_edit_message(request, id_message):

    msg = TopicsMsg.objects.get(id=id_message)
    if request.method == "POST":
        form = MessageForm(request.POST)
        msg.message = form.data["message"]
        msg.date = datetime.now()
        msg.edited = True
        msg.save()

    return HttpResponseRedirect('/topic/%i' % msg.idTopic)

def edit_message(request, id_message):

    msg = TopicsMsg.objects.get(id=id_message)

    return render(
        request, 'main/edit_message.html',
        {
            'id_message' : id_message,
            'author' : msg.author,
            'message': msg.message
        }
    )