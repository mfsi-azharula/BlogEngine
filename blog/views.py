"""
    @author:Mindfire
    @dateCreated:
    View file fetch all the details from data base and shows data in the template
"""
import time
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from calendar import month_name
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.forms import ModelForm
from blog.models import *

class CommentForm(ModelForm):

    """
    Class  for call model form for coment section
    """
    class Meta:

        model = Comment
        exclude = ["post"]

def add_comment(request, pk):

    """
    Function for Add a new comment.
    """

    p = request.POST

    if p.has_key("body") and p["body"]:
        author = "Anonymous"

        if p["author"]: author = p["author"]

        comment = Comment(post=Post.objects.get(pk=pk))
        cf = CommentForm(p, instance=comment)
        cf.fields["author"].required = False
        comment = cf.save(commit=False)
        comment.author = author
        comment.save()

    return HttpResponseRedirect(reverse("blog:post", args=[pk]))
		
def delete_comment(request, post_pk, pk=None):

    """
    Delete comment(s) with primary key `pk` or with pks in POST.
    """

    if request.user.is_staff:
        if not pk: pklst = request.POST.getlist("delete")
        else: pklst = [pk]

        for pk in pklst:
            Comment.objects.get(pk=pk).delete()

        return HttpResponseRedirect(reverse("blog:post", args=[post_pk]))	

def main(request):

    """
    Main function for get the details of blog home page.
    """

    posts = Post.objects.all().order_by("-created")
    paginator = Paginator(posts, 4)

    try: 
        page = int(request.GET.get("page", '1'))
    except ValueError: 
        page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response("list.html", dict(posts=posts, user=request.user))

def post(request, pk):

    """
    Function for single post with comments and a comment form.
    """

    post = Post.objects.get(pk=int(pk))
    comments = Comment.objects.filter(post=post)
    d = dict(post=post, comments=comments, form=CommentForm(), user=request.user)
    d.update(csrf(request))

    return render_to_response("post.html", d)