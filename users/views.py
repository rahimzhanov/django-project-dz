# users/views.py
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from users.forms import UserRegisterForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')  # БЕЗ namespace

    def form_valid(self, form):
        user = form.save()

        send_mail(
            subject='Добро пожаловать!',
            message='Вы успешно зарегистрировались в нашем магазине!',
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return super().form_valid(form)