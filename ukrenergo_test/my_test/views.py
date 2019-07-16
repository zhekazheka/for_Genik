from django.shortcuts import render
from django.contrib import messages
from .forms import CvsForm
from .models import CvsModel
import csv
import io
from django.contrib.auth.decorators import login_required


def home_view(request):
    return render(request, 'home.html')


@login_required(login_url='/login')
def upload_view(request):
    form_class = CvsForm()

    def form_valid(self, form):
        form.process_data()
        return super().form_valid(form)
    return render(request, 'upload.html')

# @login_required(login_url='/login')
# def upload_view(request):
#     template = "upload.html"
#     prompt = {
#         'order': 'Order of the CSV should be variable, alpha_a, alpha_b'
#     }
#     if request.method == 'GET':
#         return render(request, template, prompt)

#     csv_file = request.FILES['file']

#     if not csv_file.name.endswith('.csv'):
#         messages.error(request, 'This is not a csv file')

#     data_set = csv_file.read().decode('UTF-8')
#     io_string = io.StringIO(data_set)

#     # next(io_string)
#     for column in csv.reader(io_string, delimiter=','):
#         print(column[1:])
#         print(type(column))
#         CvsModel.objects.update_or_create(
#             variable=column[0],
#             alpha_a=column[1],
#             alpha_b=column[2]
#         )
#         for i in column:
#             print(i)
#     context = {}
#     return render(request, template, context)
