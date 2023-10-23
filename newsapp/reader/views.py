from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests

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
        url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
            search,"popularity",page,settings.APIKEY
        )
    print("url:", url)
    r = requests.get(url=url)

    search_sp = "Sport"
    url_sp = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
        search_sp, "popularity", page, settings.APIKEY
    )
    print("url:", url_sp)
    r_sp = requests.get(url=url_sp)

    data = r.json()
    if data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")
    data = data["articles"]

    data_sp = r_sp.json()
    if data_sp["status"] != "ok":
        return JsonResponse({"success": False})
    data_sp = data_sp["articles"]

    context = {
        "success": True,
        "data": [],
        "Sport_Data": [],
        "search": search
    }


    # seprating the necessary data
    for i in data:
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
            "publishedat": i_sp["publishedAt"]
        })

    # send the news feed to template in context
    return render(request, 'index.html', context=context)


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


