from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required
import subprocess

from accounts.models import Interest
from reader.models import News
from accounts.models import User
from .forms import NewsSaveForm, SearchForm


from django.core.management.base import BaseCommand

from django.conf import settings
import os
import requests

API_KEYS = [
   "fde47eb1fd3c4768964eb3d3bd9eaae2",
   "7dfa405963a9460693136651c8006b36",
   "dbb12ae7153a417b85f1b3ea8f8bfe6e",
]

current_key_index = 0
API_KEY = API_KEYS[current_key_index]
    
def select_new_api_key():
    global API_KEY  
    global current_key_index
    if is_rate_limited(API_KEY):
        next_key_index = (current_key_index + 1) % len(API_KEYS)
    else:
        return API_KEY

    for _ in range(len(API_KEYS)):
        next_key = API_KEYS[next_key_index]
        if not is_rate_limited(next_key):
            print(f"Switching to API key {next_key}")
            return next_key
        next_key_index = (next_key_index + 1) % len(API_KEYS)

    return None

def is_rate_limited(api_key):
    url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
                "us",1,api_key
            )
    response = requests.get(url)
    if response.status_code == 429:  # HTTP 429 indicates rate limiting
        print(f"API key {api_key} is rate limited.")
        return True
    return False



temp_img = "https://images.pexels.com/photos/3225524/pexels-photo-3225524.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500"
#  https://www.w3schools.com/code/tryit.asp?filename=GJ8R42LMFRLP

def home(request):
    API_KEY = select_new_api_key()
    page = request.GET.get('page', 1)
    search = request.GET.get('search', None)
    url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
            "us",1,API_KEY
        )
    print("url:", url)
    r = requests.get(url=url)

    default_interests = ["Technology", "Science", "Health", "Entertainment", "Sport", "Culture"]

    context = {
            "success": True,
            "data": [],
            "interests": Interest.objects.all(),
            "user_interests": [],
        }
    
    data = r.json()
    if data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")
    data = data["articles"]

    # separating the necessary data
    for i in data:
        if i["title"] == "[Removed]":
                continue
        if i["author"] is None:
            i["author"] = "Anonymous"
        context["data"].append({
            "title": i["title"],
            "author": i["author"],
            "description":  "" if i["description"] is None else i["description"],
            "url": i["url"],
            "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
            "publishedat": i["publishedAt"].split("T")[0]
        })

    for interest in default_interests:
        search = interest
        url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
            search, "popularity", page, API_KEY
        )
        print("url:", url)
        r = requests.get(url=url)
        data = r.json()
        if data["status"] != "ok":
            return HttpResponse("<h1>Request Failed</h1>")
        data = data["articles"]

        context["data_"+search] = []

        for i in data:
            if i["title"] == "[Removed]":
                continue
            if i["author"] is None:
                i["author"] = "Anonymous"
            context["data_"+search].append({
                "title": i["title"],
                "author": i["author"],
                "description": "" if i["description"] is None else i["description"],
                "url": i["url"],
                "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                "publishedat": i["publishedAt"].split("T")[0]
            })
        if search == "Sport":
            print("context:", "data_"+search)

    if request.user.is_authenticated:
        user = request.user
        interests = user.interests.all()
        x=0
        for interest in interests:
            context["user_interests"].append(interest.name)
            search = interest.name
            url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
                search, "popularity", page, API_KEY
            )
            print("url:", url)
            r = requests.get(url=url)
            data = r.json()
            if data["status"] != "ok":
                return HttpResponse("<h1>Request Failed</h1>")
            data = data["articles"]

            context["data_"+str(x)] = []
            
            for i in data:
                if i["title"] == "[Removed]":
                    continue
                if i["author"] is None:
                    i["author"] = "Anonymous"
                context["data_"+str(x)].append({
                    "title": i["title"],
                    "author": i["author"],
                    "description": "" if i["description"] is None else i["description"],
                    "url": i["url"],
                    "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                    "publishedat": i["publishedAt"].split("T")[0]
                })
            x+=1
    # send the news feed to template in context
    return render(request, 'index.html', context=context)

def search_results(request):
    API_KEY = select_new_api_key()
    if request.method == 'GET':
        query = request.GET.get('q', '')  # Get the search query from the request
        print("query:",query)
        npage = request.GET.get('page', 1)

        url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
            query, "popularity", npage, API_KEY
        )

        r = requests.get(url=url)

        data = r.json()
        if data["status"] != "ok":
            return HttpResponse("<h1>Request Failed</h1>")
        data = data["articles"]
        # Process the query and obtain search results
        # You can use Django's ORM or any other method to retrieve search results

        # For example, if you have a model named 'Article' and want to search in its title field:
        # search_results = Article.objects.filter(title__icontains=query)

        #context = {
        #    'query': query,
            # 'search_results': search_results,  # Uncomment this line if you have search results to display
        #}

        context = {
        "success": True,
        "data": [],
        "search": query,
        "current_page": int(npage),
        "page_range": range(1,6)
        }

        for i in data:
            if i["title"] == "[Removed]":
                continue
            context["data"].append({
                "title": i["title"],
                "author": i["author"],
                "description": "" if i["description"] is None else i["description"],
                "url": i["url"],
                "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                "publishedat": i["publishedAt"].split("T")[0]
            })

        return render(request, 'search-result.html', context=context)

    # Handle the case when the form is not submitted (e.g., first page load)
    return render(request, 'search-result.html')



def category(request):
    API_KEY = select_new_api_key()
    if request.method == 'GET':
        query = request.GET.get('q', '')  # Get the search query from the request
        print("query:",query)
        npage = request.GET.get('page', 1)  # Get the search query from the request

        url = "https://newsapi.org/v2/everything?q={}&page={}&apiKey={}".format(
            query, npage, API_KEY
        )
        print("url:",url)

        r = requests.get(url=url)

        trending_url = "https://newsapi.org/v2/top-headlines?sortBy={}&country=us&page={}&apiKey={}".format(
              "popularity", 1, API_KEY
        )
        print("trending_url:",trending_url)

        r_trending = requests.get(url=trending_url)

        latest_url = "https://newsapi.org/v2/top-headlines?country=us&page={}&apiKey={}&sortBy={}".format(
             1, API_KEY,"publishedAt"
        )
        print("latest_url:", latest_url)

        r_latest = requests.get(url=latest_url)

        popular_url = "https://newsapi.org/v2/everything?q={}&page={}&apiKey={}&sortBy={}".format(
            query, 1, API_KEY,"popularity"
        )
        print("popular_url:", popular_url)

        r_popular = requests.get(url=popular_url)

        data = r.json()
        if data["status"] != "ok":
            return HttpResponse("<h1>Request Failed</h1>")
        data = data["articles"]

        data_trending = r_trending.json()
        if data_trending["status"] != "ok":
            return HttpResponse("<h1>Request Failed</h1>")
        data_trending = data_trending["articles"]

        data_latest = r_latest.json()
        if data_latest["status"] != "ok":
            return HttpResponse("<h1>Request Failed</h1>")
        data_latest = data_latest["articles"]

        data_popular = r_popular.json()
        if data_popular["status"] != "ok":
            return HttpResponse("<h1>Request Failed</h1>")
        data_popular = data_popular["articles"]


        
        saved_news_url = []
        if request.user.is_authenticated:
            saved_news = request.user.user_saved_news.all()
            for i in saved_news:
                saved_news_url.append(i.url)
        
        context = {
            "success": True,
            "data": [],
            "Popular_Data": [],
            "Trending_Data": [],
            "Latest_Data": [],
            "search": query,
            "current_page": int(npage),
            "page_range": range(1,6),
            "saved_news_url": saved_news_url
        }

        for i in data:
            if i["title"] == "[Removed]":
                continue
            context["data"].append({
                "title": i["title"],
                "author": i["author"],
                "description": "" if i["description"] is None else i["description"],
                "url": i["url"],
                "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                "publishedat": i["publishedAt"].split("T")[0]
            })
        print (len(context["data"]))

        for i_trending in data_trending:
            if i_trending["title"] == "[Removed]":
                continue
            context["Trending_Data"].append({
                "title": i_trending["title"],
                "author": i_trending["author"],
                "description": "" if i_trending["description"] is None else i_trending["description"],
                "url": i_trending["url"],
                "image": temp_img if i_trending["urlToImage"] is None else i_trending["urlToImage"],
                "publishedat": i_trending["publishedAt"].split("T")[0]
            })

        for i_latest in data_latest:
            if i_latest["title"] == "[Removed]":
                continue
            context["Latest_Data"].append({
                "title": i_latest["title"],
                "author": i_latest["author"],
                "description": "" if i_latest["description"] is None else i_latest["description"],
                "url": i_latest["url"],
                "image": temp_img if i_latest["urlToImage"] is None else i_latest["urlToImage"],
                "publishedat": i_latest["publishedAt"].split("T")[0]
            })

        for i_popular in data_popular:
            if i_popular["title"] == "[Removed]":
                continue
            context["Popular_Data"].append({
                "title": i_popular["title"],
                "author": i_popular["author"],
                "description": "" if i_popular["description"] is None else i_popular["description"],
                "url": i_popular["url"],
                "image": temp_img if i_popular["urlToImage"] is None else i_popular["urlToImage"],
                "publishedat": i_popular["publishedAt"].split("T")[0]
            })


        return render(request, 'category.html', context=context)

    # Handle the case when the form is not submitted (e.g., first page load)
    return render(request, 'category.html')


def loadcontent(request):
    API_KEY = select_new_api_key()
    try:
        page = request.GET.get('page', 1)
        search = request.GET.get('search', None)
        # url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
        #     "Technology","popularity",page,API_KEY
        # )
        if search is None or search=="top":
            url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
                "us",page,API_KEY
            )
        else:
            url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
                search,"popularity",page,API_KEY
            )
        print("url:",url)
        r = requests.get(url=url)


        context = {
            "success": True,
            "data": [],

            "search": search
        }


        data = r.json()
        if data["status"] != "ok":
            return JsonResponse({"success":False})
        data = data["articles"]




        for i in data:
            context["data"].append({
                "title": i["title"],
                "author": i["author"],
                "description":  "" if i["description"] is None else i["description"],
                "url": i["url"],
                "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                "publishedat": i["publishedAt"]
            })




        return JsonResponse(context)
    except Exception as e:
        return JsonResponse({"success":False})
    
@login_required
def save_news(request):
    form = NewsSaveForm(request.POST)
    print(form.is_valid())
    print(form.errors)

    if form.is_valid():
        news_url = form.cleaned_data['news_url']
        news_title = form.cleaned_data['news_title']
        news_description = form.cleaned_data['news_description']
        news_image = form.cleaned_data['news_image']
        news_publishedat = form.cleaned_data['news_publishedat']

        #check if the news already exists of this user
        news = request.user.user_saved_news.filter(url=news_url)
        if news.exists():
            
            return JsonResponse({"exists": True})

        saved_news = News(
        
        url=news_url,
        title = news_title,
        description = news_description,
        image = news_image,
        created_at = news_publishedat,)

        saved_news.save()
        request.user.user_saved_news.add(saved_news)

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})

@login_required
def delete_news(request):
    if request.method == 'POST':
        news_url = request.POST.get('news_url', None)
        print(news_url)
        if news_url is None:
            return JsonResponse({"success": False})
        news = request.user.user_saved_news.filter(url=news_url)
        if news.exists():
            news.delete()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})
    return JsonResponse({"success": False})

def bookmarks(request):
    user = request.user
    saved_news = user.user_saved_news.all()

    context = {
        'saved_news': saved_news
    }

    return render(request, 'bookmarks.html', context)



def add_to_historic(request):
    news_url = request.GET.get('url')
    news_title = request.GET.get('title')
    news_description = request.GET.get('description')
    news_image = request.GET.get('image')
    news_publishedat = request.GET.get('publishedat')

    if news_url:
        if request.user.is_authenticated:
            print(request.user)
            new = News.objects.create(url=news_url, title=news_title, description=news_description, image=news_image, created_at=news_publishedat)
            new.save()
            user = User.objects.get(email=request.user)
            user.user_news_historic.add(new)

    # Redirect to the original news URL
    return redirect(news_url)
