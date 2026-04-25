from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, BookPricing
from catalogue.models import Livre

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.decorators.http import require_safe
@require_safe  # N'accepte que GET et HEAD (méthodes sûres)
def product_list(request):
    livres = Livre.objects.all()
    return render(request, 'cart/browsing.html', {'livres': livres})
@require_safe
@login_required(login_url='cart:login')
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user, status=False)
    total_price = sum(item.subtotal for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@require_safe
@login_required(login_url='cart:login')
def add_to_cart(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    # Vérifier que le livre a un pricing
    try:
        pricing = livre.pricing
    except BookPricing.DoesNotExist:
        messages.error(request, "Ce livre n'a pas de prix défini.")
        return redirect('cart:view_cart')
    cart_item, created = CartItem.objects.get_or_create(
    livre=livre,
    user=request.user,
    status=False, # panier non payé
    defaults={'unit_price': pricing.final_price, 'quantity': 1}
    )
    return redirect('cart:view_cart')

@require_safe
@login_required(login_url='cart:login')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart:view_cart')

@require_safe
@login_required(login_url='cart:login')
def add_qty(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    cart_item = get_object_or_404(CartItem, livre=livre, user=request.user,status=False)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:view_cart')

@require_safe
@login_required(login_url='cart:login')
def sub_qty(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    cart_item = get_object_or_404(CartItem, livre=livre, user=request.user,
    status=False)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        messages.warning(request, "La quantité ne peut pas être inférieure à 1.")
    return redirect('cart:view_cart')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # connecte directement après inscription
            return redirect('cart:product_list')
    else:
        form = UserCreationForm()
    return render(request, 'cart/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirige vers la page demandée avant login, ou vers product_list
            return redirect(request.GET.get('next', 'cart:product_list'))
    else:
        form = AuthenticationForm()  # formulaire vide pour GET

    return render(request, 'cart/login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('cart:login')
