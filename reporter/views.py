from django.shortcuts import render, redirect
from .models import Report
from .forms import ReportForm
import folium

# Create your views here.
def index(request):

    return render(request, 'reporter/index.html')

def map_view(request):
    all_reports = Report.objects.all()

    # create a folium map centered on Karachi
    my_map = folium.Map(location=[24.916452, 67.042635], zoom_start=10)

    # add a marker to the map for each report
    for report in all_reports:
        coordinates = (report.location_lat, report.location_lon)
        folium.Marker(coordinates, popup=report.report_type).add_to(my_map)

    context = {'map': my_map._repr_html_()}
    return render(request, 'reporter/map_view.html', context)

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