from django import forms

from .models import CvsModel
import csv
import io


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
        reader = csv.DictReader(f, delimiter=',')
        print(reader.fieldnames)
        
        # for row in reader:
        #     print(row)
        #     print(type(row))
        # for val in row.values():
        #     print(val)
        # CvsModel.objects.update_or_create(

    # def csv_file(self, *args, **kwargs):
    #     file = self.cleaned_data.get('file')
    #     if not file.endswith('.csv'):
    #         raise forms.ValidationError("This is not valid format of file")
    #     return file
