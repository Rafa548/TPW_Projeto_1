import subprocess
import os
import requests

from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from accounts.models import Interest
from reader.models import News
from accounts.models import User
from .forms import NewsSaveForm, SearchForm
from django.core.cache import cache


API_KEYS = [
   "fde47eb1fd3c4768964eb3d3bd9eaae2",
   "7dfa405963a9460693136651c8006b36",
   "dbb12ae7153a417b85f1b3ea8f8bfe6e",
   "0d349c59c2cb4d4dac3c008cb0149b09",
    "2def9e2a6c4841518f693d780c62d6ff",
    "9803944a12724709be189825d140c2ab",
    "b147c9ae5a0b4b2ea438d7192a13aed5",
]

API_KEY = API_KEYS[0]
    
def select_new_api_key():
    global API_KEY 
    global API_KEYS 
    current_key_index = API_KEYS.index(API_KEY)
    if is_rate_limited(API_KEY):
        next_key_index = (current_key_index + 1) % len(API_KEYS)
    else:
        next_key_index = current_key_index

    for _ in range(len(API_KEYS)):
        next_key = API_KEYS[next_key_index]
        print(f"Checking API key {next_key}")
        #print(f"Api_keys: {API_KEYS}")
        if not is_rate_limited(next_key):
            print(f"Switching to API key {next_key}")
            return next_key
        next_key_index = (next_key_index + 1) % len(API_KEYS)

    return None

def is_rate_limited(api_key):
    url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
                "us",1,api_key
            )
    print("url:", url)
    response = requests.get(url)
    if response.status_code == 429:  # HTTP 429 indicates rate limiting
        print(f"API key {api_key} is rate limited.")
        return True
    return False



temp_img = "https://images.pexels.com/photos/3225524/pexels-photo-3225524.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500"

def home(request):
    user = request.user
    cache_key = f"newsfeed_{user.id}"
    context = cache.get(cache_key)

    if context is None:
        global API_KEY
        page = request.GET.get('page', 1)
        search = request.GET.get('search', None)
        notifications = 0
        url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
                "us",1,API_KEY
            )
        print("url:", url)
        r = requests.get(url=url)
        if r.status_code == 429:
            print("changing api key")
            API_KEY = select_new_api_key()
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
                "notifications": notifications,
                "notifications_news": [],
            }
        
        data = r.json()
        if data["status"] != "ok":
            return HttpResponse("<h1>Request Failed</h1>")
        data = data["articles"]

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
            if r.status_code == 429:
                print("changing api key")
                API_KEY = select_new_api_key()
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
            last_news_titles = user.user_last_news.values_list('title', flat=True)
            last_news = list(last_news_titles)

            x=0
            for interest in interests:
                context["user_interests"].append(interest.name)
                search = interest.name


                url1 = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
                    search, "publishedAt", page, API_KEY
                )
                r1 = requests.get(url=url1)

                if r1.status_code == 429:
                    print("changing api key")
                    API_KEY = select_new_api_key()
                    url1 = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
                        search, "publishedAt", page, API_KEY
                    )

                    print("url:", url1)
                    r1 = requests.get(url=url1)

                data1 = r1.json()
                if data1["status"] != "ok":
                    return HttpResponse("<h1>Request Failed</h1>")
                data1 = data1["articles"]

                for i in data1:
                    if i["title"] == "[Removed]":
                        continue
                    if i["author"] is None:
                        i["author"] = "Anonymous"
                    if i["description"] is None:
                        i["description"] = "No description provided"
                    if page == 1 and i["title"] not in last_news:
                        new = News(url=i["url"], title=i["title"], description=i["description"], image=i["urlToImage"], created_at=i["publishedAt"])
                        #print("new:", new)
                        if new not in News.objects.all():
                            new.save()
                        user.user_last_news.add(new)
                        if notifications < 10:
                            context["notifications_news"].append({
                                "title": i["title"],
                                "author": i["author"],
                                "description": "No description provided" if i["description"] is None else i["description"],
                                "url": i["url"],
                                "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                                "publishedat": i["publishedAt"]
                            })
                            notifications+=1
                    
            
                context["notifications"] += notifications


                url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
                    search, "popularity", page, API_KEY
                )
                print("url:", url)
                r = requests.get(url=url)

                if r.status_code == 429:
                    print("changing api key")
                    API_KEY = select_new_api_key()
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
            print("notifications:", notifications)
        cache.set(cache_key, context, settings.CACHE_TIMEOUT)
    return render(request, 'index.html', context=context)


def search_results(request):
    global API_KEY
    if request.method == 'GET':
        query = request.GET.get('q', '')  # Get the search query from the request
        print("query:",query)
        npage = request.GET.get('page', 1)

        url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&searchIn=title&apiKey={}".format(
            query, "popularity", npage, API_KEY
        )

        r = requests.get(url=url)

        if r.status_code == 429:
                    print("changing api key")
                    API_KEY = select_new_api_key()
                    url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&searchIn=title&apiKey={}".format(
                        query, "popularity", npage, API_KEY
                    )

                    print("url:", url)
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

        saved_news_url = []
        if request.user.is_authenticated:
            saved_news = request.user.user_saved_news.all()
            for i in saved_news:
                saved_news_url.append(i.url)

        context = {
        "success": True,
        "data": [],
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

        return render(request, 'search-result.html', context=context)

    # Handle the case when the form is not submitted (e.g., first page load)
    return render(request, 'search-result.html')


def category(request):
    category = request.GET.get('q', '')
    n_page = request.GET.get('page', 1)
    cache_key = f"category_{category}_{n_page}"
    context = cache.get(cache_key)
    if context is None:
        global API_KEY
        if request.method == 'GET':
            query = request.GET.get('q', '')  # Get the search query from the request
            #print("query:",query)
            npage = request.GET.get('page', 1)  # Get the search query from the request

            url = "https://newsapi.org/v2/everything?q={}&page={}&apiKey={}".format(
                query, npage, API_KEY
            )
            #print("url:",url)

            r = requests.get(url=url)

            if r.status_code == 429:
                    print("changing api key")
                    API_KEY = select_new_api_key()
                    url = "https://newsapi.org/v2/everything?q={}&page={}&apiKey={}".format(
                        query, npage, API_KEY
                    )

                    print("url:", url)
                    r = requests.get(url=url)

            trending_url = "https://newsapi.org/v2/top-headlines?sortBy={}&country=us&page={}&apiKey={}".format(
                "popularity", 1, API_KEY
            )
            #print("trending_url:",trending_url)

            r_trending = requests.get(url=trending_url)

            if r_trending.status_code == 429:
                print("changing api key")
                API_KEY = select_new_api_key()
                trending_url = "https://newsapi.org/v2/top-headlines?sortBy={}&country=us&page={}&apiKey={}".format(
                    "popularity", 1, API_KEY
                )

                print("url:", trending_url)
                r_trending = requests.get(url=trending_url)

            latest_url = "https://newsapi.org/v2/top-headlines?country=us&page={}&apiKey={}&sortBy={}".format(
                1, API_KEY,"publishedAt"
            )
            #print("latest_url:", latest_url)

            r_latest = requests.get(url=latest_url)

            if r_latest.status_code == 429:
                print("changing api key")
                API_KEY = select_new_api_key()
                latest_url = "https://newsapi.org/v2/top-headlines?country=us&page={}&apiKey={}&sortBy={}".format(
                    1, API_KEY,"publishedAt"
                )
                print("url:", latest_url)
                r_latest = requests.get(url=latest_url)

            popular_url = "https://newsapi.org/v2/everything?q={}&page={}&apiKey={}&sortBy={}".format(
                query, 1, API_KEY,"popularity"
            )
            #print("popular_url:", popular_url)

            r_popular = requests.get(url=popular_url)

            if r_popular.status_code == 429:
                print("changing api key")
                API_KEY = select_new_api_key()
                popular_url = "https://newsapi.org/v2/everything?q={}&page={}&apiKey={}&sortBy={}".format(
                    query, 1, API_KEY,"popularity"
                )
                print("url:", popular_url)
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
            #print (len(context["data"]))

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

            cache.set(cache_key, context, settings.CACHE_TIMEOUT)
    return render(request, 'category.html', context=context)


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

@login_required
def delete_historic_news(request):
    if request.method == 'POST':
        news_url = request.POST.get('news_url', None)
        if news_url is None:
            return JsonResponse({"success": False})
        news = request.user.user_news_historic.filter(url=news_url)
        if news.exists():
            news.delete()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})
    return JsonResponse({"success": False})


def add_to_historic(request):
    news_url = request.GET.get('url')
    news_title = request.GET.get('title')
    news_description = request.GET.get('description')
    news_image = request.GET.get('image')
    news_publishedat = request.GET.get('publishedat')

    if news_url:
        if request.user.is_authenticated:
            new = News.objects.create(url=news_url, title=news_title, description=news_description, image=news_image, created_at=news_publishedat)
            new.save()
            user = User.objects.get(email=request.user)
            user.user_news_historic.add(new)

    return redirect(news_url)

def get_cached_data(url, cache_key, cache_timeout):
    cached_data = cache.get(cache_key)
    if cached_data is None:
        response = requests.get(url)
        data = response.json()
        cache.set(cache_key, data, cache_timeout)
    else:
        data = cached_data
    return data


def get_latest_interests(request):
    user = request.user
    interests = user.profile.interests.all()
    interests_data = [interest.name for interest in interests]
    context = { "interests_modal": interests_data }
    return render(request, 'index.html', context=context)