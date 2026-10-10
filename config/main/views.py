from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ContactForm, QuickQuoteForm
from .models import ContactRequest, Project, Service


def home_view(request):
    services = Service.objects.filter(is_active=True).order_by('order', 'title')[:6]
    projects = Project.objects.all()[:3]

    if request.method == 'POST':
        form = QuickQuoteForm(request.POST)
        if form.is_valid():
            ContactRequest.objects.create(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                service=form.cleaned_data['service'],
                message=form.cleaned_data['message'],
            )
            messages.success(request, 'تم إرسال طلبك بنجاح، وسيقوم فريقنا بالتواصل معك قريباً.')
            return redirect('home')
    else:
        form = QuickQuoteForm()

    context = {
        'services': services,
        'projects': projects,
        'form': form,
    }
    return render(request, 'main/home.html', context)


def service_detail_view(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    services = Service.objects.filter(is_active=True).order_by('order', 'title')
    related_services = services.exclude(id=service.id)[:3]
    return render(request, 'main/service_detail.html', {
        'service': service,
        'services': services,
        'related_services': related_services,
    })


@require_http_methods(["GET", "POST"])
def contact_view(request):
    form = ContactForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'تم إرسال رسالتك بنجاح، وسنقوم بالرد عليك في أقرب وقت.')
        return redirect('contact')

    return render(request, 'main/contact.html', {
        'services': Service.objects.filter(is_active=True).order_by('order', 'title'),
        'form': form,
    })
