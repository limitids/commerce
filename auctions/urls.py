from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create',views.create,name="create"),
    path('listing/<int:listing>',views.listing,name='listing'),
    path("watchlist", views.watchlist, name="watchlist"),
    path('category',views.categories, name="categories"),
    path ('category/<str:category>', views.category,name="category")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)