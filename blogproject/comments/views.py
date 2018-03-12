from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm

# Create your views here.

def post_comment(request,post_pk):

    post = get_object_or_404(Post,pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            #redirect函数可以接收URL作为参数，也接收一个模型的实例，会调用实例的get_absolute_url
            #会根据get_absolute_url方法返回的url值进行重定向
            return redirect(post)

        else:
            comment_list = post.comment_set.all()
            context = {'post':post,
                       'form':form,
                       'comment_list':comment_list
                       }
            return render(request,'blog/detail.html',context=context)
    else:
        return redirect(post)