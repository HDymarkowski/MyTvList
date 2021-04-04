from MyTvList.models import UserProfile
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from MyTvList.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import tmdbSimpleApi

# Create your views here.
def index(request):

    # TODO add like if user logged in show reccomendations or else don't
    # TODO make getPopular to work somehow?
    context_dict = {}
    context_dict['popular'] = tmdbSimpleApi.getPopular()
    UserFavouriteShow = UserProfile.favourite_Show_Name
    context_dict['recs'] = tmdbSimpleApi.getRecommendations(UserFavouriteShow, 3)


    response = render(request, 'Homepage.html', context=context_dict)

    return response

def createAccount(request):
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'createAccount.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('MyTvList:index'))
            else:
                return HttpResponse("Your MyTvList account is disabled")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('MyTvList:index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def topshows(request):

    context_dict = {}

    response = render(request, 'TopShows.html', context=context_dict)

    return response

def recommended(request):

    context_dict = {}

    UserFavouriteShow = UserProfile.favourite_Show_Name
    context_dict['recs'] = tmdbSimpleApi.getRecommendations(UserFavouriteShow, 10)
    #context_dict['recs'] = [{'title':'test', 'tagline': 'test', 'poster_path': ''}]

    response = render(request, 'Recommended.html', context=context_dict)

    return response


def castPage(request):

    #context_dict = tmdbSimpleApi.getCastMemberPage(tmdbSimpleApi.getIdPerson(castMember))
    context_dict = tmdbSimpleApi.getCastMemberPage(tmdbSimpleApi.getIdPerson("James Gandolfini"))
    context_dict['imgFile'] =tmdbSimpleApi.img(context_dict['image'])

    for cred in context_dict['credits']:
        cred['imgFile'] = tmdbSimpleApi.img(cred['image'])
    response = render(request, 'castPage.html',context=context_dict)

    return response