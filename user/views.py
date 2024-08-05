from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return valid

class SignInView(LoginView):
    form_class = AuthenticationForm
    template_name = 'signin.html'

    def get_success_url(self):
        return reverse_lazy('index')
