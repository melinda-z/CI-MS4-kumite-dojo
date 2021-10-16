from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category
from bag.models import BagItem
from bag.views import _bag_id
from django.http import HttpResponse


def all_products(request, category_name=None):
    """A view to show all products, including sorting and search quries"""

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if "sort" in request.GET:
            sortkey = request.GET["sort"]
            sort = sortkey
            if sortkey == "name":
                sortkey = "lower_name"
                products = products.annotate(lower_name=Lower("name"))
            if sortkey == "category":
                sortkey == "category__name"
            if "direction" in request.GET:
                direction = request.GET["direction"]
                if direction == "desc":
                    sortkey = f"-{sortkey}"
                products = products.order_by(sortkey)

        if "category" in request.GET:
            categories = request.GET["category"].split(",")
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if "q" in request.GET:
            query = request.GET["q"]
            if not query:
                messages.error(request, "You didn't enter any search criterial")
                return redirect(reverse("products"))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f"{sort}_{direction}"

    context = {
        "products": products,
        "search_term": query,
        "current_categories": categories,
        "current_sorting": current_sorting,
    }
    return render(request, "products/products.html", context)


def product_detail(request, slug):
    """A view to show individual product details"""

    product = get_object_or_404(Product, slug=slug)
    in_bag = BagItem.objects.filter(
        bag__bag_id=_bag_id(request), product=product
    ).exists()

    context = {
        "product": product,
        "in_bag": in_bag,
    }

    return render(request, "products/product_detail.html", context)


def membership(request):
    """A view to show the membership category products"""
    category = Category.objects.filter(name=membership)

    context = {
        "product": product,
    }
    return render(request, "products/membership.html", context)
