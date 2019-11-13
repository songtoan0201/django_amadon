from django.shortcuts import render, redirect
from .models import Order, Product


def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)


def checkout(request):
    if request.method == "POST":
        quantity_from_form = int(request.POST["quantity"])
        id_from_form = int(request.POST["product_id"])
        product = Product.objects.get(id=id_from_form)
        total_charge = quantity_from_form * product.price
        print("Charging credit card...")
        Order.objects.create(
            quantity_ordered=quantity_from_form, total_price=total_charge)

        return redirect("/checkout")
    else:
        last_order = Order.objects.last()
        all_order = Order.objects.all()
        total_charge = 0
        quantity = 0
        for order in all_order:
            total_charge += order.total_price
            quantity += order.quantity_ordered
        context = {
            "total_charge": total_charge,
            "product_price": last_order.total_price/last_order.quantity_ordered,
            "quantity": quantity,
        }
        return render(request, "store/checkout.html", context)
