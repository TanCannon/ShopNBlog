from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='blogHome'),
    path('blogpost/<int:id>',views.blogpost,name='blogPost'),
    path('search/',views.search,name='searchPost'),
    path('signup/',views.handelSignup,name='signup'),
    path('login/',views.handelLogin,name='login'),
    path('logout/',views.handelLogout,name='logout'),
    path('postcomment/',views.postComment,name='postComment')
]