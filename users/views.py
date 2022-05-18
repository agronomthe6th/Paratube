from pickle import FALSE
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
# from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UpdateProfileForm
from main.models import Videos
from .models import Channel, Profile
from django.contrib.auth import logout
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.db.models import Count

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # messages.success(request, f'Account created for {username}')
            channel = Channel.objects.filter(user__username = username).get()
            print(channel)
            channel.channel_name = username
            channel.save()
            return redirect(to='login')
        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "Check your email " \
                      "if an account exists with the email you entered. You should receive them shortly."
    success_url = reverse_lazy('home')

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            # messages.success(request, 'Your profile is updated successfully')
    else:
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'users/profile_edit.html', {'profile_form': profile_form,'profile':True})

def profile_view(request, user):
    template_name = 'users/profile_view.html'
    channel = Channel.objects.filter(user__username = user).get()
    videos = Videos.objects.filter(user__username = channel.user).order_by("-datetime")
    subscriptions = channel.user.profile.subscriptions.all()

    # total_views = 0
    # total_videos = 0
    # for vid in videos:
    #     total_videos+=1
    #     total_views+=vid.views_num
    # updates = []
    # if request.user.subscriptions:
    #     for u in request.user.subscriptions.all():
    #         for v in Videos.objects.filter(user__username = u):
    #             #CHECK IF VIEWED
    #             if not v.viewed(request.user):
    #                 updates.append(v)

    sort = request.GET.get('sort')
    filter = request.GET.get('filter')

    if sort:
        if(sort=='New'):
            videos = videos.order_by('-datetime')
        elif(sort=='Most viewed') or (sort=='Most+viewed'):
            videos  = videos.order_by('-views')
        elif(sort=='Popular'):
            videos  = videos.annotate(num_likes=Count('likes')).order_by('-num_likes')
    else:
        videos = videos.all()
    if filter:
        if(filter=='month'):
            startdate = date.today()
            enddate = startdate - timedelta(days=30)
            videos = videos.filter(datetime__range=[enddate, startdate])
        elif(filter=='3month'):
            startdate = date.today()
            enddate = startdate - timedelta(days=60)
            videos = videos.filter(datetime__range=[enddate, startdate])
        elif(filter=='6month'):
            startdate = date.today()
            enddate = startdate - timedelta(days=180)
            videos = videos.filter(datetime__range=[enddate, startdate])

    paginator = Paginator(videos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    if (channel.user == request.user):
        owner = True 
    else:
        owner = False
    context={}
    context['page_obj']=page_obj
    context['subsriptions'] = subscriptions
    context['channel'] = channel
    # context['total_views'] = total_views
    # context['total_videos'] = total_videos
    # context['updates'] = updates
    context['owner'] = owner
    return render(request, template_name, context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')