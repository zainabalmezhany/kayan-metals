from django.core.management.base import BaseCommand
from main.models import Service, Project, CompanyInfo
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed initial services, projects and company info for Kayan Metals'

    def handle(self, *args, **options):
        company = CompanyInfo.get_instance()
        company.phone_1 = '+966571500100'
        company.phone_2 = '+96657310020'
        company.whatsapp_1 = '966571500100'
        company.whatsapp_2 = '96657310020'
        company.email = 'info@kayan-metals.com'
        company.company_name = 'كيان المعادن للمقاولات العامة'
        company.address_riyadh = 'الرياض، المملكة العربية السعودية'
        company.google_maps_embed_url = 'https://www.google.com/maps?q=Riyadh%20Saudi%20Arabia&z=12&output=embed'
        company.facebook_url = ''
        company.instagram_url = ''
        company.tiktok_url = ''
        company.whatsapp_url = ''
        company.save()

        services = [
            {
                'title': 'هدم المباني',
                'slug': 'demolition',
                'short_description': 'هدم منظم للمباني والمنشآت مع تخطيط مسبق وإدارة دقيقة للمخاطر والمخلفات.',
                'full_description': (
                    'ننفذ أعمال هدم المباني والمنشآت وفق طبيعة الموقع ونطاق المشروع، بدءًا من معاينة الموقع '
                    'وتحديد طريقة العمل وتسلسل التنفيذ، مع التنسيق المسبق لعزل الخدمات وتأمين مناطق العمل.\n\n'
                    'تعمل الفرق على تفكيك العناصر وإزالة الأنقاض بمعدات مناسبة، مع الحد من الغبار والضوضاء '
                    'قدر الإمكان ومراعاة المباني والمرافق المحيطة. كما نفرز المواد القابلة للاسترداد ونرتب '
                    'نقل المخلفات، ثم نسلّم الموقع مرتبًا وفق نطاق العمل المتفق عليه.'
                ),
                'order': 1,
            },
            {
                'title': 'الحفر وتجهيز المواقع',
                'slug': 'excavation',
                'short_description': 'حفر وتسوية وتجهيز للمواقع والأساسات والخنادق وفق مناسيب ومتطلبات المشروع.',
                'full_description': (
                    'نجهز المواقع لأعمال البناء والبنية التحتية، بما يشمل الحفر للأساسات والخنادق، إزالة '
                    'التربة الزائدة، وتسوية الأرض وفق المناسيب المحددة للمشروع. يبدأ العمل بمراجعة حدود '
                    'الموقع ومتطلبات التنفيذ والتنسيق حول الخدمات القائمة ومسارات المعدات.\n\n'
                    'نختار آليات الحفر والنقل بحسب طبيعة التربة وحجم الأعمال، ونحافظ على تنظيم الموقع '
                    'وممرات الحركة أثناء التنفيذ. بعد انتهاء الأعمال، يمكننا ترتيب نقل نواتج الحفر وتجهيز '
                    'المساحة للمرحلة التالية حسب الاتفاق.'
                ),
                'order': 2,
            },
            {
                'title': 'شراء وبيع وسكراب المعادن',
                'slug': 'scrap-trading',
                'short_description': 'شراء وفرز وتوريد المعادن والخردة مع تنسيق التقييم والوزن والنقل.',
                'full_description': (
                    'نوفر خدمة شراء وبيع الخردة والمعادن للمواقع الصناعية والتجارية، مع فرز المواد بحسب '
                    'نوعها وحالتها لتسهيل تقييمها وتحديد طريقة الاستفادة منها. تشمل المواد التي يمكن '
                    'تقييمها الحديد والمعادن الشائعة الأخرى وفق الكميات والمواصفات المتاحة.\n\n'
                    'ننسق معاينة المواد والوزن وآلية التحميل والنقل، ونوضح العرض قبل إتمام العملية. '
                    'تساعد هذه الخطوات على تنظيم المخزون المعدني بالموقع وتحويل المواد القابلة للاسترداد '
                    'إلى مسار إعادة استخدام أو تدوير مناسب.'
                ),
                'order': 3,
            },
            {
                'title': 'نقل المخلفات وتنظيف الموقع',
                'slug': 'cleanup',
                'short_description': 'جمع مخلفات المشاريع وفرزها ونقلها لترك الموقع مرتبًا وجاهزًا للخطوة التالية.',
                'full_description': (
                    'نتولى جمع مخلفات البناء والتشغيل من الموقع، وفرز المواد القابلة للاسترداد عن بقية '
                    'المخلفات متى أمكن، ثم تنظيم تحميلها ونقلها بحسب نوعها وحجمها. ننسق مسارات النقل '
                    'ومواعيد الرفع بما يقلل تعطيل حركة العمل داخل الموقع.\n\n'
                    'تساعد الخدمة على إبقاء مناطق العمل أكثر ترتيبًا وتجهيز المساحة للأعمال اللاحقة. '
                    'يتم تحديد نطاق التنظيف وعدد مرات الرفع وطريقة التعامل مع المخلفات ضمن عرض العمل '
                    'بحسب احتياج المشروع.'
                ),
                'order': 4,
            },
        ]

        for s in services:
            obj, created = Service.objects.update_or_create(
                slug=s['slug'],
                defaults={
                    'title': s['title'],
                    'short_description': s['short_description'],
                    'full_description': s['full_description'],
                    'order': s['order'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created service: {obj.title}"))

        # example project
        Project.objects.update_or_create(
            title='مشروع تجريبي - تنظيف موقع صناعي',
            defaults={
                'description': 'إكمال نقل المخلفات وتنظيف كامل لموقع صناعي مع تسليم نهائي.',
                'location': 'الرياض - منطقة الصناعية',
                'completion_date': timezone.now().date(),
            }
        )

        self.stdout.write(self.style.SUCCESS('Seeding complete.'))
