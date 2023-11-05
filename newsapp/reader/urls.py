from django.urls import path
from reader import views
from django.urls import path, include



urlpatterns = [
    path('', views.home, name="Home"),
    path('next', views.loadcontent, name="Loadcontent"),
    path('prev', views.loadcontent, name="Loadcontent"),
    #path('search', views.search, name="Search"),
    path('search_result', views.search_results, name='search_results'),
    path('index', views.home, name='index'),
    path('category', views.category, name='category'),
    path('save_news', views.save_news, name='save_news'),
    path('delete_news', views.delete_news, name='delete_news'),
    path('bookmarks', views.bookmarks, name='bookmarks'),
    path('add_to_historic',views.add_to_historic, name='add_to_historic'),
]
