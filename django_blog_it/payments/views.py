# payments/views.py
import stripe # new

from django.conf import settings
from django.views.generic.base import TemplateView
from django.shortcuts import render # new
import os

stripe.api_key = os.getenv('STRIPE_SECRET_KEY') # new

class PaymentPage(TemplateView):
    template_name = 'payments/home.html'
    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['key'] = os.getenv('STRIPE_PUBLISHABLE_KEY')
        return context

def charge(request): # new
    if request.method == 'POST':
        print('i am here')
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='Donate Kaustav Banerjee',
            source=request.POST.get('stripeToken')
        )
        return render(request, 'payments/charge.html')
