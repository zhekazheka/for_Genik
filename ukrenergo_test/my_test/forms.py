from django import forms

from .models import CvsModel
import csv
import io


class CvsForm(forms.Form):
    data_file = forms.FileField()

    def process_data(self):
        f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
        reader = csv.DictReader(f)
        print(reader)

        for i in reader:
            print(i)

    # def csv_file(self, *args, **kwargs):
    #     file = self.cleaned_data.get('file')
    #     if not file.endswith('.csv'):
    #         raise forms.ValidationError("This is not valid format of file")
    #     return file
