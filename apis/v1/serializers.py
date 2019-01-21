from rest_framework import serializers
from  apps.models import Device, Category, Product, OrderLine, Order
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class DeviceSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, required=True)
    shop_name = serializers.CharField(max_length=255, required=True)
    sr_no = serializers.CharField(max_length=20, required=False)
    address = serializers.CharField(required=False)
    pin = serializers.CharField(max_length=4, required=True)

    def create(self, validated_data):
        username = validated_data.get('username', None)
        address = validated_data.get('address', None)
        sr_no = validated_data.get('sr_no', None)
        shop_name = validated_data.get('shop_name', None)
        pin = validated_data.get('pin', None)

        user, created = User.objects.get_or_create(username=username)
        device, device_created = Device.objects.get_or_create(user=user)
        device.pin = make_password(pin)
        device.shop_name = shop_name
        device.sr_no = sr_no
        device.address = address
        device.save()
        return device


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    pin = serializers.CharField(max_length=4)


class ChangePassSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    pin = serializers.CharField(max_length=4)
    new_pin = serializers.CharField(max_length=4)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'image', 'regular_price', 'price', 'unite')


class CreateOrderSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)


class OrderlineSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # product = serializers.IntegerField(source=)
    class Meta:
        model = OrderLine
        fields = ('id', 'product', 'quantity', 'unite_price', 'amount')


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    orderline_set = OrderlineSerializer(read_only=True, many=True)
    class Meta:
        model = Order
        fields = ('id', 'device', 'status', 'order_total', 'orderline_set')
