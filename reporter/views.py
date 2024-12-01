from django.shortcuts import render, redirect
from .models import Report
from .forms import ReportForm
import folium
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from .forms import LoginForm
from .forms import ReportForm, LoginForm
import logging
from .forms import RegistrationForm 
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

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
        popup_content = f"Report: {report.report_type}<br>Resolved: {'Yes' if report.is_resolved else 'No'}"
        folium.Marker(coordinates, popup=popup_content).add_to(my_map)

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

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('reporter:reports')  # Redirect to the reports page after login
    else:
        form = LoginForm()
    return render(request, 'reporter/login.html', {'form': form})

logger = logging.getLogger(__name__)

from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            # Generate a success message with the username
            messages.success(request, f'Account created successfully! Your username is: {user.username}')
            return redirect('reporter:login')  # Redirect to login after registration
    else:
        form = RegistrationForm()
    return render(request, 'reporter/register.html', {'form': form})

def logout_view(request):
    # Example logout view (if needed)
    logout(request)
    return redirect('reporter:index')