from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from .forms import OrderForm
from bag.views import _bag_id
from bag.models import Bag


def checkout(request):
    bag = request.session.session_key
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse("products"))

    order_form = OrderForm()
    template = "checkout/checkout.html"
    context = {
        "order_form": order_form,
    }

    return render(request, template, context)