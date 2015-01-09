from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

# Create your views here.
from models import Cart, CartItem
from goods.models import Product
from django.views.decorators.csrf import csrf_exempt
#Need to add crsf token to frontend

def AddCartProduct(request):
	request.session.set_expiry(120000)
	
	if request.method == "POST":
		try:
			the_id = request.session['cart_id']
			print ('cart exist')
		except:
			new_cart = Cart()
			new_cart.save()
			request.session['cart_id'] = new_cart.id
			the_id = new_cart.id
		
		cart = Cart.objects.get(id=the_id)
		request.session['items_total'] = cart.cartitem_set.count()
		print (request.session['items_total'])
		try:
			product = Product.objects.get(pk=int(request.POST['id'][4:]))
			
		except Product.DoesNotExist:
			pass
		except:
			pass
			
		else:
			pass

		cart_item = CartItem.objects.create(cart=cart, product=product)
		cart_item.save()

		return JsonResponse(product.short_name, safe=False)
	return JsonResponse('success', safe=False)