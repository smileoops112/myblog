from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import MainView, PostDetailView, SignUpView, SignInView, SuccessView, FeedBackView, SearchResultsView

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('blog/<slug>/', PostDetailView.as_view(), name='detail_post'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('sign_in/', SignInView.as_view(), name='sign_in'),
    path('sign_out/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='sign_out'),
    path('contacts/', FeedBackView.as_view(), name='contacts'),
    path('contacts/success/', SuccessView.as_view(), name='success'),
    path('search/', SearchResultsView.as_view(), name='search'),
]