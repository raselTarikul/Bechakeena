from django.db import models
from datetime import datetime
import pytz
import decimal
from rest_framework import status, permissions
from rest_framework.response import Response
from apis.v1 import schema
from rest_framework.views import APIView
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from apps.models import Device, Category, Product, Order, OrderLine
from .serializers import DeviceSerializer, LoginSerializer, CategorySerializer, ProductSerializer, \
    CreateOrderSerializer, OrderSerializer, ChangePassSerializer


class RegisterDevice(APIView):
    schema = schema.device_registration_schema

    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Your registration completed.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Field Validation Error'}, status.HTTP_406_NOT_ACCEPTABLE)


class Login(APIView):
    schema = schema.device_login_schema

    def post(self, request):
        try:
            with transaction.atomic():
                serializer = LoginSerializer(data=request.data,
                                                   context={'request': request})
                if serializer.is_valid(raise_exception=True):
                    username = serializer.validated_data['username']
                    pin = serializer.validated_data['pin']
                    try:
                        user  = User.objects.get(username=username)
                        device = Device.objects.get(user=user)
                        if check_password(pin, device.pin):
                            token, created = Token.objects.get_or_create(user=user)
                            return Response({
                                'token': token.key,
                            }, status=200)
                        else:
                            return Response({'message': 'Invalid Pin'}, status.HTTP_406_NOT_ACCEPTABLE)
                    except User.DoesNotExist:
                        return Response({'message': 'User does not exists'}, status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    return Response({'message': 'Field Validation Error'}, status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({'message': 'Can not login with provided credentials.'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ChangePassword(APIView):
    schema = schema.device_change_pass_schema
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            with transaction.atomic():
                serializer = ChangePassSerializer(data=request.data,
                                                   context={'request': request})
                if serializer.is_valid(raise_exception=True):
                    username = serializer.validated_data['username']
                    pin = serializer.validated_data['pin']
                    new_pin = serializer.validated_data['new_pin']
                    try:
                        user  = User.objects.get(username=username)
                        device = Device.objects.get(user=user)
                        if check_password(pin, device.pin):
                            device.pin = make_password(new_pin)
                            
                            device.save()
                            return Response({'message': 'Pin changed successfully'}, status=status.HTTP_200_OK)
                        else:
                            return Response({'message': 'Invalid Pin'}, status.HTTP_406_NOT_ACCEPTABLE)
                    except User.DoesNotExist:
                        return Response({'message': 'User does not exists'}, status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    return Response({'message': 'Field Validation Error'}, status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({'message': 'Invalid credentials.'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class CategoryList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        categorys = Category.objects.all()
        serializers = CategorySerializer(categorys, many=True)
        return Response(serializers.data)


class ProductList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        products = Product.objects.all()
        serializers = ProductSerializer(products, many=True)
        return Response(serializers.data)


class ProductListByCategory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk'] if 'pk' in kwargs.keys() else None
        if pk:
            products = Product.objects.filter(category=pk)
        else:
            products = Product.objects.all()

        serializers = ProductSerializer(products, many=True)
        return Response(serializers.data)


class CreateOrder(APIView):
    schema = schema.create_order_schema
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data, many=True)
        if serializer.is_valid():
            product_list = list()
            order_total = 0
            if len(serializer.data) > 0:
                order = Order()
                order.created_time = datetime.now(pytz.UTC)
                order.device = request.user.device
                order.order_total = 0
                order.save()
                for pro in serializer.data:
                    try:
                        product = Product.objects.get(id=pro['product_id'])
                        product_list.append(product)

                        order_total += product.price * decimal.Decimal(pro['quantity'])

                        order.orderline_set.create(product=product, quantity= decimal.Decimal(pro['quantity']), unite_price=product.price,
                                                   amount=product.price * decimal.Decimal(pro['quantity']), dicount=0)
                    except models.ObjectDoesNotExist:
                        pass
                order.order_total = order_total
                order.save()
                return Response({'message': 'success'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'No Product in List'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'message': 'Invalid Data'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class GetOrderList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        orders = Order.objects.filter(device=request.user.device)
        serializers = OrderSerializer(orders, many=True)
        return Response(serializers.data)

