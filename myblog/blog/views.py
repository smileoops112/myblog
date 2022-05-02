from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.http.response import HttpResponseRedirect, HttpResponse
from django.views import View
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from taggit.models import Tag
from .models import Post, Comment
from .forms import SignUpForm, SignInForm, FeedBackForm, CommentForm
# Create your views here.


class MainView(View):

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/home.html', context={'page_obj': page_obj})


class PostDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        common_tags = Post.tag.most_common()
        last_posts = Post.objects.all().order_by('id')[:5]
        comment_form = CommentForm()
        return render(request, 'blog/post_detail.html', context={
            'post': post,
            'common_tags': common_tags,
            'last_post': last_posts,
            'comment_form': comment_form
        })

    def post(self, request, slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST['text']
            username = self.request.user
            post = get_object_or_404(Post, url=slug)
            comment = Comment.object.create(post=post, username=username, text=text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'blog/post_detail.html', context={'comment_form': comment_form})


class SignUpView(View):

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'blog/sign_up.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'blog/sign_up.html', context={'form': form})


class SignInView(View):

    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'blog/signin.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'blog/signin.html', context={'form': form})


class FeedBackView(View):

    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        return render(request, 'blog/contacts.html', context={'form': form, 'title': 'Write me'})

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                send_mail(f'From {name} | {subject}', message, from_email, ['asdasdasd@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Nevalidniy zagolovok')
            return HttpResponseRedirect('success')
        return render(request, 'blog/contacts.html', context={'form': form})


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/success.html', context={'title': 'sps'})


class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        results = ''
        query = self.request.GET.get('q')
        if query:
            results = Post.objects.filter(
                Q(h1__icontains=query) | Q(content__icontains=query)
            )
        paginator = Paginator(results, 6)
        page_number = request.GET.get('page')
        paginator_obj = paginator.get_page(page_number)
        return render(request, 'blog/search.html', context={
            'results': paginator_obj,
            'count': paginator.count,
            'title': 'Поиск'
        })


class TagView(View):

    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag)
        common_tags = Post.tag.most_common()
        return render(request, 'blog/tag.html', context={
            'posts': posts,
            'common_tags': common_tags,
            'title': f'#tag {tag}'
        })