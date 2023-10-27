from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required

from accounts.models import Interest
from reader.models import News
from .forms import NewsSaveForm, SearchForm


temp_img = "https://images.pexels.com/photos/3225524/pexels-photo-3225524.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500"
#  https://www.w3schools.com/code/tryit.asp?filename=GJ8R42LMFRLP

def home(request):
    page = request.GET.get('page', 1)
    search = request.GET.get('search', None)

    if search is None or search=="top":
        # get the top news
        url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
            "us",1,settings.APIKEY
        )
    else:
        # get the search query request
        url = "https://newsapi.org/v2/everything?q={}&country={}&sortBy={}&page={}&apiKey={}".format(
            search,"pt","popularity",page,settings.APIKEY
        )
    print("url:", url)
    r = requests.get(url=url)

    search_sp = "Sport"
    url_sp = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
        search_sp, "popularity", page, settings.APIKEY
    )
    print("url:", url_sp)
    r_sp = requests.get(url=url_sp)

    search_cul = "Culture"
    url_cul = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
        search_cul, "popularity", page, settings.APIKEY
    )
    print("url:", url_cul)
    r_cul = requests.get(url=url_cul)



    data = r.json()
    if data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")
    data = data["articles"]

    data_sp = r_sp.json()
    if data_sp["status"] != "ok":
        return JsonResponse({"success": False})
    data_sp = data_sp["articles"]

    data_cul = r_cul.json()
    if data_cul["status"] != "ok":
        return JsonResponse({"success": False})
    data_cul = data_cul["articles"]

    context = {
        "success": True,
        "data": [],
        "Sport_Data": [],
        "Culture_Data": [],
        "search": search,
        "interests": Interest.objects.all()
    }


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
            "publishedat": i["publishedAt"]
        })

    for i_sp in data_sp:
        if i_sp["title"] == "[Removed]":
                continue
        context["Sport_Data"].append({
            "title": i_sp["title"],
            "author": i_sp["author"],
            "description": "" if i_sp["description"] is None else i_sp["description"],
            "url": i_sp["url"],
            "image": temp_img if i_sp["urlToImage"] is None else i_sp["urlToImage"],
            "publishedat": i_sp["publishedAt"].split("T")[0]
        })

    for i_cul in data_cul:
        if i_cul["title"] == "[Removed]":
                continue
        context["Culture_Data"].append({
            "title": i_cul["title"],
            "author": i_cul["author"],
            "description": "" if i_cul["description"] is None else i_cul["description"],
            "url": i_cul["url"],
            "image": temp_img if i_cul["urlToImage"] is None else i_cul["urlToImage"],
            "publishedat": i_cul["publishedAt"].split("T")[0]
        })

    # send the news feed to template in context
    return render(request, 'index.html', context=context)

def search_results(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')  # Get the search query from the request
        print("query:",query)
        npage = request.GET.get('page', 1)

        url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
            query, "popularity", npage, settings.APIKEY
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
    if request.method == 'GET':
        query = request.GET.get('q', '')  # Get the search query from the request
        print("query:",query)
        npage = request.GET.get('page', 1)  # Get the search query from the request

        url = "https://newsapi.org/v2/everything?q={}&page={}&apiKey={}".format(
            query, npage, settings.APIKEY
        )
        print("url:",url)

        r = requests.get(url=url)

        trending_url = "https://newsapi.org/v2/top-headlines?sortBy={}&country=us&page={}&apiKey={}".format(
              "popularity", 1, settings.APIKEY
        )
        print("trending_url:",trending_url)

        r_trending = requests.get(url=trending_url)

        latest_url = "https://newsapi.org/v2/top-headlines?country=us&page={}&apiKey={}&sortBy={}".format(
             1, settings.APIKEY,"publishedAt"
        )
        print("latest_url:", latest_url)

        r_latest = requests.get(url=latest_url)

        popular_url = "https://newsapi.org/v2/everything?q={}&page={}&apiKey={}&sortBy={}".format(
            query, 1, settings.APIKEY,"popularity"
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


        context = {
            "success": True,
            "data": [],
            "Popular_Data": [],
            "Trending_Data": [],
            "Latest_Data": [],
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
    try:
        page = request.GET.get('page', 1)
        search = request.GET.get('search', None)
        # url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
        #     "Technology","popularity",page,settings.APIKEY
        # )
        if search is None or search=="top":
            url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
                "us",page,settings.APIKEY
            )
        else:
            url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
                search,"popularity",page,settings.APIKEY
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

        saved_news = News(
            url=news_url,
            title = news_title,
            description = news_description,
            image = news_image,
            created_at = news_publishedat)

        saved_news.save()
        request.user.user_saved_news.add(saved_news)

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})




