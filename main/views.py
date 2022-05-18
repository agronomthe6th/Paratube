from django.forms import URLField
from django.shortcuts import redirect, render
from django.views.generic.base import View, HttpResponseRedirect, HttpResponse
import requests
from .forms import *
from .models import *
import string, random
from django.core.files.storage import FileSystemStorage
import os
from wsgiref.util import FileWrapper
from django.utils import timezone
import subprocess
from django.shortcuts import render, get_object_or_404
from django.db.models import Q 
from .forms import MyForm
from django.shortcuts import render
import random
from pytube import YouTube
from django.core.paginator import Paginator
from django.views.generic import ListView
from users.models import *
# from .serializers import *
from django.http import JsonResponse
from datetime import date, timedelta
import mimetypes
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import Count


list_of_tags = [
    "alien",
    "angel",
    "clown",
    "cryptid",
    "cult",
    "devil",
    "ghost",
    "ghost_hunter",
    "ghost_hunting",
    "gnome",
    "goblin",
    "wendigo",
    "spirit_board",
    "forest",
    "bigfoot",
    "haunted",
    "haunted_house",
    "mutant",
    "mystery",
    "possessed",
    "satan",
    "spirit",
    "supernatural",
    "ufo",
]


class VideoFileView(View):
    
    def get(self, request, file_name):
        # print("video view")
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(BASE_DIR)
        print(file_name)
        file = FileWrapper(open(BASE_DIR+'/main/static/videos/'+file_name, 'rb'))
        response = HttpResponse(file, content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        return response

def Catalog(request):

    # print('\n'+'-------------------------')
    # print(request)
    # print(request.GET)
    # print('-------------------------'+'\n')
    sort = request.GET.get('sort')
    filter = request.GET.get('filter')

    if sort:
        if(sort=='New'):
            videos = Videos.objects.order_by('-datetime')
        elif(sort=='Most viewed') or (sort=='Most+viewed'):
            videos  = Videos.objects.order_by('-views')
        elif(sort=='Popular'):
            # dupes
            videos  = Videos.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')
            # videos = videos.distinct()
            # print(videos)
    else:
        videos = Videos.objects.all()
            
    if filter:
        if(filter=='month'):
            # bad time
            startdate = date.today()+ timedelta(days=1)
            # print(startdate)
            enddate = startdate - timedelta(days=30)
            videos = videos.filter(datetime__range=[enddate, startdate])
        elif(filter=='3month'):
            startdate = date.today()+ timedelta(days=1)
            enddate = startdate - timedelta(days=60)
            videos = videos.filter(datetime__range=[enddate, startdate])
        elif(filter=='6month'):
            startdate = date.today()+ timedelta(days=1)
            enddate = startdate - timedelta(days=180)
            videos = videos.filter(datetime__range=[enddate, startdate])

    paginator = Paginator(videos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={}
    context['tags']=list_of_tags
    context['page_obj']=page_obj

    return render(request, 'main/catalog.html', context)

class HomeView(View):
    template_name = 'main/index.html'
    def get(self, request):
        most_recent_videos = Videos.objects.order_by('-datetime')[:8]
        most_viewed_videos  = Videos.objects.order_by('-views')[:8]
        channel = False
        if request.user.username != "":
            try:
                channel = Channel.objects.filter(user__username = request.user)
                print(channel)
                channel = channel.get()
            except Channel.DoesNotExist:
                channel = False
            if channel: 
                print(request.user)
        return render(request, self.template_name, 
            {'most_recent_videos': most_recent_videos, 
            'most_viewed_videos': most_viewed_videos, 
            'channel': channel,
            'isHome':True,
            'tags':list_of_tags,
            })

class VideoView2(View):

    def get(self, request, id):
        video = Videos.objects.get(id=id)
        video.views = video.views + 1 
        if request.user.is_authenticated:
            video.viewers.add(request.user)
        video.save()
        side_videos = Videos.objects.all().exclude(id = id)
        if Videos.objects.get(id=id).embedornot != True:
            video.path = 'http://localhost:8000/get_video/'+video.path
        paginator = Paginator(side_videos, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        uploader = video.username
        context = {'video':video}
        context['uploader_channel'] = uploader
        context['page_obj'] = page_obj
        return render(request, 'main/video.html', context)

    def post(self, request, id):
        if request.POST.get("operation") == "Subscribe":
            print('Subscribe button pressed on video/' + str(id))
            post = Videos.objects.get(id=id)
            profile = post.user.profile
            if profile.subscribers.filter(id=request.user.id).exists():
                # print('unsub')
                request.user.profile.subscriptions.remove(post.user)
                profile.subscribers.remove(request.user)
                profile.save()
                subscribed = False
            else:
                # print('sub')
                request.user.profile.subscriptions.add(post.user)
                profile.subscribers.add(request.user)
                profile.save()
                subscribed = True
            ctx={"subscribed":subscribed, "subscribers":profile.total_subscribers}
            print(ctx)
            return JsonResponse(ctx)
        elif request.POST.get("operation") == "like_submit":
            
            post = Videos.objects.get(id=id)
            if post.likes.filter(id=request.user.id):
                # print('like removed')
                post.likes.remove(request.user)
                post.save()
                liked = False
            else:
                # print('like pressed')
                post.likes.add(request.user)
                if post.dislikes.filter(id=request.user.id):
                    post.dislikes.remove(request.user)
                post.save()
                liked = True
            ctx={"dislikes_count":post.total_dislikes,"likes_count":post.total_likes,"liked":liked}
            print(ctx)
            return JsonResponse(ctx)
        elif request.POST.get("operation") == "dislike_submit":
            print('dislike pressed')
            post = Videos.objects.get(id=id)
            if post.dislikes.filter(id=request.user.id):
                # print('dislike removed')
                post.dislikes.remove(request.user)
                post.save()
                disliked = False
            else:
                # print('dislike pressed')
                post.dislikes.add(request.user)
                if post.likes.filter(id=request.user.id):
                    post.likes.remove(request.user)
                post.save()
                disliked = True
            ctx={"dislikes_count":post.total_dislikes,"likes_count":post.total_likes,"disliked":disliked}
            print(ctx)
            return JsonResponse(ctx)

class NewVideo(View):
    template_name = 'main/new_video.html'
    
    def get(self, request):
        if request.user.is_authenticated == False:
            print('user not auth')
            channel = "Anon"
            form = CNewVideoForm()
            form2 = CNewYTVideoForm() 
            return render(request, self.template_name, {'form':form, 
            'form2':form2, 
            'channel':channel,
            'list_of_tags':list_of_tags})
        try:
            channel = Channel.objects.filter(user__username = request.user).get().channel_name != "" 
            if channel:
                print(request.user)
                form = NewVideoForm()
                form2 = NewYTVideoForm() 
                return render(request, self.template_name, {'form':form, 
                'form2':form2, 
                'channel':channel,
                'list_of_tags':list_of_tags})
        except Channel.DoesNotExist:
            channel = request.user.username
            print(request.user.username)
            form = NewVideoForm()
            form2 = NewYTVideoForm() 
            print('try failed')
            return render(request, self.template_name, {'form':form,
            'form2':form2, 
            'channel':channel,
            'list_of_tags':list_of_tags})
    def post(self, request):
        print(request)

        form = NewVideoForm(request.POST, request.FILES)       
        form2 = NewYTVideoForm(request.POST, request.FILES) 

        if form.is_valid():

            vtags = dict(request.POST.lists()).get('basic')
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            file = form.cleaned_data['file']

            random_char = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            path = random_char+file.name
            fs = FileSystemStorage(location = os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            fs.save("main/static/videos/"+path, file)
            # file_url = fs.url(filename)

            if not mimetypes.guess_type("main/static/videos/"+path)[0].startswith('video'):
                print('-------------------------------------------------------')
                print('bad video')
                os.remove("main/static/videos/"+path)
                print('-------------------------------------------------------')
                return JsonResponse({"error":"bad format"})
            try:
                subprocess.call(['ffmpeg', '-i', "main/static/videos/"+path, '-ss', '00:00:00.000', '-vframes', '1', "main/static/thumbnails/"+path[:path.index(".") + len(".")]+"jpg"])
                subprocess.call(["ffmpeg", "-t", "5" ,'-hide_banner', "-i","main/static/videos/"+path, "main/static/thumbnails/"+path[:path.index(".") + len(".")]+"gif"])
            except:
                return JsonResponse({'error':"bad format"})
            if request.user.is_authenticated == False:
                new_video = Videos(title=title, 
                    description=description,
                    path=path,
                    # user = request.user,
                    thumbnailpath = "/static/thumbnails/"+path[:path.index(".") + len(".")]+"jpg",
                    views = 0,
                    datetime = timezone.now())
                new_video.save()
            else:
                new_video = Videos(title=title, 
                    description=description,
                    path=path,
                    user = request.user,
                    thumbnailpath = "/static/thumbnails/"+path[:path.index(".") + len(".")]+"jpg",
                    views = 0,
                    datetime = timezone.now())
                new_video.save()
            if vtags:
                for tag in vtags:
                    new_video.tags.add(tag.replace(" ", ""))
            return JsonResponse({'success':"success", 'data':new_video.id})
        elif form2.is_valid():

            vtags = dict(request.POST.lists()).get('basic')

            if validate_url(form2.cleaned_data['link']) != True:
                return JsonResponse({"error":"invalid link"})

            if request.user.is_authenticated == False:
                link = form2.cleaned_data['link']
                video = YouTube(link)
                new_video = Videos(path = link,
                                title=video.title, 
                                embedornot = True,
                                description= video.description,
                                # user=request.user,
                                thumbnailpath = video.thumbnail_url,
                                views = 0,
                                datetime = timezone.now())
                new_video.save()
            else:
                link = form2.cleaned_data['link']
                video = YouTube(link)
                new_video = Videos(path = link,
                                title=video.title, 
                                embedornot = True,
                                description= video.description,
                                user=request.user,
                                thumbnailpath = video.thumbnail_url,
                                views = 0,
                                datetime = timezone.now())
                new_video.save()
            if vtags:
                for tag in vtags:
                    new_video.tags.add(tag.replace(" ", ""))
            t = "http://127.0.0.1:8000/video/" + str(new_video.id) +"/"
            return HttpResponseRedirect(t)
            # change 
            # return JsonResponse({'success':"success", 'data':new_video.id})
            # render(request, 'main/new_video.html')
        else:

            return JsonResponse({'error':"error"})

def aboutus(request):
    return render(request, "main/aboutuss.html", {})

def search(request):
     
    # print('\n'+'START-------------------------')
    # print(request)
    # print(request.GET)
    # print('-------------------------'+'\n')
    search_post = request.GET.get('search')
    if search_post:
                # if ("searchintitle" in request.GET) and ("searchindesc" in request.GET):
                # print('yes both checkmarks are checked')
        posts = Videos.objects.filter(Q(title__icontains=search_post) 
        | Q(description__icontains=search_post) 
        | Q(tags__name__in=[search_post])).distinct()
                # elif "searchintitle" in request.GET:
                #     print('just searchintitle')
                #     posts = Videos.objects.filter(Q(title__icontains=search_post))
                # elif "searchindesc" in request.GET:
                #     print('just searchindesc')
                #     posts = Videos.objects.filter(Q(description__icontains=search_post))
                # else:
                #     posts = Videos.objects.all().order_by("datetime")
    else:
        # print('empty search query')
        posts = Videos.objects.all().order_by("datetime")

    sort = request.GET.get('sort')
    filter = request.GET.get('filter')

    if sort:
        if(sort=='New'):
            videos = posts.order_by('-datetime')
        elif(sort=='Most viewed') or (sort=='Most+viewed'):
            videos  = posts.order_by('-views')
        elif(sort=='Popular'):
            videos  = posts.annotate(num_likes=Count('likes')).order_by('-num_likes')
    else:
        videos = posts.all()

    if filter:
        if(filter=='month'):
            # bad time
            startdate = date.today()+ timedelta(days=1)
            # print(startdate)
            enddate = startdate - timedelta(days=30)
            videos = videos.filter(datetime__range=[enddate, startdate])
        elif(filter=='3month'):
            startdate = date.today()+ timedelta(days=1)
            enddate = startdate - timedelta(days=60)
            videos = videos.filter(datetime__range=[enddate, startdate])
        elif(filter=='6month'):
            startdate = date.today()+ timedelta(days=1)
            enddate = startdate - timedelta(days=180)
            videos = videos.filter(datetime__range=[enddate, startdate])

    paginator = Paginator(videos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={}
    context['tags']=list_of_tags
    context['page_obj']=page_obj
    context['search_post']=search_post
    
    return render(request, 'main/search_results.html', context)

def validate_url(url):
    url_form_field = URLField()
    try:
        url = url_form_field.clean(url)
    except ValidationError:
        return False
    return True

# def test3(request):
#     print('test3')
#     if request.is_ajax():
#         print(request.POST)
#     return render(request, 'main/test.html', {'tags':list_of_tags})

# def updates(request):
#     updates = []
#     if request.user.subscriptions:
#         for u in request.user.subscriptions.all():
#             for v in Videos.objects.filter(user__username = u):
#                 #CHECK IF VIEWED
#                 if not v.viewed(request.user):
#                     updates.append(v)
#     print('finished')
#     print(updates)
#     return updates
