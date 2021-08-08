from django.shortcuts import redirect, render,get_object_or_404
from .models import Post,Comments
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .forms import  Mailform,CommentsForm
import yagmail
from taggit.models import Tag
from django.contrib.auth.models import User
# Create your views here.
def post_list_view(request,slug=None):
    post_list=Post.objects.all()
    tag=None
    if slug:
        tag=get_object_or_404(Tag,slug=slug)
        post_list=post_list.filter(body__contains=slug)
    paginator=Paginator(post_list,2)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'post_list.html',{'postlist':post_list,'tag':tag})

def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    comments=post.comments.filter(active=True)
    
    csubmit=False
    form=CommentsForm()
    if request.method=='POST':
        form=CommentsForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.post=post
            form.save()
            csubmit=True
            form=CommentsForm()
            redirect('/year/month/day/post')
    else:
        form=CommentsForm
    return render(request,'post_detail.html',{'post':post,'csubmit':csubmit,'comments':comments,'form':form})

def mail_view(request,id):
    form=Mailform()
    sent=False
    send=''
    if request.method=='POST':
        post=get_object_or_404(Post,pk=id)
        form=Mailform(request.POST)
        if form.is_valid:
            yag = yagmail.SMTP(user='bhaskarabcchauhan@gmail.com', password='fpqxugswlsgmmuur')
            to=request.POST['to']
            name=request.POST['name']           
            subject='{} recommends you to read {}'.format(name,post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message='Read post at {}'.format(post_url)     
            yag.send(to,subject,message)
            sent=True
            send='Email Sent Successfully!!'
    return render(request,'mail.html',{'form':form,'send':send,'sent':sent})