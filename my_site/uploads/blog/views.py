from datetime import date
from typing import Any
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Post
from django.views.generic import ListView,DetailView
from .forms import Commentform
from django.views import View
from django.urls import reverse

# all_posts = [
#     {
#         "slug": "hike-in-the-mountains",
#         "image": "mountains.jpg",
#         "author": "Maximilian",
#         "date": date(2021, 7, 21),
#         "title": "Mountain Hiking",
#         "excerpt": "There's nothing like the views you get when hiking in the mountains! And I wasn't even prepared for what happened whilst I was enjoying the view!",
#         "content": """
#           Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#           aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#           velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

#           Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#           aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#           velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

#           Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#           aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#           velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.
#         """
#     },
#     {
#         "slug": "programming-is-fun",
#         "image": "coding.jpg",
#         "author": "Maximilian",
#         "date": date(2022, 3, 10),
#         "title": "Programming Is Great!",
#         "excerpt": "Did you ever spend hours searching that one error in your code? Yep - that's what happened to me yesterday...",
#         "content": """
#           Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#           aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#           velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

#           Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#           aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#           velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

#           Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#           aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#           velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.
#         """
#     },
#     {
#         "slug": "into-the-woods",
#         "image": "woods.jpg",
#         "author": "Maximilian",
#         "date": date(2020, 8, 5),
#         "title": "Nature At Its Best",
#         "excerpt": "Nature is amazing! The amount of inspiration I get when walking in nature is incredible!",
#         "content": """
#           Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#           aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#           velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

#           Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#           aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#           velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

#           Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
#           aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
#           velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.
#         """
#     }
#  ]


# def starting_page(request):
#     # all_posts.sort(key=func)
#     # latest_posts=all_posts[-3:]
#     latest_posts=Post.objects.all().order_by('-date')[:3]
#     return render(request,"blog/index.html",{'posts':latest_posts})

class starting_page(ListView):
    template_name= "blog/index.html"
    model=Post
    context_object_name='posts'
    ordering=['-date']

    def get_queryset(self):
        context= super().get_queryset()
        data=context[:3]
        return data
    
        

# def posts(request):
#     all_posts=Post.objects.all()
#     return render(request, "blog/all-post.html",{'posts':all_posts} )

class posts(ListView):
    template_name= "blog/all-post.html"
    model=Post
    context_object_name='posts'
    ordering=['-date']

# def post_detail(request,slug):
#     x=get_object_or_404(Post,slug=slug)
#     tags=x.tag.all()
#     return render(request,"blog/post-details.html",{'post':x,'tags':tags} )

class post_detail(View):

    def is_save(self,request,post_id):
        stored_posts=request.session.get("stored_posts")
        if stored_posts is not None:
            saved= post_id in stored_posts
        else:
            saved=False
        return saved

    def get(self,request,slug):
        post=Post.objects.get(slug=slug)
        comment_form=Commentform()
        tags=post.tag.all()
        context={
            'post':post,
            'comment_form':comment_form,
            'tags':tags,
            'comment':post.comments.all(),
            'saved':self.is_save(request,post.id)
        }
        return render(request,"blog/post-details.html",context)
    def post(self,request,slug):
        comment_form=Commentform(request.POST)
        post=Post.objects.get(slug=slug)
        
        if comment_form.is_valid():
            comment=comment_form.save(commit=False)
            comment.post=post
            comment.save()

            return HttpResponseRedirect(reverse("post-detail-page",args=[slug]))
        context={
            'post':post,
            'comment_form':comment_form,
            'tags':post.tag.all(),
            'comment':post.comments.all(),
            'saved':self.is_save(request,post.id)
        }
        return render(request,"blog/post-details.html",context)
    
class Read_later(View):
    def get(self,request):
        stored_posts=request.session.get("stored_posts")
        context={}
        if stored_posts is None:
            context['posts']=[]
            context['has_post']=False
        else:
            post=Post.objects.filter(id__in=stored_posts)
            context['posts']=post
            context['has_post']=True
        return render(request,"blog/stored_post.html",context)

    def post(self,request):
        stored_posts=request.session.get("stored_posts")
        if stored_posts is  None:
            stored_posts=[]
        post_id=int(request.POST['post_id'])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"]=stored_posts
        return HttpResponseRedirect("/")





