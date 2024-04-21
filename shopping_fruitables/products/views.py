from django.shortcuts import render
from django.views import View
from .models import Product, Category, Comment, Cart
from customers.models import Customers
from django.contrib.auth.models import User
# Create your views here.


class ProductListView(View):
    def get(self, request):
        search = request.GET.get('search')
        print(search)
        if not search:
            products = Product.objects.all()
            categories = Category.objects.all()
            featured_products = Product.objects.all()
            context = {'products': products,
                       "categories": categories,
                       "featured_products": featured_products,
                       }
            return render(request, 'vegetable_web/shop.html', context)
        else:
            products = Product.objects.filter(title__icontains=search)
            featured_products = Product.objects.all()
            categories = Category.objects.all()
            context = {'products': products,
                       "categories": categories,
                       "featured_products": featured_products,
                       }
            return render(request, 'vegetable_web/shop.html', context)


class ProductDetailView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        featured_products = Product.objects.all()
        categories = Category.objects.all()
        customers = Customers.objects.all()
        comments = Comment.objects.all()
        user_id = request.user.id
        " userning malumotlari faqat comment yozish uchun test qilishga olingan "
        user = User.objects.get(id=user_id)
        print(user)
        context = {
            'product': product,
            "categories": categories,
            'featured_products': featured_products,
            'customers': customers,
            'comments': comments,
            'user': user,
        }
        return render(request, 'vegetable_web/shop-detail.html', context)

    def post(self, request, id):
        """ bu methodni customer emas user yozsa qabul qiladigan qilmoqchi edim lekin ozor kamchiliklar bor shuning uchun bu ishlamaydi """
        user = request.user
        text = request.POST.get('comment')
        comment = Comment.objects.create(text=text, user=user)
        product = Product.objects.get(id=id)
        product.comments.add(comment)
        product.save()
        product = Product.objects.get(id=id)
        featured_products = Product.objects.all()
        categories = Category.objects.all()
        customers = Customers.objects.all()
        comments = Comment.objects.all()
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        context = {
            'product': product,
            "categories": categories,
            'featured_products': featured_products,
            'customers': customers,
            'comments': comments,
            'user': user,
            }
        return render(request, 'vegetable_web/shop-detail.html', context)


class CartView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        Cart.objects.create(product=product)
        # Mahsulotlar uchun umumiy narxni va yetkazib berish narxini hisoblash
        total_price = 0
        shipping_price = 0
        for cart_product in Cart.objects.all():
            total_price += cart_product.product.price
            shipping_price = cart_product.shipping_price
        cart = Cart.objects.all()
        context = {
            'product': product,
            'cart': cart,
            'total_price_ship': total_price + shipping_price,
            'total_price': total_price,
            'shipping_price': shipping_price,
        }
        return render(request, 'vegetable_web/cart.html', context)