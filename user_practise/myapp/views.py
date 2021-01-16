from django.shortcuts import render
from myapp.forms import UserInfo,MoreInfo
from myapp.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
# Create your views here.


def index(request):
    return render(request,'myapp/index.html')

@login_required
def user_profile(request):
    data = UserProfile.objects.filter(user = request.user).values_list('portfolio','dp')
    if not data:
        portfolio = ''
        dp = ''
    else:
        portfolio, dp = data[0]
        dp = dp.split('/')[-1]
        dp = '/media/dps/'+dp
    mydic={'username':request.user.username,'email':request.user.email,'portfolio':portfolio,'dp':dp}
    return render(request, 'myapp/user_profile.html',context=mydic)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False

    if request.method == 'POST':
        user = UserInfo(request.POST, request.FILES)
        more = MoreInfo(request.POST, request.FILES)

        if user.is_valid() and more.is_valid():
            user = user.save(commit=False)
            user.set_password(request.POST.get('password'))
            user.save()

            more = more.save(commit=False)
            more.user = user
            if 'dps' in request.FILES:
                more.dp = request.FILES['dps']
            more.save()
            # mydic.update({'username':user.username,'email':user.email,'protfolio':more.portfolio,'dp':more.dp})
            registered = True

        else:
            return HttpResponse('Something inserted wrong!')

    else:
        user = UserInfo()
        more = MoreInfo()
    return render(request,'myapp/register.html', context = {
    'registered':registered, 'user_info' : user, 'more_info':more
    })



def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Your session is expired!')

        else :
            print("{} tried to login is a unauthorized user".format(username))
            return HttpResponse('Sorry, You are not registered')

    return render(request, 'myapp/login.html')
