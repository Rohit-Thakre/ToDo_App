from django.shortcuts import render
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from main.models import ToDo
from django.db.models import Q

# Create your views here.
def home(request): 
    todo = None
    search = request.GET.get('search') 
    if search: 
        todo = ToDo.objects.filter( Q(user= request.user) & Q(label__icontains=search) | Q(description__icontains = search)).order_by('completed', '-created')
        context = {'todo':todo}


        return render(request, 'home.html', context)

    if request.user.is_authenticated:
        todo = ToDo.objects.filter(user = request.user).order_by('completed','-created')

    context = {'todo':todo}

    return render(request, 'home.html', context)


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        email_check = User.objects.filter(username=username)
        if email_check:
            instance = authenticate(username=username, password=password)
            if instance:
                login(request, instance)
                return redirect('home')
            else:
                return render(request, 'login.html', {'val': True,  'msg': "Password Incorrect !"})

        else:
            return render(request, 'login.html', {'val': True,  'msg': "No account with this credentials"})

    return render(request, 'login.html', {'val': False})

@login_required()
def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        username = request.POST.get('username', '')
        pass1 = request.POST.get('pass1', '')
        pass2 = request.POST.get('pass2', '')
        try:
            usr_obj = User.objects.filter(username = username).first()
            if usr_obj: 
                return render(request, 'register.html', {'val': True, 'msg': 'Email Taken !'})
        except:
            pass


        if full_name == '' and username == '' and pass1 != pass2:
            return render(request, 'register.html', {'val': True, 'msg': 'Fill all fields !'})

        if pass1 != pass2:
            return render(request, 'register.html', {'val': True, 'msg': 'passwords are different !'})

        else:
            user_obj = User.objects.create(username=username)
            user_obj.set_password(pass1)
            user_obj.save()
            login(request, user_obj)
            return redirect('home')

    return render(request, 'register.html')


@login_required()
def remove_task(request, id): 
    task = ToDo.objects.get(id=id)

    if task: 
        task.delete()
    else: 
        return HttpResponse("Nice Try dude!")
    
    return redirect('home')

@login_required()
def create_task(request, id=None):
    context= {}
    if id: 
        task = ToDo.objects.get(id=id)
    
        if request.method == "POST": 
            completed = int(request.POST.get('completed', False))
            label = request.POST.get('label')
            description = request.POST.get('des')

            task.completed=completed
            task.label= label
            task.description = description
            task.save()

            return redirect('home')

        context = {'task':task}
        return render(request, 'create_task.html' , context)
    


    if request.method == "POST": 
        completed = int(request.POST.get('completed', False))
        label = request.POST.get('label' ,' ')
        description = request.POST.get('des', ' ')

        task = ToDo.objects.get_or_create(label=label, description=description, completed = completed,user= request.user)
        return redirect('home')

    return render(request, 'create_task.html' , context)




def user(request):
    todo= ToDo.objects.filter(user= request.user).order_by('completed', '-created')

    context = {'todo':todo, 'todo_cnt': todo.count()}

    return render(request, 'user.html', context)


def del_ac(request): 
    user = User.objects.get(username=request.user)
    user.delete()

    return redirect('home')