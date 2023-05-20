
from django.db.models import Q
from _decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Post, Dish_type, Dishes_list, Order, Status, Order_content, Table, Worker
from django.shortcuts import redirect

from django.http import HttpResponse


def main(request):
    return render(request, 'users/login.html')

@login_required
def index(request):
    return render(request, 'main/index.html')


@login_required
def dishes(request):
    query = request.GET.get('q')
    if query:
        dishes = Dishes_list.objects.filter(Q(name_dish__icontains=query))
    else:
        dishes = Dishes_list.objects.all()
    context = {
        'types': Dish_type.objects.all(),
        'dishes': dishes,
        'query': query,
    }
    return render(request, 'main/menu.html', context)


@login_required
def show_type(request,type_id):
    #Будем отображать только те блюда, которые соответсвуют виду, совпадают с тем ключом, который передали в виде запроса
    dishes=Dishes_list.objects.filter(dish_type_id=type_id)
    types=Dish_type.objects.all()
    context={
        'dishes':dishes,
        'types':types,
    }
    return render(request,'main/menu.html',context=context)

@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('order_list')


@login_required
def remove_from_cart(request, dish_id):
    print("dish_id:", dish_id)  # отладочная информация
    cart = request.session.get('cart', {})
    if str(dish_id) in cart:
        del cart[str(dish_id)]
        if not cart:
            del request.session['cart']
        else:
            request.session['cart'] = cart
    return redirect('cart')

@login_required
def order_list(request):
    orders = Order.objects.prefetch_related('order_content_set__dish').all().order_by('status_id','-id')
    statuss = Status.objects.all()
    if request.method == 'POST':
        for order in orders:
            status = request.POST.get(str(order.id))
            if status:
                order.status_id = int(status)
                order.save()
    context = {
        'statuss': statuss,
        'orders': orders,
    }
    return render(request, 'main/order_list.html', context)
@login_required
#добавление в заказ
def add_to_cart(request, dish_id):
    # Получаем блюдо по id
    dish = Dishes_list.objects.get(pk=dish_id)
    # Получаем текущую корзину пользователя из сессии
    cart = request.session.get('cart', {})
    # Получаем информацию о добавляемом блюде в корзину
    cart_item = cart.get(str(dish_id), {'quantity': 0, 'price': str(dish.price)})
    # Увеличиваем количество добавляемых блюд на 1
    cart_item['quantity'] += 1

    # Обновляем информацию о добавляемом блюде в корзину
    cart[str(dish_id)] = cart_item
    # Обновляем корзину пользователя в сессии
    request.session['cart'] = cart
    # Перенаправляем пользователя на страницу с меню
    return redirect('cart')
@login_required
def save_order(request):
    cart = request.session.get('cart', {})
    table_number = request.POST['table_number']
    user = request.user
    # Получаем объекты из базы данных
    worker = Worker.objects.get(user=user)
    table = Table.objects.get(number_table=table_number)
    status = Status.objects.get(id=1)
    order = Order(worker=worker, number_table=table, status=status, cost=0)
    order.save()
    for dish_id, item in cart.items():
        dish = Dishes_list.objects.get(pk=dish_id)
        cost = Decimal(item['price']) * item['quantity']
        order_content = Order_content(order=order, dish=dish, number_of_servings=item['quantity'], cost=cost)
        order_content.save()
        order.cost += cost
    order.save()
    request.session['cart'] = {}
    return redirect('order_list')

@login_required
def cart(request):
    cart = request.session.get('cart', {})  # Получаем корзину из сессии
    cart_items = []  # Создаем пустой список для хранения элементов корзины
    total_price = 0  # Изначально общая цена равна 0
    # Для каждого элемента корзины получаем информацию о блюде и его количестве
    table_number = request.POST.get('table_number')  # Получаем номер стола из POST-запроса
    for dish_id, item in cart.items():
        dish = Dishes_list.objects.get(pk=dish_id)
        # Получаем количество порций из POST-запроса или из элемента корзины
        item_quantity = int(request.POST.get('quantity_{}'.format(dish_id), item['quantity']))
        item_price = float(item['price']) * item_quantity  # Вычисляем цену элемента корзины
        total_price += item_price  # Увеличиваем общую цену на стоимость текущего элемента
        cart_items.append({
            'dish': dish,
            'quantity': item_quantity,
            'item_price': item_price
        })
        cart[dish_id]['quantity'] = item_quantity
    # Обновляем номер стола в сессии
    # Обновляем корзину в сессии
    request.session['cart'] = cart
    request.session['table_number'] = table_number
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'table_number': table_number
    }

    return render(request, 'main/cart.html', context)

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('cart')


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def generate_report(response, order_id):
    # Получаем данные из базы данных
    order = Order.objects.get(id=order_id)
    # Создаем PDF-документ
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="example.pdf"'
    pdfmetrics.registerFont(TTFont('Roboto', 'D:\Django\Roboto-Thin.ttf'))
    # Создаем canvas объект и настраиваем его
    p = canvas.Canvas(response, pagesize=letter)
    p.setTitle("Пример PDF-документа")

    # Устанавливаем шрифт и кодировку
    p.setFont("Roboto", 14)
    # Добавляем заголовок отчета
    p.drawString(100, 750, "Отчет по заказам")

    # Добавляем информацию о заказах
    y = 700
    if y < 100:
        p.showPage()
        y = 700
        p.setFont("Roboto", 14)
        p.drawString(100, 750, "Отчет по заказам")
    p.drawString(100, y, f"Заказ №{order.id}  Стол №{order.number_table_id} ")
    y-= 30
    p.drawString(100, y, f" Дата: {order.data.strftime('%d.%m.%Y')} Время: {order.data.strftime('%H:%M')}")
    y -= 30
    p.drawString(100, y, f" Официант: {order.worker.name}")
    y -= 30
    p.drawString(120, y, f"Блюдо")
    p.drawString(370, y, f"Количество")
    p.setDash([3, 2])
    p.line(100, y-5, 450, y-5)
    y -= 40
    order_contents = Order_content.objects.filter(order=order)
    for order_content in order_contents:
        p.drawString(120, y, f"- {order_content.dish.name_dish} ")
        p.drawString(370, y, f" x{order_content.number_of_servings}")
        y -= 40
    p.line(100, y+15, 450, y+15)
    p.drawString(350, y-3, "Итого:")
    p.drawString(400, y-3, f"{order.cost}")
    p.setDash([3, 2])
    p.line(100, y-10, 450, y-10)
    y -= 30
    # Сохраняем PDF-документ и возвращаем его
    p.showPage()
    p.save()
    return response


def generate_report_all(response):
    # Получаем данные из базы данных
    orders = Order.objects.all()
    # Создаем PDF-документ
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="example.pdf"'
    pdfmetrics.registerFont(TTFont('Roboto', 'D:\Django\Roboto-Thin.ttf'))
    # Создаем canvas объект и настраиваем его
    p = canvas.Canvas(response, pagesize=letter)
    p.setTitle("Пример PDF-документа")

    # Устанавливаем шрифт и кодировку
    p.setFont("Roboto", 14)
    # Добавляем заголовок отчета
    p.drawString(100, 750, "Отчет по заказам")

    # Добавляем информацию о заказах
    y = 700
    for order in orders:
        if y < 100:
            p.showPage()
            y = 700
            p.setFont("Roboto", 14)
            p.drawString(100, 750, "Отчет по заказам")
        y -= 10
        p.drawString(100, y, f"Заказ №{order.id}  Стол №{order.number_table_id} ")
        y -= 30
        p.drawString(100, y, f" Дата: {order.data.strftime('%d.%m.%Y')} Время: {order.data.strftime('%H:%M')}")
        y -= 30
        p.drawString(100, y, f" Официант: {order.worker.name}")
        y -= 30
        p.drawString(120, y, f"Блюдо")
        p.drawString(370, y, f"Количество")
        p.setDash([3, 2])
        p.line(100, y - 5, 450, y - 5)
        y -= 40
        order_contents = Order_content.objects.filter(order=order)
        if y < 100:
            p.showPage()
            p.setDash([3, 2])
            y = 700
            p.setFont("Roboto", 14)
        for order_content in order_contents:
            p.drawString(120, y, f"- {order_content.dish.name_dish} ")
            p.drawString(370, y, f" x{order_content.number_of_servings}")
            y -= 25
        p.line(100, y + 15, 450, y + 15)
        p.drawString(320, y - 3, "Итого:")
        p.drawString(400, y - 3, f"{order.cost}")
        y -= 50
        p.setDash()
        p.line(80, y+10, 500, y+10)
        y-=30
    # Сохраняем PDF-документ и возвращаем его
    p.showPage()
    p.save()
    return response
