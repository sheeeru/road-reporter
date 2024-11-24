from django.shortcuts import render, redirect
from .models import Report
from .forms import ReportForm

# Create your views here.
def index(request):
    return render(request, 'reporter/index.html')

def reports(request):
    """Show all reports."""
    reports = Report.objects.order_by('reported_at')
    context = {'reports': reports}
    return render(request, 'reporter/reports.html', context)

def new_report(request):
    """Add a new report"""
    if request.method != 'POST':
        # No data was submitted, create a blank form
        form = ReportForm()
    else:
        # POST data submitted, process data
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('reporter:reports')

    # Display a blank or invalid form.
    context = {'form':form}
    return render(request, 'reporter/new_report.html', context)