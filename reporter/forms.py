from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_type', 'report_description', 'location_lat', 'location_lon', 'is_resolved', 'image']