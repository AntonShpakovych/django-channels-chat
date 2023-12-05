from django.urls import reverse_lazy
from django.views import generic

from user.forms import CreateUserForm


class SignUpUserView(generic.CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy("user:login")
    template_name = "user/registration/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["is_signup"] = True

        return context
