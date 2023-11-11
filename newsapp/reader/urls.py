from django.urls import path
from reader import views


urlpatterns = [
    path('', views.home, name="Home"),
    #path('next', views.loadcontent, name="Loadcontent"),
    #path('prev', views.loadcontent, name="Loadcontent"),
    path('search_result', views.search_results, name='search_results'),
    path('category', views.category, name='category'),
    path('save_news', views.save_news, name='save_news'),
    path('delete_news', views.delete_news, name='delete_news'),
    path('add_to_historic',views.add_to_historic, name='add_to_historic'),
    path('delete_historic_news', views.delete_historic_news, name='delete_historic_news'),
]
