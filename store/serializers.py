from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Customer, Product, Collection,Review,Cart,CartItem,Order,OrderItem
from decimal import Decimal
from django.db import transaction
from .signals import order_created
class CollectionSerializer(serializers.ModelSerializer):
    class Meta():
        model = Collection
        fields = ['id','title','products_count']
    
    products_count = serializers.IntegerField(read_only=True)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ['id','title','unit_price']

class ProductSerializer(serializers.ModelSerializer):
    class Meta():
        model=Product
        # field = '__all__'
        fields = ['id','title','description','slug','inventory','unit_price','price_with_tax','collection']
        
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','date','name','description']
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        product = get_object_or_404(Product, id=product_id)
        return Review.objects.create(product=product, **validated_data)

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
    
    def get_product(self, cart_item: CartItem):
        return {
            'id': cart_item.product.id,
            'title': cart_item.product.title,
            'unit_price': cart_item.product.unit_price
        }
        
    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found.')
        return value
        
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        
        try:
            # Update existing item
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # Create new item
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            
        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'created_at']
        
    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
        
class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']
        
    def create(self, validated_data):
        # Get the current user from the context if available
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user_id = request.user.id
            validated_data['user_id'] = user_id
        
        return super().create(validated_data)
    
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','unit_price'] 
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['id','customer','placed_at','payment_status','items']
        
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
        
class CreateOrderSerializer(serializers.Serializer):
    with transaction.atomic():
        cart_id = serializers.UUIDField()
        
        def validate_cart_id(self, cart_id):
            if not Cart.objects.filter(pk=cart_id).exists():
                raise serializers.ValidationError('No cart with the given ID was found.')
            if CartItem.objects.filter(cart_id=cart_id).count() == 0:
                raise serializers.ValidationError('The cart is empty.')
            return cart_id
        
        def save(self, **kwargs):
            customer = Customer.objects.get(user_id=self.context['user_id'])
            
            cart_items = CartItem.objects \
                            .select_related('product') \
                            .filter(cart_id=self.validated_data['cart_id'])
            
            order = Order.objects.create(customer=customer)
            order_items = [
                    OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                    ) for item in cart_items
                ]
            OrderItem.objects.bulk_create(order_items)
            
            Cart.objects.filter(pk=self.validated_data['cart_id']).delete()
            
            order_created.send_robust(self.__class__, order=order)
            
            return order
            
            