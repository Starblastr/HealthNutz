from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.views import generic
import datetime
from django.conf import settings
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from .models import Image
from django import forms
from .forms import ImageUpload


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


class ItemDetail(generic.DetailView):
    model = Product
    template_name = 'store/item_detail.html'

    def get(self, request, slug):
        data = cartData(request)
        product = self.get_object(queryset=None)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        products = Product.objects.all()
        context = {'products': products, 'cartItems': cartItems, 'product': product}
        return render(request, 'store/item_detail.html', context)


# # homepage
def home(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    if request.method == 'GET':
        return render(request, 'store/home.html', context)
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['username']
        user = authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
    else:
        messages.error(request, "Invalid Credentials")

    return render(request, 'store/home.html', context)

def blog(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    posts = Post.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'post_list':posts}
    return render(request, 'store/blog.html', context)


# registration view if needed
def register(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password1')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
    context = {'products': products, 'cartItems': cartItems, }
    return render(request, 'store/register.html', context)

from .models import Post
from .forms import CommentForm, UserCommentForm
from django.shortcuts import render, get_object_or_404

def post_detail(request, slug):
    template_name = 'store/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    current_post = Post.objects.get(slug=slug)
    posts = Post.objects.all()
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method != 'POST':
        if request.user.is_authenticated:
            comment_form = UserCommentForm()
        else:
            comment_form = CommentForm()
        return render(request, template_name, {'post': post,
                                           'current_post': current_post,
                                           'posts': posts,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
    # Comment posted
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = UserCommentForm(data=request.POST)
        else:
            comment_form = CommentForm(data=request.POST)
        # comment_form.fields['name'] = request.user.customer.name
        # comment_form.fields['email'] = request.user.customer.email

        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            #Assign user to comment
            new_comment.user_id = request.user.customer.pk
            # Assign username as name
            new_comment.name = request.user.customer.name
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
        if request.user.is_authenticated:
            comment_form = UserCommentForm()




    return render(request, template_name, {'post': post,
                                           'current_post': current_post,
                                           'posts': posts,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
# about me page
def about(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/about.html', context)


def policy(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/policy.html', context)


def contact(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/contact.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)





# very interesting view for handling adding and remving items
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def processOrder(request):
    itemData = cartData(request)
    items = itemData['items']
    itemList = []
    for i in items:
        n = i['product']['name']
        q = str(i['quantity'])
        p = str(i['product']['price'])
        item = f"(Product: {n} | Quantity: {q} | Price: {p})"
        itemList.append(item)
    transaction_id = datetime.datetime.now().timestamp()
    date_ordered = datetime.datetime.today().strftime('%Y-%m-%d')
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    order.date_ordered = date_ordered
    order.items = itemList
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
        customer_addrs = ShippingAddress.objects.get(order=order)
    #Lets Send the Customer an order confirmation email
    from_email = settings.EMAIL_HOST_USER
    to_email = [from_email, customer.email]
    send_mail('Your Synsational Baskets Order', f"Thank you for your purchase. Please allow 3-5 business days for"
                                                f"your order to arrive. Your Items: {itemList}                                                                      "
                                                f"Shipping to: {customer_addrs}, {customer_addrs.zipcode}, {customer_addrs.city}, {customer_addrs.state}", from_email,
                                                to_email, fail_silently=False)

    return JsonResponse('Payment submitted..', safe=False)

# Create your views here.
def handler500(request):
    data = {}
    if request.method == 'POST':
        f = request.POST.get('email')
        print(f)
    return render(request, f, 'store/home.html', status=500,)



def image_upload(request):
    images = Image.objects.all()
    if request.method == 'POST':
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('portfolio')
    else:
        form = ImageUpload()
    return render(request, 'store/image_index.html', {'form': form, 'images': images})