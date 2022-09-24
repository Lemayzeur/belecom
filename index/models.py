from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

class Product(models.Model):
	class Meta:
		db_table = 'products'

	name = models.CharField(max_length=200)
	description = models.TextField(max_length=1000)
	category = models.ForeignKey('Category', on_delete=models.RESTRICT) 
	old_price = models.FloatField(null=True, blank=True)
	price = models.FloatField()
	photo = models.ImageField(upload_to='product_photos/')
	brand = models.CharField(max_length=50, blank=True, null=True)

	is_active = models.BooleanField(default=False)

	def __str__(self):
		return self.name 

class Category(models.Model):
	class Meta:
		db_table = 'categories'
		verbose_name_plural = 'Categories'

	name = models.CharField(max_length=100) 
	photo = models.ImageField(upload_to='category_photos/', blank=True, null=True)

	def __str__(self):
		return self.name 

class Stock(models.Model):
	class Meta:
		db_table = 'stocks'


	product = models.ForeignKey("Product", on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

class Order(models.Model):
	class Meta:
		db_table = 'orders'

	user = models.ForeignKey(User, on_delete=models.RESTRICT)
	sub_total = models.FloatField(default=0)
	discount = models.FloatField(default=0)
	tax = models.FloatField(default=0)
	total = models.FloatField(default=0)

	def __str__(self):
		return "BEC00" + str(self.id)

class OrderProduct(models.Model):
	class Meta:
		db_table = 'order_products'

	order = models.ForeignKey("Order", on_delete=models.CASCADE)
	product = models.ForeignKey("Product", on_delete=models.CASCADE)

	price = models.FloatField()
	quantity = models.FloatField(default=1)

class Cart(models.Model):
	class Meta:
		db_table = 'carts'

	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
	total = models.FloatField(default=0)

	def total_item(self):
		return self.cartproduct_set.count()

	def total_item_2(self):
		items = self.cartproduct_set.all()
		if items:
			return items.aggregate(t=models.Sum('quantity'))['t']
		return 0


	def grand_total(self):
		return self.cartproduct_set.annotate(
				pri_total = models.F("price") * models.F("quantity")
			).aggregate(gt = models.Sum('pri_total'))['gt']

	def __str__(self):
		return "CC0" + str(self.id)

class CartProduct(models.Model):
	class Meta:
		db_table = 'cart_products'

	cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
	product = models.ForeignKey("Product", on_delete=models.CASCADE)

	price = models.FloatField()
	quantity = models.IntegerField(default=1)

	def total(self):
		return self.price * self.quantity

class Payment(models.Model):
	class Meta:
		db_table = 'payments'

	user = models.ForeignKey(User, on_delete=models.RESTRICT)
	order = models.ForeignKey("Order", on_delete=models.RESTRICT)
	total_to_pay = models.FloatField()
	cash = models.FloatField()
	discount = models.FloatField(default=0)
	tax = models.FloatField(null=True, blank=True)
	cash_return = models.FloatField()
	payment_type = models.ForeignKey("PaymentType", blank=True, null=True, on_delete=models.SET_NULL)

class PaymentType(models.Model):
	class Meta:
		db_table = 'payment_types'

	PAYPAL, CARD, MONCASH = 'paypal', 'card', 'moncash'

	PAYMENT_TYPE_LIST =[
		(PAYPAL, 'Paypal'),
		(CARD, 'Card'),
		(MONCASH, 'MonCash'),
	]
	category = models.CharField(max_length=30, choices=PAYMENT_TYPE_LIST, default=MONCASH)
