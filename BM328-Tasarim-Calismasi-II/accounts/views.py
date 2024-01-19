from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.models import User
from .models import Profile
from slugify import slugify
from .forms import ProfileModelForm



def login_view(request):
    # login olan kullanıcı direkt olarak ana sayfaya gitsin.
    if request.user.is_authenticated:
        messages.info(request, f'{request.user.username} - Loginsin')
        return redirect('home')

    context = dict()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Bu bilgileri doğru aldık mı?
        user = authenticate(request, username=username, password=password)
        #eğer kullanıcıyı bulduysa login ol.
        if len(username) < 3 or len(password) < 3:
            messages.warning(request, f"Lütfen kullanıcı adı veya şifreyei doğru giriniz. 3 karakterden küçük olmamalı")
            redirect('accounts:login_view')
        print(username, password)
        print(user)
        if user is not None: 
            login(request, user)
            # login olduğunu kullanıcıya belli edelim.
            messages.success(request, f'{request.user.username} - Login oldu') 
            return redirect('home')
        #print(request.POST)
        print(username, password)

    return render(request, 'accounts/login.html', context)


def logout_view(request):
    messages.success(request, f'{request.user.username} - Oturumun kapatıldı') 
    logout(request)
    return redirect('home')


def register_view(request):
    context = dict()
    if request.method == 'POST':
        post_info = request.POST
        email = post_info.get('email')
        email_confirm = post_info.get('email_confirm')
        first_name = post_info.get('first_name')
        last_name = post_info.get('last_name')
        password = post_info.get('password')
        password_confirm = post_info.get('password_confirm')
        instagram = post_info.get('instagram')
        print('*'*30)
        print(email, email_confirm, password, password_confirm, first_name, last_name, instagram)
        if len(first_name) < 3 or len(last_name) < 3 or len(email) < 3 or len(password) < 3:
            messages.warning(request, "Bilgiler en az 3 karakterden oluşmalı")

        if email != email_confirm:
            messages.warning(request, "Lütfen email bilgisini doğru giriniz.")
            return redirect('accounts:register_view')
        
        if password != password_confirm:
            messages.warning(request, "Lütfen şifre bilgisini doğru giriniz.")
            return redirect('accounts:register_view')

        user, created = User.objects.get_or_create(username=email)
        #Eğer create değilse kullanıcı vardır. sistemde kaydı vardır. 
        if not created:
            #messages.warning(request, "Daha önce kayit olunmuş")    
            user_login = authenticate(request, username=email, password=password)
            if user_login is not None:
                messages.success(request, "Daha önce kayit oldunuz Ana sayfaya yönlendiriliyorsunuz.")
                login(request, user_login) 
                # login olduğunu kullanıcıya belli edelim.
                return redirect('home')
            messages.warning(request, f"{email} adresi sistemde kayıtlı ama login olmadınız. Login sayfasına yönlendiriliyorsunuz")
            return redirect('accounts:login_view')

        user.email=email
        user.first_name=first_name
        user.last_name=last_name
        user.set_password(password)

        profile, profile_created = Profile.objects.get_or_create(user=user)
        profile.instagram=instagram
        profile.slug=slugify(f"{first_name}-{last_name}")
        user.save()
        profile.save()

        messages.success(request, f"{user.first_name} Sisteme kaydedildiniz")
        user_login = authenticate(request, username=email, password=password)
        login(request, user_login) 
        return redirect('home')

    return render(request, 'accounts/register.html', context)