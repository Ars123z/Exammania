from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("profile/", views.profile, name="profile"),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('subscribe/<str:subscription_type>/', views.subscribe, name='subscribe'),
    path('join/', views.join, name="join"),
    path('subscription-redirect/', views.success, name= "subscription_redirect"),
    path('about-us/', views.about_us, name="about_us"),
    path('contact-us/', views.contact_us, name="contact_us"),
    path('terms-of-use/', views.terms_of_use, name="terms_of_use"),
    path('privacy-policy/', views.privacy_policy, name="privacy_policy"),
]