from django.test import TestCase
from django.contrib import admin
from django.test import RequestFactory, override_settings
from django.urls import reverse

from .admin import CompanyInfoAdmin
from .models import CompanyInfo, ContactRequest, Service


@override_settings(SECURE_SSL_REDIRECT=False)
class PublicSiteTests(TestCase):
	def test_home_creates_company_settings_when_missing(self):
		response = self.client.get(reverse('home'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'كيان المعادن للمقاولات العامة')
		self.assertTrue(CompanyInfo.objects.exists())

	def test_about_page_is_not_routed(self):
		response = self.client.get('/about/')

		self.assertEqual(response.status_code, 404)

	def test_homepage_quote_can_be_submitted_without_service(self):
		response = self.client.post(reverse('home'), {
			'name': 'Test Customer',
			'phone': '+966500000000',
			'email': '',
			'service': '',
			'message': 'Please contact me about a project.',
		})

		self.assertRedirects(response, reverse('home'))
		self.assertEqual(ContactRequest.objects.count(), 1)
		self.assertFalse(ContactRequest.objects.get().is_processed)

	def test_service_detail_and_contact_submission(self):
		service = Service.objects.create(
			title='خدمات الهدم',
			slug='demolition-test',
			short_description='وصف مختصر',
			full_description='وصف تفصيلي',
		)

		detail = self.client.get(reverse('service_detail', args=[service.slug]))
		self.assertEqual(detail.status_code, 200)
		self.assertContains(detail, service.full_description)

		response = self.client.post(reverse('contact'), {
			'name': 'Test Customer',
			'phone': '+966500000000',
			'email': '',
			'service': str(service.pk),
			'message': 'Please contact me about this service.',
		})

		self.assertRedirects(response, reverse('contact'))
		self.assertEqual(ContactRequest.objects.get().service, service)


class CompanyInfoAdminTests(TestCase):
	def test_company_settings_admin_allows_only_one_record(self):
		model_admin = CompanyInfoAdmin(CompanyInfo, admin.site)
		request = RequestFactory().get('/admin/main/companyinfo/')

		self.assertTrue(model_admin.has_add_permission(request))
		CompanyInfo.objects.create()
		self.assertFalse(model_admin.has_add_permission(request))
