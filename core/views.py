from django.shortcuts import render ,HttpResponse ,redirect
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib.auth import authenticate ,login as loginuser,logout
from .forms import TODOForm
from .models import TODO
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user=user).order_by('priority')
        return render(request,"home.html",{'form':form ,'todos':todos})

def signout(request):
     logout(request)
     return redirect('/signup')

@login_required(login_url='/login')
def addtodo(request):
     if request.user.is_authenticated:
        user = request.user
     
        form = TODOForm(request.POST)
       
        if form.is_valid():
           
                todo = form.save(commit=False)
                todo.user = user
                todo.save()
                return redirect('/')
       

        else:
            return render(request,"home.html",{'form':form})
         

def login(request):
    if request.method == "GET":
        form = AuthenticationForm()
        return render(request,"login.html",{'form':form})
    
    else:
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
           username = form.cleaned_data.get('username')
           password = form.cleaned_data.get('password') 
           user = authenticate(username = username ,password=password)
           if user is not None:
               loginuser(request,user)
               return redirect('/')
        else:
          return render(request,"login.html",{'form':form})

def signup(request):
    if request.method == "GET":
        form = UserCreationForm()
        return render(request,"signup.html",{'form':form})
    
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect('/login')
        else:
            return render(request,"signup.html",{'form':form}) 
        
def deletetodo(request,id):
    TODO.objects.get(pk = id).delete()
    return redirect('/')

def changetodo(request, id ,status):
    todo=TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('/')


@login_required(login_url='/login')
def search(request):
    query = request.GET['search']

    if len(query)>100:
        todos = TODO.objects.none()
    else:
       todos = TODO.objects.filter(title__icontains = query) 
    if todos.count() == 0:
        return redirect('/')
    return render(request,"search.html",{'todos':todos ,'query':query})
 

