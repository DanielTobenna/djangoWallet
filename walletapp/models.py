from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
#from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class Customer(models.Model):
	user= models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
	username= models.CharField(max_length=200, null=True)
	firstname= models.CharField(max_length=200, default='Please fill me', null=True, blank=True)
	Lastname= models.CharField(max_length=200, default='Please fill me', null=True, blank=True)
	Address= models.CharField(max_length=200, default='Please fill me', null=True, blank=True)
	Phonenumber= models.CharField(max_length=200, default='Please fill me', null=True, blank=True)
	email= models.CharField(max_length=200, default='Please fill me', null=True, blank=True)
	profile_pic= models.ImageField(default='profile_pic.PNG',null=True, blank=True)
	usdt= models.FloatField(default=0, null=True)
	btc= models.FloatField(default=0, null=True)
	eth= models.FloatField(default=0, null=True)
	dodge= models.FloatField(default=0, null=True)
	trx= models.FloatField(default=0, null=True)
	axs= models.FloatField(default=0, null=True)
	floki= models.FloatField(default=0, null=True)
	busd= models.FloatField(default=0, null=True)
	dash= models.FloatField(default=0, null=True)
	etc= models.FloatField(default=0, null=True)
	xmr= models.FloatField(default=0, null=True)
	bnbbsc= models.FloatField(default=0, null=True)
	shib= models.FloatField(default=0, null=True)
	bch= models.FloatField(default=0, null=True)
	xrp= models.FloatField(default=0, null=True)
	sol= models.FloatField(default=0, null=True)
	ltc= models.FloatField(default=0, null=True)
	dot= models.FloatField(default=0, null=True)
	xlm= models.FloatField(default=0, null=True)
	ada= models.FloatField(default=0, null=True)
	elm= models.FloatField(default=0, null=True)
	pyn= models.FloatField(default=0, null=True)
	rdn= models.FloatField(default=0, null=True)
	ttm= models.FloatField(default=0, null=True)
	date_created= models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.email

	@property
	def profile_picUrl(self):
		try:
			url= self.profile_pic.url
		except:
			url=''
		return url

class Token(models.Model):
	customer= models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
	element= models.FloatField(null=True, blank=True)
	polygon= models.FloatField(null=True, blank=True)
	radon= models.FloatField(null=True, blank=True)
	tetim= models.FloatField(null=True, blank=True)

	def __str__(self):
		return self.customer.email

class Token_price(models.Model):
	element_price= models.FloatField(null=True, blank=True)
	polygon_price= models.FloatField(null=True, blank=True)
	radon_price= models.FloatField(null=True, blank=True)
	tetim_price= models.FloatField(null=True, blank=True)

	def __int__(self):
		return self.element_price


class Payment_id(models.Model):
	Status= (

		('Successful', 'Successful'),

		('Failed', 'Failed'),

		('Pending', 'Pending'),

	)
	customer= models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
	payment_id= models.CharField(max_length=200, null=True)
	price_amount= models.CharField(max_length=200, null=True)
	price_currency= models.CharField(max_length=200, null=True)
	commodity= models.CharField(max_length=200, null=True)
	transaction_status= models.CharField(max_length=200, null=True, choices=Status, default='Pending')
	date_created= models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.customer.email
