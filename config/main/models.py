from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Service(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان الخدمة')
    slug = models.SlugField(max_length=170, unique=True, blank=True, verbose_name='الرابط')
    icon_class = models.CharField(
        max_length=80,
        blank=True,
        default='',
        help_text='مثال: fas fa-hard-hat',
        verbose_name='أيقونة Font Awesome',
    )
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name='صورة الخدمة')
    short_description = models.CharField(max_length=255, verbose_name='وصف مختصر')
    full_description = models.TextField(verbose_name='الوصف التفصيلي')
    order = models.PositiveIntegerField(default=0, verbose_name='الترتيب')
    is_active = models.BooleanField(default=True, verbose_name='نشط')

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'الخدمة'
        verbose_name_plural = 'الخدمات'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True) or 'service'
            self.slug = base_slug
            suffix = 2
            while Service.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f'{base_slug}-{suffix}'
                suffix += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})

    @property
    def photo_url(self):
        if self.image:
            return self.image.url

        photos = {
            'demolition': '/static/images/services/demolition.svg',
            'excavation': '/static/images/services/excavation.svg',
            'scrap-trading': '/static/images/services/scrap.svg',
            'cleanup': '/static/images/services/cleanup.svg',
        }
        return photos.get(self.slug, photos['demolition'])

class Project(models.Model):
    title = models.CharField(max_length=180, verbose_name='عنوان المشروع')
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name='صورة المشروع')
    location = models.CharField(max_length=200, blank=True, verbose_name='الموقع')
    description = models.TextField(verbose_name='وصف المشروع')
    completion_date = models.DateField(verbose_name='تاريخ الإنجاز')
    order = models.PositiveIntegerField(default=0, verbose_name='الترتيب')

    class Meta:
        ordering = ['order', '-completion_date']
        verbose_name = 'المشروع'
        verbose_name_plural = 'المشاريع'

    def __str__(self):
        return self.title


class CompanyInfo(models.Model):
    company_name = models.CharField(
        max_length=180,
        default='كيان المعادن للمقاولات العامة',
        verbose_name='اسم الشركة',
    )
    phone_1 = models.CharField(max_length=30, default='+966571500100', verbose_name='هاتف 1')
    phone_2 = models.CharField(max_length=30, default='+96657310020', verbose_name='هاتف 2')
    whatsapp_1 = models.CharField(max_length=30, default='966571500100', verbose_name='واتساب 1')
    whatsapp_2 = models.CharField(max_length=30, default='96657310020', verbose_name='واتساب 2')
    email = models.EmailField(default='info@kayan-metals.com', verbose_name='البريد الإلكتروني')
    address_riyadh = models.CharField(
        max_length=255,
        default='الرياض، المملكة العربية السعودية',
        verbose_name='العنوان في الرياض',
    )
    google_maps_embed_url = models.TextField(
        default='https://www.google.com/maps?q=Riyadh%20Saudi%20Arabia&z=12&output=embed',
        verbose_name='رابط خريطة Google Maps',
    )
    facebook_url = models.URLField(blank=True, null=True, verbose_name='رابط Facebook')
    tiktok_url = models.URLField(blank=True, null=True, verbose_name='رابط TikTok')
    instagram_url = models.URLField(blank=True, null=True, verbose_name='رابط Instagram')
    whatsapp_url = models.URLField(blank=True, null=True, verbose_name='رابط WhatsApp')
    working_hours = models.CharField(max_length=120, default='السبت - الخميس: 9:00 صباحاً - 7:00 مساءً', verbose_name='مواعيد العمل')

    class Meta:
        verbose_name = 'بيانات الشركة'
        verbose_name_plural = 'بيانات الشركة'

    @classmethod
    def get_instance(cls):
        instance = cls.objects.order_by('pk').first()
        if instance:
            return instance
        return cls.objects.create()

    @property
    def whatsapp_link(self):
        return self.whatsapp_url or f'https://wa.me/{self.whatsapp_1}'

    def __str__(self):
        return 'بيانات الشركة'


class ContactRequest(models.Model):
    name = models.CharField(max_length=120, verbose_name='الاسم')
    phone = models.CharField(max_length=30, verbose_name='رقم الهاتف')
    email = models.EmailField(blank=True, null=True, verbose_name='البريد الإلكتروني')
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contact_requests',
        verbose_name='الخدمة المطلوبة',
    )
    message = models.TextField(verbose_name='الرسالة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    is_processed = models.BooleanField(default=False, verbose_name='تمت المعالجة')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'طلب الاتصال'
        verbose_name_plural = 'طلبات الاتصال'

    def __str__(self):
        return f'{self.name} - {self.phone}'
