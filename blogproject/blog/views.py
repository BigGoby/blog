import markdown
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm
# Create your views here.
from blog.models import Post, Category, Tag
from django.views.generic import ListView,DetailView

'''
def index(request):
    post_list = Post.objects.all()

    return render(request,'blog/index.html',context={'post_list':post_list})
 
 
 def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request,'blog/index.html',context={'post_list':post_list})

def archives(request,year,month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month)
    return render(request,'blog/index.html',context={'post_list':post_list})
 
'''
#对于这种获取某个表的列表数据的，就用ListView类视图
class IndexView(ListView):
    #model:告诉django要获取哪个模型类的数据，就是获取哪个表的数据
    model = Post
    #指定要渲染的模板
    template_name = 'blog/index.html'
    #获取数据的变量名，这个变量会传递给模板
    context_object_name = 'post_list'
    #类视图帮我们分页逻辑，通过paginate_by指定每页的数量
    paginate_by = 3


class CategoryView(IndexView):
    #和IndexView不用的地方是，我们覆写了父类的get_queryset方法
    #该方法默认获取全部的数据
    #我们只需要获取指定分类下的数据，所以，我们改变的它的默认行为
    #在类视图中，从URL获取的参数值会自动保存在实例的kwargs属性中
    #kwargs是一个字典，args属性是一个列表
    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)


class ArchivesView(IndexView):
    def get_queryset(self):
        return super().get_queryset().filter(
            created_time__year = self.kwargs.get('year'),
            created_time__month=self.kwargs.get('month'),
        )
'''
listview总结：
1、listview主要用在获取某个model列表中
2、通过template_name属性来指定需要渲染的模板，通过
context_object_name属性来制定需要获取的model列表的名字
3、复写 get_queryset 方法以增加获取model列表的其他逻辑
4、复写get_context_data方法来为上下文对象添加额外的变量以便在模板中访问

'''





'''
def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    #阅读量
    post.increase_views()

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])


    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post':post,
               'form':form,
               'comment_list':comment_list}
    return render(request,'blog/detail.html',context=context)

'''

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    #先调用父类的get方法，是因为只有当get方法被调用后，
    # 才有self.object属性，
    # 这个属性就是Post模型的实例
    def get(self, request, *args, **kwargs):

        response = super().get(request,*args,**kwargs)

        self.object.increase_views()

        return response

    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    #覆写get_context_data是因为要添加出了post传递的值以外，
    #还需要把评论和表单的内容传递给模板，
    #往context里面添加内容
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({'form':form,
                        'comment_list':comment_list
                        })
        return context

'''
detailview总结:
detailview用来获取某个model中的单个对象
通过template_name属性来指定需要渲染的模板，通过
context_object_name来指定获取的model对象的名字，
复写get_object方法来增加获取对象的其他逻辑
复写get_context_data方法来为上下文对象添加额外的变量，来在模板中访问


'''


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tag)
