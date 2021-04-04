from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,FormView,DeleteView
from django.urls import reverse_lazy,resolve
from django.http import Http404,request

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from .decorators import allow_shares
from django.views.decorators.csrf import csrf_protect
from mailer import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm





class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):

    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks') 

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)    

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)    


class TaskList( LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

class TaskDetail( LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ###context['tasks'] = context['tasks'].filter(user=self.request.user)
        ###context['count'] = context['tasks'].filter(complete=False).count()
        ###return context
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__startswith=search_input)
        context['search_input'] = search_input

        return context

class TaskCreate( LoginRequiredMixin,CreateView):
    model = Task 
    fields =  ['email','title', 'description', 'complete']
    success_url = reverse_lazy('tasks') 

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form )

class TaskUpdate( LoginRequiredMixin,UpdateView):
    model = Task
    fields =  ['email','title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    ###email = send_mail(
        ###'your assigned task status has been changed please do look at it',
        ###'your task status has been edited',
        ###settings.EMAIL_HOST_USER,
        ###[request]
    ###)

    ###email.fail_silently = False
    ###email.send()
 

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))

