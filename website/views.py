from django.shortcuts import render, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.conf import settings
from django.core.mail.message import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template, select_template
from django.contrib import messages

from website.forms import ContactForm


def home(request):
    return TemplateResponse(request, "website/index.html")


def underconstruction(request):
    return TemplateResponse(request, "website/underconstruction.html")


def clinics(request):
    return TemplateResponse(request, "website/clinics.html")


def process_contact_form(request):
    form = ContactForm(request.POST)

    if form.is_valid():
        subject = form.cleaned_data['subject']
        email_address = form.cleaned_data['email_address']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        cc = form.cleaned_data['cc']
        message = form.cleaned_data['message']

        ctx = {
            'host': 'http://{}'.format(request.META.get('HTTP_HOST')),
            'first_name': first_name,
            'last_name': last_name,
            'email_address': email_address,
            'message': message,
        }

        msg = EmailMultiAlternatives(
            'Website Enquiry: {}'.format(subject),
            get_template('website/contact_form_email.txt').render(ctx),
            settings.DEFAULT_FROM_EMAIL,
            to=[settings.DEFAULT_TO_EMAIL],
            cc=[email_address] if cc else [],
            reply_to=[email_address]
        )
        msg.attach_alternative(
            get_template(
                'website/contact_form_email.html'
            ).render(ctx),
            "text/html"
        )
        msg.send(fail_silently=False)

        messages.info(
            request,
            "Thank you for your enquiry! Your email has been sent and "
            "we'll get back to you as soon as possible."
        )

        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['email_address'] = email_address
        # required field, so must be True if form valid
        request.session['data_privacy_accepted'] = True

        return HttpResponseRedirect(reverse('website:contact'))

    else:
        messages.error(
            request, "Please correct the errors below"
        )
        return TemplateResponse(
            request, 'website/contact.html', {'form': form}
        )


def contact(request, template_name='website/contact.html'):

    if request.method == 'POST':
        return process_contact_form(request)

    subject = 'Enquiry'
    first_name = request.session.get('first_name', '')
    last_name = request.session.get('last_name', '')
    email_address = request.session.get('email_address', '')
    data_privacy_accepted = request.session.get('data_privacy_accepted', False)

    form = ContactForm(initial={
        'first_name': first_name, 'last_name': last_name,
        'email_address': email_address, 'subject': subject,
        'data_privacy_accepted': data_privacy_accepted
    })

    return TemplateResponse(
        request, template_name, {'form': form}
    )


def privacy_policy(request):
    return render(request, 'website/privacy_policy.html')
