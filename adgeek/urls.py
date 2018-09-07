from django.conf.urls import url
from . import views
from . import views_tim
from . import views_tony
from . import views_nate

urlpatterns = [
    url(r'^adgeek_api/', views.adgeek_api, name='adgeek_api'),
    url(r'^adgeek_post_qa/', views.adgeek_post_qa, name='adgeek_post_qa'),
    url(r'^adgeek_tim/', views_tim.adgeek_tim, name='adgeek_tim'),
    url(r'^adgeek_tony/', views_tony.adgeek_tony, name='adgeek_tony'),
    url(r'^adgeek_nate/', views_nate.adgeek_nate, name='adgeek_nate'),
]
