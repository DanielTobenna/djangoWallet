from django.shortcuts import render, redirect, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
import cryptocompare
#imported cryptocompare to get the amount for each crypto
from .forms import *
import json
import requests

# Create your views here.
def home(request):
	return render(request, 'walletapp/home.html')

def signin(request):
	if request.user.is_authenticated:
		return redirect('dashboard')

	else:
		if request.method == "POST":
			email= request.POST.get('email')
			password= request.POST.get('password')

			user= authenticate(request, email=email, password=password)

			if user is not None:
				template= render_to_string('walletapp/loginAlert.html', {'name':email})
				plain_message= strip_tags(template)
				email_message= EmailMultiAlternatives(
					'Login alert on your account!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[email]

					)
				email_message.attach_alternative(template, 'text/html')
				email_message.send()
				login(request, user)
				return redirect('dashboard')

			else:
				messages.error(request, "Email or password is incorrect")

	context={}
	return render(request, 'walletapp/login.html')

def signup(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	form = UserAdminCreationForm()
	if request.method=='POST':
		form=UserAdminCreationForm(request.POST)
		if form.is_valid():
			user=form.save()
			email= form.cleaned_data.get('email')
			messages.success(request, "Account was created for " + email)
			template= render_to_string('walletapp/email_template.html', {'name': email,})
			emailmessage= EmailMessage(
				'Welcome to Bluechipcrypto-exchange!',
				template,
				settings.EMAIL_HOST_USER,
				[email],
				)
			emailmessage.fail_silently=False
			emailmessage.send()
			Customer.objects.create(
				user=user,
				email= user.email,
				)
			return redirect('signin')
	return render(request, 'walletapp/signup.html', {'form':form})

@login_required(login_url='signin')
def dashboard(request):
	customer= request.user.customer
	customer_token= customer.token_set.all()
	customer_pk= customer.pk
	customer_email= customer.email
	customerUsdt= customer.usdt
	customerbtc= customer.btc
	customereth= customer.eth
	customerdodge= customer.dodge
	customertrx= customer.trx
	customersol= customer.sol
	customerltc= customer.ltc
	customerdot= customer.dot
	customerxlm= customer.xlm
	customerada= customer.ada
	customerelm= customer.elm
	customerpyn= customer.pyn
	customerrdn= customer.rdn
	customerttm= customer.ttm
	customeraxs= customer.axs
	customerfloki= customer.floki
	customerbusd= customer.busd
	customerdash= customer.dash
	customeretc= customer.etc
	customerxmr= customer.xmr
	customerbnbbsc= customer.bnbbsc
	customershib= customer.shib
	customerbch= customer.bch
	customerxrp= customer.xrp

	#used cryptocompare to get prices of coins and divided customers coin balance by it
	xrp_price= cryptocompare.get_price('XRP', 'USD')
	xr_price= xrp_price['XRP']['USD']
	customer_xrp_wallet= float(customerxrp)/float(xr_price)
	customer_xrp= round(customer_xrp_wallet, 4)

	axs_price= cryptocompare.get_price('AXS', 'USD')
	ax_price= axs_price['AXS']['USD']
	customer_axs_wallet= float(customeraxs)/float(ax_price)
	customer_axs= round(customer_axs_wallet, 4)

	floki_price= cryptocompare.get_price('FLOKI', 'USD')
	flok_price= floki_price['FLOKI']['USD']
	customer_floki_wallet= float(customerfloki)/float(flok_price)
	customer_floki= round(customer_floki_wallet, 4)

	busd_price= cryptocompare.get_price('BUSD', 'USD')
	bus_price= busd_price['BUSD']['USD']
	customer_busd_wallet= float(customerbusd)/float(bus_price)
	customer_busd= round(customer_busd_wallet, 4)

	dash_price= cryptocompare.get_price('DASH', 'USD')
	das_price= dash_price['DASH']['USD']
	customer_dash_wallet= float(customerdash)/float(das_price)
	customer_dash= round(customer_dash_wallet, 4)

	etc_price= cryptocompare.get_price('ETC', 'USD')
	et_price= etc_price['ETC']['USD']
	customer_etc_wallet= float(customeretc)/float(et_price)
	customer_etc= round(customer_etc_wallet, 4)

	xmr_price= cryptocompare.get_price('XMR', 'USD')
	xm_price= xmr_price['XMR']['USD']
	customer_xmr_wallet= float(customerxmr)/float(xm_price)
	customer_xmr= round(customer_xmr_wallet, 4)

	bch_price= cryptocompare.get_price('BCH', 'USD')
	bc_price= bch_price['BCH']['USD']
	customer_bch_wallet= float(customerbch)/float(bc_price)
	customer_bch= round(customer_bch_wallet, 4)

	shib_price= cryptocompare.get_price('SHIB', 'USD')
	shibainu_price= shib_price['SHIB']['USD']
	customer_shib_wallet= float(customershib)/float(shibainu_price)
	customer_shib= round(customer_shib_wallet, 4)

	bnbbsc_price= cryptocompare.get_price('BNB', 'USD')
	bnb_price= bnbbsc_price['BNB']['USD']
	customer_bnb_wallet= float(customerbnbbsc)/float(bnb_price)
	customer_bnb= round(customer_bnb_wallet, 4)


	bitcoin_price= cryptocompare.get_price('BTC', 'USD')
	btc_price= bitcoin_price['BTC']['USD']
	customer_bitcoin_wallet= float(customerbtc)/ float(btc_price)
	customer_bitcoin= round(customer_bitcoin_wallet, 4)

	usdt_price= cryptocompare.get_price('USDT', 'USD')
	usd_price= usdt_price['USDT']['USD']
	customer_Usdt_wallet= float(customerUsdt)/float(usd_price)
	customer_Usdt= round(customer_Usdt_wallet, 4)

	eth_price= cryptocompare.get_price('ETH', 'USD')
	ethereum_price= eth_price['ETH']['USD']
	customer_eth_wallet= float(customereth)/float(ethereum_price)
	customer_eth= round(customer_eth_wallet, 4)

	doge_price= cryptocompare.get_price('DOGE', 'USD')
	my_doge_price= doge_price['DOGE']['USD']
	customer_doge_wallet= float(customerdodge)/float(my_doge_price)
	customer_doge= round(customer_doge_wallet, 4)

	trx_price= cryptocompare.get_price('TRX', 'USD')
	tron_price= trx_price['TRX']['USD']
	tron_wallet= float(customertrx)/float(tron_price)
	customer_trx= round(tron_wallet, 4)

	sol_price= cryptocompare.get_price('SOL', 'USD')
	solana_price= sol_price['SOL']['USD']
	solana_wallet= float(customersol)/float(solana_price)
	customer_sol= round(solana_wallet, 4)

	ltc_price= cryptocompare.get_price('LTC', 'USD')
	litecoin_price= ltc_price['LTC']['USD']
	litecoin_wallet= float(customerltc)/float(litecoin_price)
	customer_ltc= round(litecoin_wallet, 4)

	dot_price= cryptocompare.get_price('DOT', 'USD')
	polkadot_price= dot_price['DOT']['USD']
	polkadot_wallet= float(customerdot)/float(polkadot_price)
	customer_dot= round(polkadot_wallet, 4)

	xlm_price= cryptocompare.get_price('XLM', 'USD')
	stellar_price= xlm_price['XLM']['USD']
	stellar_wallet= float(customerxlm)/float(stellar_price)
	customer_xlm= round(stellar_wallet, 4)

	ada_price= cryptocompare.get_price('ADA', 'USD')
	cardano_price= ada_price['ADA']['USD']
	cardano_wallet= float(customerada)/float(cardano_price)
	customer_ada= round(cardano_wallet, 4)

	token_price= Token_price.objects.all()
	last_token_price= token_price.last()
	element_price= last_token_price.element_price
	polygon_price= last_token_price.polygon_price
	radon_price= last_token_price.radon_price
	tetim_price= last_token_price.tetim_price
	print(element_price)
	print(polygon_price)
	print(radon_price)
	print(tetim_price)

	number0fTetim= float(customerttm)/float(tetim_price)
	number0fPolygon= float(customerpyn)/float(polygon_price)
	number0fradon= float(customerrdn)/float(radon_price)
	number0felement= float(customerelm)/float(element_price)

	customer_tetim= round(number0fTetim, 4)
	customer_polygon= round(number0fPolygon, 4)
	customer_radon= round(number0fradon, 4)
	customer_element= round(number0felement, 4)
	print(customer_tetim)
	#start of updated tetim
	updated_customer_tetim= float(customer_tetim)*float(tetim_price)
	#start of updated randon
	updated_customer_randon= float(customer_polygon)*float(radon_price)
	#start of updated polygon
	updated_customer_polygon= float(customer_polygon)*float(polygon_price)
	#start of updated element
	updated_customer_element= float(customer_element)*float(element_price)
	customerInfo= Customer.objects.filter(id=customer_pk)
	update_customer_token= customerInfo.update(ttm=updated_customer_tetim, elm=updated_customer_element, pyn=updated_customer_polygon, rdn=updated_customer_randon)



	total_balance= float(customerUsdt) + float(customerbtc) + float(customereth) + float(customerdodge) + float(customertrx) + float(customersol) + float(customerltc) + float(customerdot) + float(customerxlm) + float(customerada) +float(customeraxs) +float(customerfloki)+float(customerbusd)+float(customerdash)+float(customeretc)+float(customerxmr)+float(customerbnbbsc)+float(customershib)+float(customerbch)+float(customerxrp)
	context={'customerUsdt':customerUsdt, 'customerbtc':customerbtc, 'customereth':customereth,
		'customerdodge':customerdodge, 'customertrx':customertrx, 'customersol':customersol, 'element_price':element_price,
		'customerltc':customerltc, 'customerdot':customerdot, 'customerxlm':customerxlm, 'polygon_price':polygon_price,
		'customerada':customerada,'customer_Usdt':customer_Usdt, 'customer_trx':customer_trx, 'radon_price':radon_price,'customer_etc':customer_etc,'customer_dash':customer_dash,
		'customer_eth':customer_eth,'customer_doge':customer_doge, 'customer_sol':customer_sol, 'tetim_price':tetim_price,'customer_xmr':customer_xmr,'customer_busd':customer_busd,
		'customer_floki':customer_floki,'customer_axs':customer_axs,'customer_xrp':customer_xrp,
		'customer_ltc':customer_ltc, 'customer_dot':customer_dot, 'customer_xlm':customer_xlm, 'customer_ada':customer_ada,'customer_bch':customer_bch,
		 'customer_bitcoin':customer_bitcoin, 'total_balance': total_balance, 'btc_price':btc_price, 'customerelm':customerelm,'customer_shib':customer_shib,
		 'customerpyn':customerpyn, 'customerrdn':customerrdn, 'customerttm':customerttm, 'customer_token':customer_token,'customer_element':customer_element,
		 'customeraxs':customeraxs, 'customerfloki':customerfloki, 'customerbusd':customerbusd, 'customerdash':customerdash,'customer_radon':customer_radon,
		 'customeretc':customeretc, 'customerxmr':customerxmr, 'customerbnbbsc':customerbnbbsc, 'customershib':customershib,'customer_polygon':customer_polygon,
		 'customerbch':customerbch, 'customerxrp':customerxrp, 'xr_price':xr_price, 'ax_price':ax_price, 'flok_price':flok_price, 'customer_tetim':customer_tetim,
		 'bus_price':bus_price, 'das_price':das_price, 'et_price':et_price,'xm_price':xm_price, 'bc_price':bc_price, 'usd_price':usd_price, 'customer_bnb':customer_bnb,
		 'ethereum_price':ethereum_price, 'my_doge_price':my_doge_price,'tron_price':tron_price,'solana_price':solana_price,'litecoin_price':litecoin_price,
		 'shibainu_price':shibainu_price, 'bnb_price':bnb_price, 'polkadot_price':polkadot_price,'stellar_price':stellar_price,'cardano_price':cardano_price,'updated_customer_element':updated_customer_element,
		 'updated_customer_tetim':updated_customer_tetim,'updated_customer_randon':updated_customer_randon,'updated_customer_polygon':updated_customer_polygon,
	}
	return render(request, 'walletapp/dashboard.html', context)

@login_required(login_url='signin')
def create_invoice(request):
	if request.method=='POST':
		customer= request.user.customer
		customer_email= customer.email
		#post data to create invoice for payment
		price_amount= request.POST.get('price_amount')
		price_currency= request.POST.get('price_currency')
		pay_currency= request.POST.get('pay_currency')
		order_id= customer_email
		order_description= "Recieve Crypto"
		if price_amount and pay_currency:
			# Api's url link
			url= 'https://api.nowpayments.io/v1/invoice'
			payload=json.dumps({
				"price_amount": price_amount,
				"price_currency": price_currency,
				"pay_currency": pay_currency,
				"order_id": order_id,
				"order_description": order_description,
				"ipn_callback_url": "https://nowpayments.io",
				"success_url": "https://www.bluechipcrypto-exchange.com/dashboard",
				#our success url will direct us to the get_payment_status view for balance top ups
				"cancel_url": "https://www.bluechipcrypto-exchange.com/dashboard"
			})
			headers={'x-api-key':'', 'Content-Type': 'application/json'}
			response= requests.request('POST', url, headers=headers, data=payload)
			res= response.json()
			generated_link= res['invoice_url']
			generated_payment_id= res["id"]
			#Now get the user and add the payment ID to the database as we will be using it to know their payment status
			Payment_id.objects.create(
				customer=customer,
				payment_id= generated_payment_id,
				price_amount= price_amount,
				price_currency=price_currency,
				commodity= pay_currency,
				)
			template= render_to_string('walletapp/pendingDepositEmail.html', {'name': customer_email, 'amount':price_amount, 'transaction_id':generated_payment_id})
			plain_message= strip_tags(template)
			emailmessage= EmailMultiAlternatives(
				'Pending Deposit Order',
				plain_message,
				settings.EMAIL_HOST_USER,
				[client_email],
				)
			emailmessage.attach_alternative(template, 'text/html')
			emailmessage.send()
			try:
				send_mail(client_name, "A client with email: {} has created a deposit request with an amount ${}".format(customer_email, price_amount),settings.EMAIL_HOST_USER, ['support@bluechipcrypto-exchange.com'])
			except BadHeaderError:
				pass
			return redirect(generated_link)
	context={}
	return render(request, 'walletapp/recieve.html', context)


@login_required(login_url='signin')
def withdraw(request):
	customer= request.user.customer
	customer_name= customer.username
	customer_pk= customer.pk
	customer_email= customer.email
	email= customer_email
	customerUsdt= customer.usdt
	customerbtc= customer.btc
	customereth= customer.eth
	customerdodge= customer.dodge
	customertrx= customer.trx
	customersol= customer.sol
	customerltc= customer.ltc
	customerdot= customer.dot
	customerxlm= customer.xlm
	customerada= customer.ada
	customeraxs= customer.axs
	customerfloki= customer.floki
	customerbusd= customer.busd
	customerdash= customer.dash
	customeretc= customer.etc
	customerxmr= customer.xmr
	customerbnbbsc= customer.bnbbsc
	customershib= customer.shib
	customerbch= customer.bch
	customerxrp= customer.xrp
	if request.method=='POST':
		coin= request.POST.get('coin')
		print(coin)
		receiving_addr= request.POST.get('address')
		preferred_coin= request.POST.get('preferred_coin')
		amount= request.POST.get('amount')
		if coin == 'bnbbsc':
			new_customerBnb= float(customerbnbbsc) - float(amount)
			print(new_customerBnb)
			if new_customerBnb > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(bnbbsc=new_customerBnb)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')

			else:
				return HttpResponse('Insufficent Binance coin balance')

		if coin == 'shib':
			new_customerShib= float(customershib) - float(amount)
			print(new_customerShib)
			if new_customerShib > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(shib=new_customerShib)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')

			else:
				return HttpResponse('Insufficent Shiba Inu balance')
		if coin == 'bch':
			new_customerBch= float(customerbch) - float(amount)
			print(new_customerBch)
			if new_customerBch > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(bch=new_customerBch)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')

			else:
				return HttpResponse('Insufficent BitcoinCash balance')
		if coin == 'xmr':
			new_customerXmr= float(customerxmr) - float(amount)
			print(new_customerXmr)
			if new_customerXmr > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(xmr=new_customerXmr)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')

			else:
				return HttpResponse('Insufficent XMR balance')
		if coin == 'etc':
			new_customerEtc= float(customeretc) - float(amount)
			print(new_customerEtc)
			if new_customerEtc > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(etc=new_customerEtc)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')

			else:
				return HttpResponse('Insufficent Ethereum Classic balance')
		if coin == 'dash':
			new_customerDash= float(customerdash) - float(amount)
			print(new_customerDash)
			if new_customerDash > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(dash=new_customerDash)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')

			else:
				return HttpResponse('Insufficent Dash balance')
		if coin == 'busd':
			new_customerBusd= float(customerbusd) - float(amount)
			print(new_customerBusd)
			if new_customerBusd > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(busd=new_customerBusd)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')

			else:
				return HttpResponse('Insufficent Binance Usd balance')
		if coin == 'floki':
			new_customerFloki= float(customerfloki) - float(amount)
			print(new_customerFloki)
			if new_customerFloki > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(usdt=new_customerFloki)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')

			else:
				return HttpResponse('Insufficent Floki balance')
		if coin == 'xrp':
			new_customerXrp= float(customerxrp) - float(amount)
			print(new_customerXrp)
			if new_customerXrp > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(xrp=new_customerXrp)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')

			else:
				return HttpResponse('Insufficent Xrp balance')
		if coin == 'axs':
			new_customerAxs= float(customeraxs) - float(amount)
			print(new_customerAxs)
			if new_customerAxs > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(axs=new_customerAxs)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')

			else:
				return HttpResponse('Insufficent Axie Infinity balance')
		if coin == 'usdt':
			new_customerUsdt= float(customerUsdt) - float(amount)
			print(new_customerUsdt)
			if new_customerUsdt > 0 and float(amount)>1000:
				customer_info= Customer.objects.filter(id=customer_pk)
				#update_bal= customer_info.update(usdt=new_customerUsdt)
				network_fee= float(amount)/4
				template= render_to_string('walletapp/ethereumNetworkFee.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin, 'network_fee':network_fee })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was not successful because you do not have enough Ethereum for your network fees. The system has sent you an email as to why this happened in details.')

			else:
				return HttpResponse('Your minimum USDT balance must be 1 USDT(ERC 20), and minimum withdrawal amount must be USD 10,000')

		if coin == 'btc':
			new_customerbtc= float(customerbtc) - float(amount)
			print(new_customerbtc)
			if new_customerbtc > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(btc=new_customerbtc)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')
			else:
				return HttpResponse('Insufficent bitcoin balance')

		if coin == 'eth':
			new_customereth= float(customereth) - float(amount)
			print(new_customereth)
			if new_customereth > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(eth=new_customereth)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')
			else:
				return HttpResponse('Insufficent Ethereum balance')

		if coin == 'dodge':
			new_customerdodge= float(customerdodge) - float(amount)
			print(new_customerdodge)
			if new_customerdodge > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(dodge=new_customerdodge)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')
			else:
				return HttpResponse('Insufficent Dodge balance')

		if coin == 'trx':
			new_customertrx= float(customertrx) - float(amount)
			print(new_customertrx)
			if new_customertrx > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(trx=new_customertrx)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')
			else:
				return HttpResponse('Insufficent Tron balance')

		if coin == 'sol':
			new_customersol= float(customersol) - float(amount)
			print(new_customersol)
			if new_customersol > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(sol=new_customersol)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')
			else:
				return HttpResponse('Insufficent Solanar balance')

		if coin == 'ltc':
			new_customerltc= float(customerltc) - float(amount)
			print(new_customerltc)
			if new_customerltc > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(ltc=new_customerltc)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')
			else:
				return HttpResponse('Insufficent Litecoin balance')

		if coin == 'dot':
			new_customerdot= float(customerdot) - float(amount)
			print(new_customerdot)
			if new_customerdot > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(dot=new_customerdot)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')
			else:
				return HttpResponse('Insufficent Polkadot balance')

		if coin == 'xlm':
			new_customerxlm= float(customerxlm) - float(amount)
			print(new_customerxlm)
			if new_customerxlm > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(xlm=new_customerxlm)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')
			else:
				return HttpResponse('Insufficent Stellar balance')

		if coin == 'ada':
			new_customerada= float(customerada) - float(amount)
			print(new_customerada)
			if new_customerada > 0.5:
				customer_info= Customer.objects.filter(id=customer_pk)
				update_bal= customer_info.update(ada=new_customerada)
				template= render_to_string('walletapp/withdrawal_email.html', {'name': customer_name, 'amount':amount, 'receiving_addr':receiving_addr, 'preferred_coin':preferred_coin })
				plain_message= strip_tags(template)

				emailmessage= EmailMultiAlternatives(
					'Your withdrawal has been completed successfully!',
					plain_message,
					settings.EMAIL_HOST_USER,
					[customer_email],
					)
				emailmessage.attach_alternative(template, 'text/html')
				emailmessage.send()
				try:
					send_mail(customer_name, "Your client with the name: {} requested a withdrawal of {}. Their email is {} and wallet address is {}. The coin associated with the address is {}".format(customer_name, amount,email, address, preferred_coin),email, ['support@bluechipcrypto-exchange.com'])
				except BadHeaderError:
					return HttpResponse('Bad Header Error. Please try again later.')

				return HttpResponse('Your withdrawal was successful')
			else:
				return HttpResponse('Insufficent Cardano balance')

	return render(request, 'walletapp/withdraw.html')

@login_required(login_url='signin')
def account_settings(request):

	customer= request.user.customer

	form=CustomerForm(instance=customer)

	if request.method=='POST':
		form= CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()

	context= {"form":form}

	return render(request, 'walletapp/profile.html', context)

@login_required(login_url='signin')
def logoutuser(request):
	logout(request)
	return redirect('signin')

def faq(request):
	return render(request, 'walletapp/faq.html')

def about(request):
	return render(request, 'walletapp/about.html')

def sitemap(request):
	return render(request, 'walletapp/sitemap.xml')

def services(request):
	return render(request, 'walletapp/services.html')

def careers(request):
	return render(request, 'walletapp/careers.html')

def privacy(request):
	return render(request, 'walletapp/privacy.html')

def contact(request):
	if request.method =='POST':
		name= request.POST.get('name')
		email= request.POST.get('email')
		phone= request.POST.get('phone')
		message= request.POST.get('message')
		try:
			send_mail(name, "Your client with the name: {} has sent a message saying: {}. Their email is {} and phone number is {}".format(name, message,email, phone),email, ['support@tetbase.com'])
			return HttpResponse('Thank you for reaching out to us, Your message has been sent successfully')

		except BadHeaderError:
			return HttpResponse('Bad Header Error. Please try again later.')
	return render(request, 'walletapp/contact.html')

def terms(request):
	return render(request, 'walletapp/terms.html')

def earn(request):
	return render(request, 'walletapp/earn.html')

def swap(request):
	customer= request.user.customer
	customer_name= customer.username
	customer_pk= customer.pk
	customer_email= customer.email
	customerUsdt= customer.usdt
	customerbtc= customer.btc
	customereth= customer.eth
	customerdodge= customer.dodge
	customertrx= customer.trx
	customersol= customer.sol
	customerltc= customer.ltc
	customerdot= customer.dot
	customerxlm= customer.xlm
	customerada= customer.ada
	if request.method=='POST':
		base_crypto= request.POST.get('base_currency')
		swap_crypto= request.POST.get('swap')
		amount= request.POST.get('amount')
		if base_crypto=='usdt' and swap_crypto=='btc':
			if float(customerUsdt) > float(amount) and float(amount) > 25:
				new_btc_bal= float(customerbtc)+ float(amount)
				new_usdt_bal= float(customerUsdt)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				#customer_info_update= customer_info.update(btc=new_btc_bal, usdt=new_usdt_bal)
				return HttpResponse('Your coin swap was not successful as you do not have enough Ethereum to complete this transaction.')
			else:
				return HttpResponse('You either do not have sufficent USDT for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='usdt' and swap_crypto=='eth':
			if float(customerUsdt) > float(amount) and float(amount) > 25:
				new_eth_bal= float(customereth)+ float(amount)
				new_usdt_bal= float(customerUsdt)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				#customer_info_update= customer_info.update(eth=new_eth_bal, usdt=new_usdt_bal)
				return HttpResponse('Your coin swap was not successful as you do not have enough Ethereum to complete this transaction.')
			else:
				return HttpResponse('You either do not have sufficent USDT for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='usdt' and swap_crypto=='dodge':
			if float(customerUsdt) > float(amount) and float(amount) > 25:
				new_dodge_bal= float(customerdodge)+ float(amount)
				new_usdt_bal= float(customerUsdt)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				#customer_info_update= customer_info.update(dodge=new_dodge_bal, usdt=new_usdt_bal)
				return HttpResponse('Your coin swap was not successful as you do not have enough Ethereum to complete this transaction.')
			else:
				return HttpResponse('You either do not have sufficent USDT for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='usdt' and swap_crypto=='trx':
			if float(customerUsdt) > float(amount) and float(amount) > 25:
				new_trx_bal= float(customertrx)+ float(amount)
				new_usdt_bal= float(customerUsdt)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				#customer_info_update= customer_info.update(trx=new_trx_bal, usdt=new_usdt_bal)
				return HttpResponse('Your coin swap was not successful as you do not have enough Ethereum to complete this transaction.')
			else:
				return HttpResponse('You either do not have sufficent USDT for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='usdt' and swap_crypto=='sol':
			if float(customerUsdt) > float(amount) and float(amount) > 25:
				new_sol_bal= float(customersol)+ float(amount)
				new_usdt_bal= float(customerUsdt)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				#customer_info_update= customer_info.update(sol=new_sol_bal, usdt=new_usdt_bal)
				return HttpResponse('Your coin swap was not successful as you do not have enough Ethereum to complete this transaction.')
			else:
				return HttpResponse('You either do not have sufficent USDT for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='usdt' and swap_crypto=='ltc':
			if float(customerUsdt) > float(amount) and float(amount) > 25:
				new_ltc_bal= float(customerltc)+ float(amount)
				new_usdt_bal= float(customerUsdt)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				#customer_info_update= customer_info.update(ltc=new_ltc_bal, usdt=new_usdt_bal)
				return HttpResponse('Your coin swap was not successful as you do not have enough Ethereum to complete this transaction.')
			else:
				return HttpResponse('You either do not have sufficent USDT for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='usdt' and swap_crypto=='dot':
			if float(customerUsdt) > float(amount) and float(amount) > 25:
				new_dot_bal= float(customerdot)+ float(amount)
				new_usdt_bal= float(customerUsdt)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				#customer_info_update= customer_info.update(dot=new_dot_bal, usdt=new_usdt_bal)
				return HttpResponse('Your coin swap was not successful as you do not have enough Ethereum to complete this transaction.')
			else:
				return HttpResponse('You either do not have sufficent USDT for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='usdt' and swap_crypto=='xlm':
			if float(customerUsdt) > float(amount) and float(amount) > 25:
				new_xlm_bal= float(customerxlm)+ float(amount)
				new_usdt_bal= float(customerUsdt)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(xlm=new_btc_bal, usdt=new_usdt_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent USDT for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='usdt' and swap_crypto=='ada':
			if float(customerUsdt) > float(amount) and float(amount) > 25:
				new_ada_bal= float(customerada)+ float(amount)
				new_usdt_bal= float(customerUsdt)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				#customer_info_update= customer_info.update(ada=new_btc_bal, usdt=new_usdt_bal)
				return HttpResponse('Your coin swap was not successful as you do not have enough Ethereum to complete this transaction.')
			else:
				return HttpResponse('You either do not have sufficent USDT for this transaction or your swap request is less than 25 USD.')
				#code for usdt swapping ends here

				#code for btc swapping starts here
		if base_crypto=='btc' and swap_crypto=='usdt':
			if float(customerbtc) > float(amount) and float(amount) > 25:
				new_usdt_bal= float(customerusdt)+ float(amount)
				new_btc_bal= float(customerbtc)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				#customer_info_update= customer_info.update(usdt=new_usdt_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was not successful as you do not have enough Ethereum to complete this transaction.')
			else:
				return HttpResponse('You either do not have sufficent BTC for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='btc' and swap_crypto=='eth':
			if float(customerbtc) > float(amount) and float(amount) > 25:
				new_eth_bal= float(customereth)+ float(amount)
				new_btc_bal= float(customerbtc)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(eth=new_eth_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent BTC for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='btc' and swap_crypto=='dodge':
			if float(customerbtc) > float(amount) and float(amount) > 25:
				new_dodge_bal= float(customerdodge)+ float(amount)
				new_btc_bal= float(customerbtc)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(dodge=new_dodge_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent BTC for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='btc' and swap_crypto=='trx':
			if float(customerbtc) > float(amount) and float(amount) > 25:
				new_trx_bal= float(customertrx)+ float(amount)
				new_btc_bal= float(customerbtc)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(trx=new_trx_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent BTC for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='btc' and swap_crypto=='sol':
			if float(customerbtc) > float(amount) and float(amount) > 25:
				new_sol_bal= float(customersol)+ float(amount)
				new_btc_bal= float(customerbtc)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(sol=new_sol_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent BTC for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='btc' and swap_crypto=='ltc':
			if float(customerbtc) > float(amount) and float(amount) > 25:
				new_ltc_bal= float(customerltc)+ float(amount)
				new_btc_bal= float(customerbtc)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(ltc=new_ltc_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent BTC for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='btc' and swap_crypto=='dot':
			if float(customerbtc) > float(amount) and float(amount) > 25:
				new_dot_bal= float(customerdot)+ float(amount)
				new_btc_bal= float(customerbtc)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(dot=new_dot_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent BTC for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='btc' and swap_crypto=='xlm':
			if float(customerbtc) > float(amount) and float(amount) > 25:
				new_xlm_bal= float(customerxlm)+ float(amount)
				new_btc_bal= float(customerbtc)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(xlm=new_xlm_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent BTC for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='btc' and swap_crypto=='ada':
			if float(customerbtc) > float(amount) and float(amount) > 25:
				new_ada_bal= float(customerada)+ float(amount)
				new_btc_bal= float(customerbtc)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(ada=new_ada_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent BTC for this transaction or your swap request is less than 25 USD.')
				#BITCOIN swap ends here
				#Ethereum swap starts here
		if base_crypto=='eth' and swap_crypto=='usdt':
			if float(customereth) > float(amount) and float(amount) > 25:
				new_usdt_bal= float(customerusdt)+ float(amount)
				new_eth_bal= float(customereth)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(usdt=new_usdt_bal, eth=new_eth_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent Ethereum for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='eth' and swap_crypto=='btc':
			if float(customereth) > float(amount) and float(amount) > 25:
				new_btc_bal= float(customerbtc)+ float(amount)
				new_eth_bal= float(customereth)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(btc=new_btc_bal, eth=new_eth_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent Ethereum for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='eth' and swap_crypto=='dodge':
			if float(customereth) > float(amount) and float(amount) > 25:
				new_dodge_bal= float(customerdodge)+ float(amount)
				new_eth_bal= float(customereth)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(dodge=new_dodge_bal, eth=new_eth_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent Ethereum for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='eth' and swap_crypto=='trx':
			if float(customereth) > float(amount) and float(amount) > 25:
				new_trx_bal= float(customertrx)+ float(amount)
				new_eth_bal= float(customereth)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(trx=new_trx_bal, eth=new_eth_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent Ethereum for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='eth' and swap_crypto=='sol':
			if float(customereth) > float(amount) and float(amount) > 25:
				new_sol_bal= float(customersol)+ float(amount)
				new_eth_bal= float(customereth)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(sol=new_sol_bal, eth=new_eth_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent Ethereum for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='eth' and swap_crypto=='ltc':
			if float(customereth) > float(amount) and float(amount) > 25:
				new_ltc_bal= float(customerltc)+ float(amount)
				new_eth_bal= float(customereth)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(ltc=new_ltc_bal, eth=new_eth_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent Ethereum for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='eth' and swap_crypto=='dot':
			if float(customereth) > float(amount) and float(amount) > 25:
				new_dot_bal= float(customerdot)+ float(amount)
				new_eth_bal= float(customereth)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(dot=new_dot_bal, eth=new_eth_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent Ethereum for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='eth' and swap_crypto=='xlm':
			if float(customereth) > float(amount) and float(amount) > 25:
				new_xlm_bal= float(customerxlm)+ float(amount)
				new_eth_bal= float(customereth)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(xlm=new_xlm_bal, eth=new_eth_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent Ethereum for this transaction or your swap request is less than 25 USD.')
		if base_crypto=='eth' and swap_crypto=='ada':
			if float(customereth) > float(amount) and float(amount) > 25:
				new_ada_bal= float(customerada)+ float(amount)
				new_eth_bal= float(customereth)- float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(ada=new_ada_bal, eth=new_eth_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have sufficent Ethereum for this transaction or your swap request is less than 25 USD.')


	return render(request, 'walletapp/swap.html')

@login_required(login_url='signin')
def moreswap(request):
	customer= request.user.customer
	customer_name= customer.username
	customer_pk= customer.pk
	customer_email= customer.email
	customerTotalbalance= customer.total_balance
	customerUsdt= customer.usdt
	customerbtc= customer.btc
	customerelm= customer.elm
	customerpyn= customer.pyn
	customerrdn= customer.rdn
	customerttm= customer.ttm
	if request.method=='POST':
		base_crypto= request.POST.get('base_currency')
		swap_crypto= request.POST.get('swap')
		amount= request.POST.get('amount')
		if base_crypto=='usdt' and swap_crypto=='elm':
			if float(customerUsdt)> float(amount) and float(amount)>15:
				new_elm_bal= float(customerelm) + float(amount)
				new_usdt_bal= float(customerUsdt) - float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				#customer_info_update= customer_info.update(elm=new_elm_bal, usdt=new_usdt_bal)
				return HttpResponse('Your coin swap was not successful as you do not have enough Ethereum to complete this transaction.')
			else:
				return HttpResponse('You either do not have enough USDT for this transaction or your request is less than 15 USD')
		if base_crypto=='usdt' and swap_crypto=='pyn':
			if float(customerUsdt)> float(amount) and float(amount)>15:
				new_pyn_bal= float(customerpyn) + float(amount)
				new_usdt_bal= float(customerUsdt) - float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				#customer_info_update= customer_info.update(pyn=new_pyn_bal, usdt=new_usdt_bal)
				return HttpResponse('Your coin swap was not successful as you do not have enough Ethereum to complete this transaction.')
			else:
				return HttpResponse('You either do not have enough USDT for this transaction or your request is less than 15 USD')
		if base_crypto=='usdt' and swap_crypto=='rdn':
			if float(customerUsdt)> float(amount) and float(amount)>15:
				new_rdn_bal= float(customerrdn) + float(amount)
				new_usdt_bal= float(customerUsdt) - float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				#customer_info_update= customer_info.update(rdn=new_rdn_bal, usdt=new_usdt_bal)
				return HttpResponse('Your coin swap was not successful as you do not have enough Ethereum to complete this transaction.')
			else:
				return HttpResponse('You either do not have enough USDT for this transaction or your request is less than 15 USD')
		if base_crypto=='usdt' and swap_crypto=='ttm':
			if float(customerUsdt)> float(amount) and float(amount)>15:
				new_ttm_bal= float(customerttm) + float(amount)
				new_usdt_bal= float(customerUsdt) - float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				#customer_info_update= customer_info.update(ttm=new_ttm_bal, usdt=new_usdt_bal)
				return HttpResponse('Your coin swap was not successful as you do not have enough Ethereum to complete this transaction.')
			else:
				return HttpResponse('You either do not have enough USDT for this transaction or your request is less than 15 USD')
				#End of usdt swap for tokens
				#start of btc swap for tokens
		if base_crypto=='btc' and swap_crypto=='elm':
			if float(customerbtc)> float(amount) and float(amount)>15:
				new_elm_bal= float(customerelm) + float(amount)
				new_btc_bal= float(customerbtc) - float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(elm=new_elm_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have enough bitcoin for this transaction or your request is less than 15 USD')
		if base_crypto=='btc' and swap_crypto=='pyn':
			if float(customerbtc)> float(amount) and float(amount)>15:
				new_pyn_bal= float(customerpyn) + float(amount)
				new_btc_bal= float(customerbtc) - float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(pyn=new_pyn_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have enough USDT for this transaction or your request is less than 15 USD')
		if base_crypto=='btc' and swap_crypto=='rdn':
			if float(customerbtc)> float(amount) and float(amount)>15:
				new_rdn_bal= float(customerrdn) + float(amount)
				new_btc_bal= float(customerbtc) - float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(rdn=new_rdn_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have enough USDT for this transaction or your request is less than 15 USD')
		if base_crypto=='btc' and swap_crypto=='ttm':
			if float(customerbtc)> float(amount) and float(amount)>15:
				new_ttm_bal= float(customerttm) + float(amount)
				new_btc_bal= float(customerbtc) - float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(ttm=new_ttm_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have enough USDT for this transaction or your request is less than 15 USD')


	return render(request,'walletapp/moreswap.html')

@login_required(login_url='signin')
def tokenswap(request):
	customer= request.user.customer
	customer_name= customer.username
	customer_pk= customer.pk
	customer_email= customer.email
	customerTotalbalance= customer.total_balance
	customerUsdt= customer.usdt
	customerbtc= customer.btc
	customerelm= customer.elm
	customerpyn= customer.pyn
	customerrdn= customer.rdn
	customerttm= customer.ttm
	if request.method=='POST':
		base_crypto= request.POST.get('base_currency')
		swap_crypto= request.POST.get('swap')
		amount= request.POST.get('amount')
		if base_crypto=='elm' and swap_crypto=='btc':
			if float(customerelm)> float(amount) and float(amount)>30:
				new_elm_bal= float(customerelm) - float(amount)
				new_btc_bal= float(customerbtc) + float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(elm=new_elm_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have enough Element for this transaction or your request is less than 30 USD')
		if base_crypto=='pyn' and swap_crypto=='btc':
			if float(customerpyn)> float(amount) and float(amount)>30:
				new_pyn_bal= float(customerpyn) - float(amount)
				new_btc_bal= float(customerbtc) + float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(pyn=new_pyn_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have enough Polygon for this transaction or your request is less than 30 USD')
		if base_crypto=='rdn' and swap_crypto=='btc':
			if float(customerrdn)> float(amount) and float(amount)>30:
				new_rdn_bal= float(customerrdn) - float(amount)
				new_btc_bal= float(customerbtc) + float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(rdn=new_rdn_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have enough Polygon for this transaction or your request is less than 30 USD')
		if base_crypto=='ttm' and swap_crypto=='btc':
			if float(customerttm)> float(amount) and float(amount)>30:
				new_ttm_bal= float(customerttm) - float(amount)
				new_btc_bal= float(customerbtc) + float(amount)
				customer_info= Customer.objects.filter(id=customer_pk)
				customer_info_update= customer_info.update(ttm=new_ttm_bal, btc=new_btc_bal)
				return HttpResponse('Your coin swap was successful.')
			else:
				return HttpResponse('You either do not have enough Tetim for this transaction or your request is less than 30 USD')
	return render(request, 'walletapp/tokenswap.html')

@login_required(login_url='signin')
@staff_member_required
def confirm_deposit(request):
	paymentInfo= Payment_id.objects.all()
	context={'paymentInfo': paymentInfo}
	return render(request, 'walletapp/confirmdeposit.html', context)

@login_required(login_url='signin')
@staff_member_required
def update_payment(request, pk):
	payment_info= Payment_id.objects.get(id=pk)
	customer_id= payment_info.customer.id
	payment_info_id= payment_info.id
	print(customer_id)
	print(payment_info_id)
	customer= Customer.objects.get(pk=customer_id)
	print(customer)
	customer_pk= customer.pk
	customer_email= customer.email
	customerUsdt= customer.usdt
	customerbtc= customer.btc
	customereth= customer.eth
	customerdodge= customer.dodge
	customertrx= customer.trx
	customersol= customer.sol
	customerltc= customer.ltc
	customerdot= customer.dot
	customerxlm= customer.xlm
	customerada= customer.ada
	payment_info= Payment_id.objects.filter(customer=customer)
	last_info= payment_info.last()
	print(last_info)
	pay_id= last_info.payment_id
	amount_paid= last_info.price_amount
	currency_paid= last_info.price_currency
	crypto_to_topup= last_info.commodity
	if payment_info and crypto_to_topup=='USDTERC20':
		new_customerUsdt= float(customerUsdt) + float(amount_paid)
		print(new_customerUsdt)
		customer_info= Customer.objects.filter(id=customer_pk)
		update_bal= customer_info.update(usdt=new_customerUsdt)
		delete_payment_info= last_info.delete()
		template= render_to_string('walletapp/deposit_email.html', {'name': customer_email, 'amount': amount_paid})
		emailmessage= EmailMessage(
			'Congratulations, Your Deposit was successfully made!',
			template,
			settings.EMAIL_HOST_USER,
			[customer_email],
			)
		emailmessage.fail_silently=False
		emailmessage.send()
		return redirect('dashboard')

	if payment_info and crypto_to_topup=='btc':
		new_customerbtc= float(customerbtc) + float(amount_paid)
		print(new_customerbtc)
		customer_info= Customer.objects.filter(id=customer_pk)
		update_bal= customer_info.update(btc=new_customerbtc)
		delete_payment_info= last_info.delete()
		template= render_to_string('walletapp/deposit_email.html', {'name': customer_email, 'amount': amount_paid})
		emailmessage= EmailMessage(
			'Congratulations, Your Deposit was successfully made!',
			template,
			settings.EMAIL_HOST_USER,
			[customer_email],
			)
		emailmessage.fail_silently=False
		emailmessage.send()
		return redirect('dashboard')

	if payment_info and crypto_to_topup=='eth':
		new_customereth= float(customereth) + float(amount_paid)
		print(new_customereth)
		customer_info= Customer.objects.filter(id=customer_pk)
		update_bal= customer_info.update(eth=new_customereth)
		delete_payment_info= last_info.delete()
		template= render_to_string('walletapp/deposit_email.html', {'name': customer_email, 'amount': amount_paid})
		emailmessage= EmailMessage(
			'Congratulations, Your Deposit was successfully made!',
			template,
			settings.EMAIL_HOST_USER,
			[customer_email],
			)
		emailmessage.fail_silently=False
		emailmessage.send()
		return redirect('dashboard')

	if payment_info and crypto_to_topup=='dodge':
		new_customerdodge= float(customertrx) + float(amount_paid)
		print(new_customerdodge)
		customer_info= Customer.objects.filter(id=customer_pk)
		update_bal= customer_info.update(dodge=new_customerUsdt)
		delete_payment_info= last_info.delete()
		template= render_to_string('walletapp/deposit_email.html', {'name': customer_email, 'amount': amount_paid})
		emailmessage= EmailMessage(
			'Congratulations, Your Deposit was successfully made!',
			template,
			settings.EMAIL_HOST_USER,
			[customer_email],
			)
		emailmessage.fail_silently=False
		emailmessage.send()
		return redirect('dashboard')

	if payment_info and crypto_to_topup=='trx':
		new_customertrx= float(customertrx) + float(amount_paid)
		print(new_customertrx)
		customer_info= Customer.objects.filter(id=customer_pk)
		update_bal= customer_info.update(trx=new_customertrx)
		delete_payment_info= last_info.delete()
		template= render_to_string('walletapp/deposit_email.html', {'name': customer_email, 'amount': amount_paid})
		emailmessage= EmailMessage(
			'Congratulations, Your Deposit was successfully made!',
			template,
			settings.EMAIL_HOST_USER,
			[customer_email],
			)
		emailmessage.fail_silently=False
		emailmessage.send()
		return redirect('dashboard')

	if payment_info and crypto_to_topup=='sol':
		new_customersol= float(customersol) + float(amount_paid)
		print(new_customersol)
		customer_info= Customer.objects.filter(id=customer_pk)
		update_bal= customer_info.update(sol=new_customersol)
		delete_payment_info= last_info.delete()
		template= render_to_string('walletapp/deposit_email.html', {'name': customer_email, 'amount': amount_paid})
		emailmessage= EmailMessage(
			'Congratulations, Your Deposit was successfully made!',
			template,
			settings.EMAIL_HOST_USER,
			[customer_email],
			)
		emailmessage.fail_silently=False
		emailmessage.send()
		return redirect('dashboard')

	if payment_info and crypto_to_topup=='ltc':
		new_customerltc= float(customerltc) + float(amount_paid)
		print(new_customerltc)
		customer_info= Customer.objects.filter(id=customer_pk)
		update_bal= customer_info.update(ltc=new_customerltc)
		delete_payment_info= last_info.delete()
		template= render_to_string('walletapp/deposit_email.html', {'name': customer_email, 'amount': amount_paid})
		emailmessage= EmailMessage(
			'Congratulations, Your Deposit was successfully made!',
			template,
			settings.EMAIL_HOST_USER,
			[customer_email],
			)
		emailmessage.fail_silently=False
		emailmessage.send()
		return redirect('dashboard')

	if payment_info and crypto_to_topup=='dot':
		new_customerdott= float(customerdot) + float(amount_paid)
		print(new_customerdot)
		customer_info= Customer.objects.filter(id=customer_pk)
		update_bal= customer_info.update(dot=new_customerdot)
		delete_payment_info= last_info.delete()
		template= render_to_string('walletapp/deposit_email.html', {'name': customer_email, 'amount': amount_paid})
		emailmessage= EmailMessage(
			'Congratulations, Your Deposit was successfully made!',
			template,
			settings.EMAIL_HOST_USER,
			[customer_email],
			)
		emailmessage.fail_silently=False
		emailmessage.send()
		return redirect('dashboard')

	if payment_info and crypto_to_topup=='xlm':
		new_customerxlm= float(customerxlm) + float(amount_paid)
		print(new_customerxlm)
		customer_info= Customer.objects.filter(id=customer_pk)
		update_bal= customer_info.update(xlm=new_customerxlm)
		delete_payment_info= last_info.delete()
		template= render_to_string('walletapp/deposit_email.html', {'name': customer_email, 'amount': amount_paid})
		emailmessage= EmailMessage(
			'Congratulations, Your Deposit was successfully made!',
			template,
			settings.EMAIL_HOST_USER,
			[customer_email],
			)
		emailmessage.fail_silently=False
		emailmessage.send()
		return redirect('dashboard')

	if payment_info and crypto_to_topup=='ada':
		new_customerada= float(customerada) + float(amount_paid)
		print(new_customerada)
		customer_info= Customer.objects.filter(id=customer_pk)
		update_bal= customer_info.update(ada=new_customerada)
		delete_payment_info= last_info.delete()
		template= render_to_string('walletapp/deposit_email.html', {'name': customer_email, 'amount': amount_paid})
		emailmessage= EmailMessage(
			'Congratulations, Your Deposit was successfully made!',
			template,
			settings.EMAIL_HOST_USER,
			[customer_email],
			)
		emailmessage.fail_silently=False
		emailmessage.send()
		return redirect('dashboard')

	return HttpResponse('Deposit confirmation was successful')

	return render(request, 'walletapp/update_payment.html' )
