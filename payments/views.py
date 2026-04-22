from django.http import JsonResponse
from django.conf import settings
from httpx import request
from requests import session
import stripe
from django.shortcuts import render
from cart.models import CartItem
stripe.api_key = settings.STRIPE_SECRET_KEY

from django.contrib.auth.decorators import login_required
def create_checkout_session(request):
    cart_items = get_cart_items(request)
    line_items = []
    for item in cart_items:
        line_items.append({
                'price_data': {
                'currency': 'eur',
                'product_data': {
                'name': item['titre'],
                },
                'unit_amount': int(item['unit_price'] * 100), # en centimes
                },
                'quantity': item['quantity'],
            })
    try:
        session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url="http://localhost:8000/payments/success/",
        cancel_url="http://localhost:8000/payments/cancel/",
        )
        return JsonResponse({"id": session.id})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
def get_cart_items(request):
    cart_items = []
    cart_objects = CartItem.objects.filter(
    user=request.user, # filtrer par user
    status=False # panier non payé
    ).select_related('livre')
    for cart in cart_objects:
        cart_items.append({
        "titre": cart.livre.titre,
        "unit_price": cart.unit_price,
        "quantity": cart.quantity,
        })
    return cart_items
@login_required(login_url='cart:login')
def success(request):
# marquer le panier comme payé
    CartItem.objects.filter(user=request.user,status=False).update(status=True)
    return render(request, "payments/success.html")
def cancel(request):
    return render(request, "payments/cancel.html")