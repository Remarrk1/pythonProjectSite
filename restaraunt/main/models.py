from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User as DefaultUser
class Post(models.Model):
    name_post = models.CharField(max_length=32)

    def __str__(self):
        return self.name_post


class Table(models.Model):
    number_table = models.IntegerField(primary_key=True)
    number_seats = models.IntegerField()

    def __str__(self):
        return f'Столик {self.number_table}'

class Status(models.Model):
    status = models.CharField(max_length=32)

    def __str__(self):
        return self.status


class Dish_type(models.Model):
    name_type = models.CharField(max_length=64)

    def __str__(self):
        return self.name_type

    def get_absolute_url(self):
        return reverse('type',kwargs={'type_id':self.pk})

class Worker(models.Model):
    user = models.OneToOneField(DefaultUser, on_delete=models.CASCADE)
    surname = models.CharField(max_length=32)
    name = models.CharField(max_length=16)
    patronymic = models.CharField(max_length=20)
    login = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.surname

class Dishes_list(models.Model):
    name_dish = models.CharField(max_length=64)
    weight = models.IntegerField()
    calories = models.IntegerField()
    dish_type = models.ForeignKey('Dish_type', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Блюдо: {self.name_dish} | Вид:{self.dish_type.name_type}'


class Order(models.Model):
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE)
    number_table = models.ForeignKey('Table', on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.pk}"

    def save(self, *args, **kwargs):
        if not self.pk:
            # Если это новый заказ, устанавливаем дату и время создания
            self.data = timezone.now()

        super().save(*args, **kwargs)
class Order_content(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    dish = models.ForeignKey('Dishes_list', on_delete=models.CASCADE)
    number_of_servings = models.IntegerField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        self.cost = self.number_of_servings * self.dish.price
        super(Order_content, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.number_of_servings}x {self.dish.name_dish} ({self.cost}₽)"

