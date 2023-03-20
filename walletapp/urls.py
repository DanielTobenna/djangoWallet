from django.urls import path

from . import views

urlpatterns=[
	path('', views.home, name='home'),
	path('signin/', views.signin, name='signin'),
	path('signup/', views.signup, name='signup'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('recieve/', views.create_invoice, name='recieve'),
	path('withdraw/', views.withdraw, name='withdraw'),
	path('account_settings/', views.account_settings, name='account_settings'),
	path('logout/', views.logoutuser, name='logout'),
	path('faq/', views.faq, name='faq'),
	path('about/', views.about, name='about'),
	path('sitemap/', views.sitemap, name='sitemap'),
	path('services/', views.services, name='services'),
	path('careers/', views.careers, name='careers'),
	path('privacy/', views.privacy, name='privacy'),
	path('contact/', views.contact, name='contact'),
	path('terms/', views.terms, name='terms'),
	path('earn/', views.earn, name='earn'),
	path('swap/', views.swap, name='swap'),
	path('moreswap/', views.moreswap, name='moreswap'),
	path('tokenswap/', views.tokenswap, name='tokenswap'),
	path('confirm_deposit/', views.confirm_deposit, name='confirm_deposit' ),
	path('update_payment/<str:pk>/', views.update_payment, name='update_payment' ),
]