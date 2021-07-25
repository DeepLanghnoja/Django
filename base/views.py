from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Contact
from blog.models import Post

# Pages

def home(request):

    allPosts = Post.objects.all().order_by('-id')[:4]

    context = {
        'allPosts': allPosts
    }

    return render(request, 'base/home.html', context)

def about(request):

    context = {
        
    }

    return render(request, 'base/about.html', context)

def contact(request):

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        content = request.POST['content']


        if len(name)<2 or len(email)<3 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")

    context = {
        
    }

    return render(request, 'base/contact.html', context)

def search(request):

    query = request.GET['query']

    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent =  Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__first_name__icontains=query)
        
        allPosts = allPostsTitle.union(allPostsContent).union(allPostsAuthor)

    if allPosts.count() == 0:
        messages.warning(request, "No search result found. Please refind your query.")

    context = {
        "allPosts": allPosts,
        "query": query
    }

    return render(request, 'base/search.html', context)


# Authentication

def handleSignup(request):

    if request.method == 'POST':
        # Get the post parameteres
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for erroneous inputs
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('base-home')
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('base-home')
        if pass1 != pass2:
            messages.success(request, "Password do not match")
            return redirect('base-home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been successfully created.")
        return redirect('base-home')
        
    else:
        return HttpResponse('404-Not Found')

def handleLogin(request):

    if request.method == 'POST':
        # Get the post parameteres
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in....")
            return redirect('base-home')
        else:
            messages.error(request, "invalid credentials, please try again")
            return redirect('base-home')

    return HttpResponse('404-not found')

def handleLogout(request):

    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('base-home')


def handleAuthor(request, first_name):

    author = get_object_or_404(User, first_name=first_name)
    allPosts = Post.objects.filter(author=author).order_by('-id')

    context = {
        "author": author,
        "allPosts": allPosts
    }

    return render(request, 'base/user.html', context)

