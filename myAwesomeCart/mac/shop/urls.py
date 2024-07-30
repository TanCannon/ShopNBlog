from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="shopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/",views.contact, name="contact"),
    path("search/",views.search, name="search"),
    path("tracker/",views.tracker, name="tracker"),
    path("productview/<int:myid>",views.productView, name="productView"),
    path("checkout/",views.checkout, name="checkout"),
    path('login/',views.handelLogin,name='login'),
    path('logout/',views.handelLogout,name='logout'),
    path('signup/',views.handelSignup,name='signup')
]