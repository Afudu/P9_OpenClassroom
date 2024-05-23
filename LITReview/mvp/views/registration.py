from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from mvp.forms import SignUpForm, CustomAuthenticationForm


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    form_class = SignUpForm
    success_message = "Your account has been created successfully. You can now log in."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'link_name': 'signup_page'})
        return context


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'link_name': 'login_page'})
        return context


class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'
