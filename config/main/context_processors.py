from .models import CompanyInfo, Service


def company_info(request):
    return {
        'company': CompanyInfo.get_instance(),
        'services': Service.objects.filter(is_active=True).order_by('order', 'title'),
    }