from django.conf.urls import url
import views
urlpatterns = [
    url('^$', views.add_to_database),
]