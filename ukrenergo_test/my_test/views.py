from django.shortcuts import render
from django.contrib import messages
from .forms import CvsForm
from .models import CvsModel
import csv
import io
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import views
import re
import uuid


@method_decorator(login_required(login_url='/login'), name='dispatch')
class CsvClassView(views.generic.edit.FormView):
    template_name = 'upload.html'
    form_class = CvsForm
    success_url = 'tables'

    def form_valid(self, form):
        form.process_data()
        return super().form_valid(form)


@login_required(login_url='/login', redirect_field_name='/')
def tables_view(request):
    # this part has to be moved to result page (some.html) at the moment, which does not exist
    # regexp to check that the value contains only valid latin charactes
    english_check = re.compile(
        r'[A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]')

    # take all the distinct variables (Alpha A/Alpha B in our case)
    # distinct_vars = CvsModel.objects.values('variable').distinct()
    # print(distinct_vars)
    # alpha_a = []
    # alpha_b = []
    # for kv in distinct_vars:
    #     # here we will need to create a new table for each unique variable
    #     print('Table for ' + kv['variable'])
    #     for val in CvsModel.objects.filter(variable=kv['variable']).values():
    #         # population of the First table
    #         if kv['variable'] == 'Alpha A':
    #             if val['value'] == '0':
    #                 val['value'] = '9'
    #             alpha_a.append(val['value'])
    #             print(val)

    #         # population of the Second table
    #         elif kv['variable'] == 'Alpha B' and english_check.match(val['value']):
    #             alpha_b.append(val['value'])
    #             # print(val)
    # print(alpha_a)
    # print(alpha_b)
    # print(len(distinct_vars[0]))

    alpha_values = CvsModel.objects.filter(variable__exact="Alpha A").values(
    ) | CvsModel.objects.filter(variable__exact="Alpha B").values()

    alphaA_len = CvsModel.objects.filter(variable__exact="Alpha A").count()
    alphaB_len = CvsModel.objects.filter(variable__exact="Alpha B").count()

    print(alphaA_len, alphaB_len)

    alphaA_values = []
    alphaB_values = []

    for i in alpha_values:
        if i['variable'] == 'Alpha A':
            if i['value'] == '0':
                i['value'] = '9'
            alphaA_values.append(i['value'])
        if i['variable'] == 'Alpha B':
            if not english_check.match(i['value']):
                continue
            alphaB_values.append(i['value'])
    print(alphaA_values)
    print(alphaB_values)
    

    # example of accessing all the objects inside the DB
    # for e in CvsModel.objects.all():
    #     print(e.variable)
    #     print(e.value)
    if len(alphaB_values) < alphaB_len:
        for i in range(alphaB_len-len(alphaB_values)):
            alphaB_values.append('')
    
    # then we just hard code population of third one with random GUIDs
    unique = []
    for i in range(16):
        unique.append(uuid.uuid4())

    context = {
        'alphaA_values': alphaA_values,
        'alphaB_values': alphaB_values,
        'range': [range(alphaA_len), range(alphaB_len)],
        'unique': unique,
    }

    return render(request, 'tables.html', context)
