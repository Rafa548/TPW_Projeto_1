from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests
from .forms import SearchForm


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
        "search": search
    }


    # separating the necessary data
    for i in data:
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
        context["Sport_Data"].append({
            "title": i_sp["title"],
            "author": i_sp["author"],
            "description": "" if i_sp["description"] is None else i_sp["description"],
            "url": i_sp["url"],
            "image": temp_img if i_sp["urlToImage"] is None else i_sp["urlToImage"],
            "publishedat": i_sp["publishedAt"].split("T")[0]
        })

    for i_cul in data_cul:
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

        url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
            query, "popularity", 1, settings.APIKEY
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
        "search": query
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
                "publishedat": i["publishedAt"]
            })

        return render(request, 'search-result.html', context=context)

    # Handle the case when the form is not submitted (e.g., first page load)
    return render(request, 'search-result.html')






def category(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')  # Get the search query from the request
        print("query:",query)
        npage = request.GET.get('page', 1)  # Get the search query from the request

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

        print("page_range:",context["page_range"])
        print("current_page:",context["current_page"])

        for i in data:
            if i["title"] == "[Removed]":
                continue
            context["data"].append({
                "title": i["title"],
                "author": i["author"],
                "description": "" if i["description"] is None else i["description"],
                "url": i["url"],
                "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                "publishedat": i["publishedAt"]
            })
        print (len(context["data"]))

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


