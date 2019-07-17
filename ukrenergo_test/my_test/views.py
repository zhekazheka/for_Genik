from django.shortcuts import render
from django.contrib import messages
from .forms import CvsForm
from .models import CvsModel
import csv
import io
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import views


def home_view(request):
    return render(request, 'home.html')

class CsvClassView(views.generic.edit.FormView):
    template_name = 'upload.html'
    form_class = CvsForm
    success_url = 'some.html'

    # @method_decorator(login_required(login_url='/login')) TODO fix me
    def form_valid(self, form):
        form.process_data()
        return super().form_valid(form)
