from django.test import TestCase
from . import views
from .models import Status
from django.urls import reverse, resolve



'''
Мы должны провести тесты текстовых меток всех полей, поскольку, даже несмотря на то, 
что не все они определены, у нас есть проект, в котором сказано, что все их значения должны быть заданы. 
Если мы не проведём их тестирование, тогда мы не будем знать, что данные метки действительно содержат необходимые значения.
'''
class StatusModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Status.objects.create(status='Оплачен')

    def test_first_name_label(self):
        status=Status.objects.get(id=1)
        field_label = status._meta.get_field('status').verbose_name
        self.assertEquals(field_label,'status')

#Эти тесты проверяют, что все URL-шаблоны правильно сопоставляются с соответствующими представлениями в файле views.py
class UrlsTest(TestCase):
    def test_main_url(self):
        url = reverse('main')
        self.assertEqual(resolve(url).func, views.main)

    def test_index_url(self):
        #Здесь используется функция reverse(), которая принимает имя URL-шаблона 'index' и возвращает соответствующий URL.
        url = reverse('index')
        #views.index представляет собой ссылку на функцию index в модуле views.
        #resolve(url) анализирует переданный URL и возвращает объект ResolverMatch,
        # содержащий информацию о соответствующем представлении (view), функции или классе.
        # .func возвращает функцию или метод, связанный с представлением (view) или классом.
        self.assertEqual(resolve(url).func, views.index)
        #Tест будет успешным, если функция,
        # связанная с URL-шаблоном 'index', совпадает с функцией views.index

    def test_dishes_url(self):
        url = reverse('menu')
        self.assertEqual(resolve(url).func, views.dishes)

    def test_show_type_url(self):
        url = reverse('type', args=[1])  # Пример URL с параметром type_id = 1
        self.assertEqual(resolve(url).func, views.show_type)

    def test_order_delete_url(self):
        url = reverse('order_delete', args=[1])  # Пример URL с параметром pk = 1
        self.assertEqual(resolve(url).func, views.order_delete)

    def test_order_list_url(self):
        url = reverse('order_list')
        self.assertEqual(resolve(url).func, views.order_list)

    def test_add_to_cart_url(self):
        url = reverse('add_to_cart', args=[1])  # Пример URL с параметром dish_id = 1
        self.assertEqual(resolve(url).func, views.add_to_cart)

    def test_save_order_url(self):
        url = reverse('save_order')
        self.assertEqual(resolve(url).func, views.save_order)

    def test_clear_cart_url(self):
        url = reverse('clear_cart')
        self.assertEqual(resolve(url).func, views.clear_cart)

    def test_remove_from_cart_url(self):
        url = reverse('remove_from_cart', args=[1])  # Пример URL с параметром dish_id = 1
        self.assertEqual(resolve(url).func, views.remove_from_cart)

    def test_cart_url(self):
        url = reverse('cart')
        self.assertEqual(resolve(url).func, views.cart)

    def test_generate_report_url(self):
        url = reverse('order_report', args=[1])  # Пример URL с параметром order_id = 1
        self.assertEqual(resolve(url).func, views.generate_report)

    def test_generate_report_all_url(self):
        url = reverse('generate_report_all')
        self.assertEqual(resolve(url).func, views.generate_report_all)