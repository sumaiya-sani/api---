
from django.contrib import admin
from django.db import router
from django.urls import path,include
from ticket import views
from rest_framework.routers import DefaultRouter 
from rest_framework.authtoken.views import obtain_auth_token

router=DefaultRouter()
router.register('guests','views.viewsets_guest',basename='guests')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django/json/',views.no_rest_no_model),
    path('django/json2/',views.no_rest_from_model),
    path('django/json3/',views.FBV_List),
    path('django/json/<int:pk>',views.FBV_pk),
    path('django/json4/',views.CBV_List.as_view()),
    path('django/<int:pk>',views.CBV_PK.as_view()),
    #mixins_list
    path('mixins/',views.mixins_list.as_view()),

    #mixins_pk_ GET BUT DELETE 

    path('mixins/<int:pk>',views.mixins_pk.as_view()),
    #generics_list
   # path('generics/',views.generics_list.as_view()),

    #generics_pk
   # path('generics/<int:pk>',views.generics_pk.as_view()),
#viewsets

    #path('rest/viewsets/',include(router.urls)),
    #Token authentication
    path('api-token-auth',obtain_auth_token),

    ]




