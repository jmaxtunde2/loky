from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from django.views.generic import TemplateView
class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = "about_loki.html"

class DonatePageView(TemplateView):
    template_name = "donate.html"

def advertise(request):
    if request.method == 'POST':
        company_name = request.POST['company_name']
        contact_name = request.POST['contact_name']
        contact_email = request.POST['contact_email']
        phone = request.POST['phone']
        website = request.POST['website']
        message = request.POST['message']

        # Here you can handle the form data, e.g., save it to the database or send an email
        # For this example, we'll send an email to the site admin
        send_mail(
            'New Advertising Application from ' + company_name,
            f"Company Name: {company_name}\nContact Name: {contact_name}\nContact Email: {contact_email}\nPhone: {phone}\nWebsite: {website}\nMessage: {message}",
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMINS[0][1]],
        )

        messages.success(request, 'Your application has been submitted successfully!')
        return redirect('advertise')

    return render(request, 'advertise.html')
