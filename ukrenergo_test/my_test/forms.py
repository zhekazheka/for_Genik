from django import forms

from .models import CvsModel
import csv
import io



class CvsForm(forms.Form):
    data_file = forms.FileField(label='')

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
