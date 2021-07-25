from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from blog.models import Post, Category, BlogComment
from blog.templatetags import extras

# Create your views here.

def home(request):

    allPosts = Post.objects.all().order_by('-id')

    context = {
        'allPosts': allPosts
    }

    return render(request, 'blog/blogHome.html', context)

def category(request, slug):

    category = get_object_or_404(Category, slug=slug)
    allPosts = Post.objects.filter(category=category).order_by('-id')

    context = {
        "category": category,
        "allPosts": allPosts,
        "user": request.user,
    }

    return render(request, 'blog/category.html', context)

def blogPost(request, slug):

    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None).order_by('-id')
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    repDict = {}

    for reply in replies:
        if reply.parent.id not in repDict.keys():
            repDict[reply.parent.id] = [reply]
        else:
            repDict[reply.parent.id].append(reply)

    context = {
        "post": post,
        "comments": comments,
        "repDict": repDict
    }

    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postId = request.POST.get("postId") 
        post = Post.objects.get(id=postId)
        parentId = request.POST.get("parentId")

        if len(comment) < 4:
            messages.error(request, "Comment must be 5 or more characters")
            return redirect(f"/blog/{post.slug}")

        if len(comment) > 100:
            messages.error(request, "Comment must be under 100 characters")
            return redirect(f"/blog/{post.slug}")

        if parentId == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:    
            parent = BlogComment.objects.get(id=parentId)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    return redirect(f"/blog/{post.slug}")