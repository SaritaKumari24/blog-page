from django.contrib import admin
from django.urls import path
from sms.views import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",home, name="home"),
    path("news/<slug>/",viewNews, name="viewNews"),
    path("category/<int:id>/",filterCategory, name="filterCategory"),
    path("delete/<slug>/",deleteNews, name="deleteNews"),
    path("insert/",insertNews, name="insertNews"),
    path("posts/",user_posts, name="posts"),
    path('api-token-auth/', views.obtain_auth_token),
    path("login/",signIn, name="signIn"),
    path("logout/",signOut, name="signOut"),
    path("register/",signUp, name="signUp"),
    path("edit/<slug>/",editNews, name="editNews"),
    path("search/",searchNews, name="search"),
    path("api/post/",PostApi.as_view()),
    path("api/post/<int:id>/",PostApi.as_view()),
    path("api/register/",RegisterUser.as_view()),


    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('postComment/<slug>/',postComment,name="postComment"),
   path('<str:slug>',blogPost,name="blogPost")


 
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)