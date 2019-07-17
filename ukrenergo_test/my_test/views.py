from django.shortcuts import render
from django.contrib import messages
from .forms import CvsForm
from .models import CvsModel
import csv
import io
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import views


@method_decorator(login_required(login_url='/login'), name='dispatch')
class CsvClassView(views.generic.edit.FormView):
    template_name = 'upload.html'
    form_class = CvsForm
    success_url = 'some.html'

    def form_valid(self, form):
        form.process_data()
        return super().form_valid(form)
