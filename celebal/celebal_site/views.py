from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from . models import Task
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from . forms import UserCreationForm
from django.contrib.auth import login


# Create your views here.
class TaskList(LoginRequiredMixin, ListView):     
    model = Task               
    context_object_name = 'tasks'   

    def get_context_data(self, **kwargs):                   #making user-specific data
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)


        return context



class TaskCreate(LoginRequiredMixin, CreateView):#looks for base/task_form.html
    model = Task
    fields = ['title']
    success_url = reverse_lazy('tasks')  

    def form_valid(self, form):                      
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'celebal_site/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

    

class RegisterPage(FormView):
    template_name = 'celebal_site/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):      #redirect_authenticated_user = True wasnt helpfull so our own
        if self.request.user.is_authenticated:
            return redirect(task)
        return super(RegisterPage, self).get(*args, **kwargs)

    