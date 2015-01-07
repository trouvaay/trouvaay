from django.shortcuts import render
from django.views import generic
import stripe

stripe.api_key = "sk_test_Ss8OxSVnDLbGv3qJ2HGUNNau"


def StripeView(request):

	if request.method == "POST":
		print('shit posted')
		token = request.POST['stripeToken']
		try:
		  charge = stripe.Charge.create(
		      amount=1000, # amount in cents, again
		      currency="usd",
		      card=token,
		      description="payinguser@example.com",
		      receipt_email="blakesadams@gmail.com",
		      capture=False
		  )
		except stripe.CardError, e:
			#TODO serve card_error text back to user
		  print('card declined')
		  pass

		
	return render(request, 'checkout/checkout.html')
# Create your views here.
