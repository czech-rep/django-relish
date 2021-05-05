from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.http import HttpResponse # thats for returning plain text, like:
    # return HttpResponse("return this string")

# posts = [
#     {
#         'author': 'Adam Czech',
#         'title': 'Blog pst 1',
#         'content': 'jestem blogerem 1',
#         'date': 'Aug 08 2020'
#     },
#     {
#         'author': 'Gabi CZ',
#         'title': 'Blog pst 2',
#         'content': 'jestem z mazzur',
#         'date': 'Aug 06 2020'
#     }
# ]


def home(request):
    # return HttpResponse('<h1>Blog home</h>')
    # return HttpResponse('aaa')
    # HttpResponse is a base method. render returns it with html template combined with contex
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title':'about'})

from users.forms import YourNameForm # we get here just a CharField, wow
def name(request):
    if request.method == 'POST':
        return HttpResponse(f'zwrocono postem: costam')
    if request.method == 'GET':
        return HttpResponse(f'zwrocono getem')
    name_form = YourNameForm()
    return render(request, 'blog/name.html', {'form': name_form}) 


# here we'll test using embedded class views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # for authertication. we'll inherit it
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # overwrite default template path
    context_object_name = 'posts'
    ordering = ['-date_posted'] # '-' reverts ordering
    paginate_by = 5


class PostDetailView(DetailView): # mind the order !
    model = Post
    # styles used:
# <a class="btn btn-secondary btn-sm mt-1 mb-1" href="{% url 'post-update' post.id %}">Update</a>
# mt margin top, mb margin bottom

class PostCreateView(LoginRequiredMixin, CreateView): # intrestingly, by default is looks for template post_form
    model = Post                # made by coping register
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
            # intrestingly, by default is looks for template post_form
    model = Post                 # made the template by coping register
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user # provide user to post model # tak na prawdę to nie rozumiem
        return super().form_valid(form)

    def test_func(self):
        # UserPassesTestMixin = Deny a request with a permission error 
        # if the test_func() method returns False.
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post # expects template post_confirm_delete
    success_url = '/'

    def test_func(self):
        # UserPassesTestMixin = Deny a request with a permission error 
        # if the test_func() method returns False.
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # overwrite default template path
    context_object_name = 'posts'
    ordering = ['-date_posted'] 
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# lets try to create endpoint that returns json about certain user
import json
def user_data(request):
    context = {
        'username' : request.user.username # so, data about usr somehow is in request
        , 'id' : request.user.id
        , 'place' : 'warsaw'
    }
    return HttpResponse( json.dumps(context, indent = 4 ))

# lets create an endpoint, sort of rest service, that returns us last posted post
from django.contrib.auth.decorators import login_required   
@login_required
def last_posted(request):
    latest = Post.objects.order_by('-date_posted').first()
    context = {
        'title' : latest.title
        , 'author' : latest.author.username
        , 'content' : latest.content
    }
    return HttpResponse( json.dumps(context, indent = 4 ))


@login_required
def post_by_id(request, post_id):
    # latest = Post.objects.filter(id=post_id).first()
    latest = Post.objects.get(id=post_id)
    context = {
        'title' : latest.title
        , 'author' : latest.author.username
        , 'content' : latest.content
    }
    return HttpResponse( json.dumps(context, indent = 4 ))


# If you just need some views not to use CSRF, you can use @csrf_exempt:
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def post_post(request):
    if request.method == 'POST':
        print('posted')
        print(request.POST.get('title'))
        return HttpResponse(request.POST)
    return HttpResponse('getujesz mnie')


@csrf_exempt
def add_post_ex(request):
    if request.method == 'POST':
        # title, post = request.POST.get('title'), request.POST.get('post') # returns request dictionary # when providing dictionary
        
        # print(json_data['title'])
        # data = request.POST # may not work when form data is required
        print(request.headers)
        data = request.body
        print(data)
        json_data = json.loads(data)
        print(' tytul:  ' + json_data['title'])
        return HttpResponse('elo elo')
    return render(request, 'blog/post_form_ex.html')

import sys # for exception message
def posting_stack(request):
    # endpoint gives access to last post posted, u can either pop or append
    # post - data must consist of title, 
    if request.method == 'POST':
        data = json.loads(request.body)
        # if data['title'] == None:
        #     return HttpResponse('title must not be empty')
        p_author = User.objects.filter(username=data['author']).first() # author field contains id from users table
        print('id: '+str(p_author.id))
        p = Post(title=data['title'], content=data['content'], author=p_author)
        try:
            p.save()
        except:
            return HttpResponse(sys.exc_info()[0])
        return HttpResponse('post successfully added')

    return HttpResponse('endpoint for adding post ')

def error_page(request, err_msg):
    args = {
        'err_msg': err_msg
    }
    return render(request, 'blog/error_page.html', args)