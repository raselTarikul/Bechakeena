from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.generic import ListView, DetailView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render_to_response, render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

from .models import Category, Product, Order, Device


class DeviceList(LoginRequiredMixin, ListView):
	model = Device


class CategoryList(LoginRequiredMixin, ListView):
	model = Category


class CategoryCreate(LoginRequiredMixin, CreateView):
	model = Category
	fields = ['parent', 'name']
	success_url = reverse_lazy('category_list_view')


class CategoryUpdate(LoginRequiredMixin, UpdateView):
	model = Category
	fields = ['parent', 'name']
	success_url = reverse_lazy('category_list_view')


class CategoryDelet(LoginRequiredMixin, DeleteView):
	model = Category
	success_url = reverse_lazy('category_list_view')


class ProductList(LoginRequiredMixin, ListView):
	model = Product


class ProductCreate(LoginRequiredMixin, CreateView):
	model = Product
	fields = ['category', 'name', 'image', 'regular_price', 'price', 'unite']
	success_url = reverse_lazy('product_list')


class ProductUpdate(LoginRequiredMixin, UpdateView):
	model = Product
	fields = ['category', 'name', 'image', 'regular_price', 'price', 'unite']
	success_url = reverse_lazy('product_list')


class ProductDelet(LoginRequiredMixin, DeleteView):
	model = Product
	success_url = reverse_lazy('product_list')


class OrderList(LoginRequiredMixin, ListView):
	model = Order


class OrderDetails(LoginRequiredMixin, DetailView):
	model = Order


class OrderComplete(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		pk = kwargs['pk'] if 'pk' in kwargs.keys() else None
		if pk:
			try:
				order = Order.objects.get(id=pk)
				order.status = 'COMPLETED'
				order.save()
			except Exception as e:
				pass
		return redirect('/apps/orders/'+str(pk))


class OrderCancel(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		pk = kwargs['pk'] if 'pk' in kwargs.keys() else None
		if pk:
			try:
				order = Order.objects.get(id=pk)
				order.status = 'CANCELLED'
				order.save()
			except Exception as e:
				pass
		return redirect('/apps/orders/' + str(pk))


class RestPin(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		pk = kwargs['pk'] if 'pk' in kwargs.keys() else None
		if pk:
			try:
				device = Device.objects.get(id=pk)
				device.pin = make_password('1234')
				device.save()
			except Exception as e:
				pass
		return redirect('/apps/devices/')


class LogOut(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		return redirect('/apps/login')


class LogIn(View):
	template_name = 'apps/login.html'

	def get(self, request):
		return render(request, self.template_name)

	def post(self, request):
		arg = {}
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user:
				if user.is_active and user.is_superuser:
					login(request, user)
					return redirect('/apps/products/')
			else:
				messages.error(request, 'Wrong Password')
				return redirect('/apps/login/')


class ChangePassword(LoginRequiredMixin, View):
	template_name = 'apps/change_password.html'

	def get(self, request):
		return render(request, self.template_name)

	def post(self, request):
		arg = {}
		if request.method == 'POST':
			password = request.POST['password']
			new_password = request.POST['new_password']
			user = authenticate(username=request.user.username, password=password)
			if user:
				user.set_password(new_password)
				user.save()
				messages.success(request, 'Password change successfully')
			else:
				messages.error(request, 'Incorrect Password')
				return redirect('/apps/change_password/')
			return redirect('/apps/products/')
