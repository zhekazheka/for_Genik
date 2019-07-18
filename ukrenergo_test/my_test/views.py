from django.shortcuts import render
from .forms import CvsForm
from .models import CvsModel
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django import views
import re
import uuid

# decorators that check if a user is loged in and has username uaenergy
decorators = [login_required(
    login_url='/login'), user_passes_test(lambda user: user.username == 'uaenergy', login_url='/specific_user')]


@method_decorator(decorators, name='dispatch')
class CsvClassView(views.generic.edit.FormView):
    '''
    This is a home view for uploading .CSV file and on success redirecting to /tables URL
    '''
    template_name = 'upload.html'
    form_class = CvsForm
    success_url = 'tables'

    def form_valid(self, form):
        form.process_data()
        return super().form_valid(form)


@login_required(login_url='/login', redirect_field_name='/')
@user_passes_test(lambda user: user.username == 'uaenergy', login_url='/specific_user')
def tables_view(request):
    '''
    This view is for querying our database for Alpha A and Alpha B values, changing Alpha A 
    values 9 to 0, deleting not latin letters from Alpha B values and generating unique symbols
    '''
    # regexp to check that the value contains only valid latin charactes
    english_check = re.compile(
        r'[A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]')

    # the main query for getting Alpha A and Alpha B values
    alpha_values = CvsModel.objects.filter(variable__exact="Alpha A").values(
    ) | CvsModel.objects.filter(variable__exact="Alpha B").values()

    # queries to know Alpha A and Alpha B length
    alphaA_len = CvsModel.objects.filter(variable__exact="Alpha A").count()
    alphaB_len = CvsModel.objects.filter(variable__exact="Alpha B").count()

    alphaA_values = []
    alphaB_values = []

    # loop on Alpha A and Alpha B to change Alpha A 0 to 9, delete non-latin letters from Alpha B values
    # and add random unique values to the lists
    for i in alpha_values:
        if i['variable'] == 'Alpha A':
            if i['value']:
                if i['value'] == '0':
                    i['value'] = '9'
                alphaA_values.append(i['value'])
            else:
                alphaA_values.append('')
        if i['variable'] == 'Alpha B':
            if i['value']:
                if not english_check.match(i['value']):
                    continue
                alphaB_values.append(i['value'])
            else:
                alphaB_values.append('')

    # check if Alpha B list with non-latin letters is smaller than all read Alpha B values
    # add empty strings to the end of the list to have a right number of cells in Alpha B table
    if len(alphaB_values) < alphaB_len:
        for i in range(alphaB_len-len(alphaB_values)):
            alphaB_values.append('')

    # hard code population of the third table with random GUIDs
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


def specific_user_view(request):
    '''
    The simplest view for all users, whom username is not uaenergy 
    '''
    return render(request, 'specific_user.html')
