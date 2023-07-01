from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import *
from rest_framework.views import APIView
from .serializers import PostSerializer,UserSerializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import  HttpResponseRedirect


def home(r):
    data = {
        "category":Category.objects.all(),
        "posts" : Post.objects.all()
    }
    return render(r, "home.html",data)

def viewNews(r,slug):
    # isAuth=False
    # post=Post.objects.get(slug=slug)
    # if post.author.id == r.user.id:
    #     isAuth=True 
    data = {
        "category":Category.objects.all(),
        "post" : Post.objects.get(slug=slug),
        
        #"isAuth":isAuth
        "related_posts":Post.objects.exclude(slug=slug)
    }
    return render(r,"view.html",data)

def blogPost(r,slug):
    post=Post.objects.filter(slug=slug)
    comment=Comment.object.filter(post=post)
    context={'post':post,'comment':comment}
    return render(r,'view.html',context)



def postComment(r,slug):
    if r.method=="POST":
        postId=r.POST.get("postId")
        post=Post.objects.get(id=postId)
        text = r.POST.get("comment")
        comment=Comment(text=comment,post=post)
        comment.save()
        
    return redirect("/")
    
    

@login_required()
def user_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'user_post.html', {'posts': posts})

def like_post(r,post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes += 1
    post.save()   
    return HttpResponseRedirect(r.META.get('HTTP_REFERER'))

    


@login_required()
def insertNews(r):
    form = PostForm(r.POST or None, r.FILES or None)
    data = {
        "form":form,
        "category":Category.objects.all()
    }

    if r.method == "POST":
        formData = form.save(commit=False)
        formData.author = r.user
        formData.save()
        return redirect(home)
    
    return render(r, "insert.html",data)

def deleteNews(r,slug):
    data = Post.objects.get(slug=slug)
    data.delete()
    return redirect(home)

def editNews(r,slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(r.POST or None, r.FILES or None, instance=post)
    data = {
        "form":form,
        "category":Category.objects.all()
    }

    if r.method == "POST":
        formData = form.save(commit=False)
        formData.author = r.user
        formData.save()
        return redirect(home)
    
    return render(r, "insert.html",data)

def signUp(r):
    form = UserCreationForm(r.POST or None)
    data = {
        "form":form
    }
    if r.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(signIn)
    # data = {}
    # data['form'] = form
    return render(r,"accounts/register.html",data) 

def signIn(r):
    form = AuthenticationForm(r.POST or None)
    data = {
        "form":form
    }

    if r.method == "POST":
        username = r.POST.get("username")
        password = r.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(r,user)
            return redirect(home)
    return render(r,"accounts/login.html",data)

def filterCategory(r,id):
    data = {
        "posts":Post.objects.filter(category__id=id),
        "category":Category.objects.all()
    }
    return render(r, "home.html",data)

def searchNews(r):
    search = r.GET.get('search')
    data = {
        "posts":Post.objects.filter(title__icontains=search),
        "category":Category.objects.all()
    }
    return render(r, "home.html",data) 

def signOut(r):
    logout(r)
    return redirect(home)



#api work

class RegisterUser(APIView):
    def post(self,r):
        serializer=UserSerializers(data=r.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        else:
            serializer.save()
            user=User.objects.get(username=serializer.data['username'])
            token_obj=Token.objects.get_or_create(user=user)
            return Response({'payload':serializer.data,'token':str(token_obj)})
                


class PostApi(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,r,id=None):
        if(id==None):
            posts=Post.objects.all()
            serializer=PostSerializer(posts,many=True)
        else:
            posts=Post.objects.get(pk=id)
            serializer=PostSerializer(posts)   

        return Response(serializer.data)  

    def post(self,r):
        data={
            "title":r.POST.get("title"),
            "category":r.POST.get("category"),
            "author":r.POST.get("author"),
            "content":r.POST.get("content"),
            "image":r.POST.get("image"),
            "date" :r.POST.get("date"), 
            "slug" :r.POST.get("slug"), 
        }

        serializer=PostSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    
    def patch(self,r,id=None):
        posts=Post.objects.get(id=id)
        serializer=PostSerializer(posts,data=r.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"msg":"not updated","error":serializer.errors})
        

    def delete(self,r,id=None):
        posts=Post.objects.get(id=id)
        posts.delete()
        return Response({"msg":"successfully deleted"})    

         
            
