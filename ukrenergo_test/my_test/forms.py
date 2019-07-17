from django import forms

from .models import CvsModel
import csv
import io
import re
import uuid


class CvsForm(forms.Form):
    data_file = forms.FileField()

    def clean_data_file(self):
        f = self.cleaned_data['data_file']

        if f:
            ext = f.name.split('.')[-1]
            if ext != 'csv':
                raise forms.ValidationError('File type not supported')
        return f

    def process_data(self):
        f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
        reader = csv.DictReader(f)

        # removes all rows from the table
        CvsModel.objects.all().delete()

        # populate the database with parsed data
        for row in reader:
            for key in row.keys():
                if key == 'Variable':
                    continue

                CvsModel.objects.create(
                    variable=row['Variable'],
                    value=row[key]
                )

        # this part has to be moved to result page (some.html) at the moment, which does not exist
        # regexp to check that the value contains only valid latin charactes
        english_check = re.compile(
            r'[A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]')

        # take all the distinct variables (Alpha A/Alpha B in our case)
        distinct_vars = CvsModel.objects.order_by().values('variable').distinct()
        print(distinct_vars)
        for kv in distinct_vars:
            # here we will need to create a new table for each unique variable
            print('Table for ' + kv['variable'])
            for val in CvsModel.objects.filter(variable=kv['variable']).values():
                # population of the First table
                if kv['variable'] == 'Alpha A':
                    if val['value'] == '0':
                        val['value'] = '9'
                    print(val)

                # population of the Second table
                elif kv['variable'] == 'Alpha B' and english_check.match(val['value']):
                    print(val)

        # then we just hard code population of third one with random GUIDs
        for i in range(16):
            print(uuid.uuid4())

        # example of accessing all the objects inside the DB
        # for e in CvsModel.objects.all():
        #     print(e.variable)
        #     print(e.value)
