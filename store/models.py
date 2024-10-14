from django.db import models

# Create your models here.

#promotion n - n product lo que quiere decir que una promocion puede tener varios productos y un producto puede estar en varias promociones
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=5, decimal_places=2)


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+') #relacion uno a muchos
    #el related_name es para que no se cree una relacion inversa, es decir que no se cree una relacion de product a collection

class Product(models.Model):
   # sku = models.CharField(max_length=255, primary_key=True) asi se pone una llave primaria
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='-') #se usa para que el titulo se convierta en una url
    description = models.TextField()
    unti_price = models.DecimalField(max_digits=6, decimal_places=2) # 9999.99 6 en total, 2 decimales
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, related_name='products') #relacion muchos a muchos


    
 

class Customer(models.Model):

    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone  = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    class Meta:
        db_table = 'store_customer' #se puede cambiar el nombre de la tabla
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
        ]

'''
Relacion uno a uno
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    #customer es la llave foranea y primaria para que solo haya una direccion por cliente
    #no se añade nada a customer porque ya se esta haciendo referencia a la tabla customer

'''


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
   

class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'
    PAYMENT_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed')
    ]
    payment_status = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
