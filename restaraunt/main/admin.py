from django.contrib import admin
from .models import Order, Post, Dish_type, Dishes_list, Status, Order_content, Worker, Table

admin.site.register(Order)
admin.site.register(Dish_type)
admin.site.register(Dishes_list)
admin.site.register(Status)
admin.site.register(Post)
admin.site.register(Order_content)
admin.site.register(Worker)
admin.site.register(Table)