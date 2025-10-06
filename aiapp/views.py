from django.shortcuts import render,redirect,get_object_or_404
from . models import Conversation,Messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from . import rag,ai



def login_view(request):
    if request.method=="POST":
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            return redirect("aiapp:chat")

    else:
        form=AuthenticationForm()

    return render(request,"aiapp/login.html",{"form":form})


def signup_view(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect("aiapp:chat")
    else:
        form=UserCreationForm()

    return render(request,"aiapp/signup.html",{"form":form})


def logout_view(request):
    logout(request)
    return redirect("aiapp:login")

@login_required(login_url="aiapp:login")
def chat_view(request):

    con_id=request.POST.get("con_id")

    if con_id:
      conversation=get_object_or_404(Conversation,id=con_id,user=request.user)

    else:
          conversation = Conversation.objects.create(user=request.user)

    messages=conversation.messages.all().order_by("created_at")
    answer=""


    if request.method=="POST":
        user_input=request.POST.get("input")
        file=request.FILES.get("file")

        if conversation.title=="New Chat" and user_input:
          conversation.title=user_input[:50]
          conversation.save()

        if user_input and file:
            answer=rag.get_rag(user_input,file)

        elif user_input:
            answer=ai.get_ai(user_input,conversation)


        if user_input:
            Messages.objects.create(conversation=conversation,sender="user",content=user_input)

        if answer:
            Messages.objects.create(conversation=conversation,sender="assistant",content=answer)

        messages=conversation.messages.all().order_by("created_at")

    return render(request,"aiapp/chat.html",{"conversation":conversation,"messages":messages})


@login_required(login_url="aiapp:login")
def chat_history(request):
    conversations = request.user.conversations.all().order_by("-created_at")
    return render(request, "aiapp/history.html", {"conversations": conversations})


@login_required(login_url="aiapp:login")
def specific_history(request,id):
    if id:
      conversation=get_object_or_404(Conversation,id=id,user=request.user)
      messages=conversation.messages.all().order_by("created_at")

      return render(request,"aiapp/specific.html",{"messages":messages})




