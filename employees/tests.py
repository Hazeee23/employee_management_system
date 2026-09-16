from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Employee
from .forms import EmployeeForm


class EmployeeDirectoryTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='manager', password='test-password', is_staff=True)
		self.client.login(username='manager', password='test-password')
		for index in range(11):
			Employee.objects.create(
				first_name=f'Employee{index}',
				last_name='Tester',
				email=f'employee{index}@example.com',
				phone='+639171234567',
				department='Engineering' if index < 10 else 'People',
				position='Developer',
				date_hired=date(2024, 1, 1),
				salary=50000,
			)

	def test_employee_detail_page(self):
		employee = Employee.objects.first()

		response = self.client.get(f'/employees/{employee.id}/')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, employee.email)

	def test_dashboard_page(self):
		response = self.client.get('/employees/')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Team dashboard')
		self.assertContains(response, 'Department coverage')

	def test_departments_page(self):
		response = self.client.get('/employees/departments/')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Departments')
		self.assertContains(response, 'Engineering')
		self.assertContains(response, 'Average salary')

	def test_reports_page(self):
		response = self.client.get('/employees/reports/')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Hiring trend')
		self.assertContains(response, 'Department totals')
		self.assertContains(response, 'Salary range')

	def test_directory_filters_and_paginates(self):
		response = self.client.get('/employees/directory/?department=Engineering&sort=salary_high')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['employees']), 10)
		self.assertEqual(response.context['page_obj'].paginator.count, 10)
		self.assertContains(response, 'Employee0')
		self.assertNotContains(response, 'Employee10')

	def test_export_respects_department_filter(self):
		response = self.client.get('/employees/export/?department=People')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['Content-Type'], 'text/csv')
		self.assertContains(response, 'Employee10')
		self.assertNotContains(response, 'Employee0')

	def test_regular_user_can_view_but_cannot_manage(self):
		self.client.logout()
		User.objects.create_user(username='viewer', password='test-password')
		self.client.login(username='viewer', password='test-password')
		employee = Employee.objects.first()

		self.assertEqual(self.client.get('/employees/directory/').status_code, 200)
		self.assertEqual(self.client.get(f'/employees/edit/{employee.id}/').status_code, 302)
		self.assertEqual(self.client.post(f'/employees/delete/{employee.id}/').status_code, 302)
		self.assertTrue(Employee.objects.filter(id=employee.id).exists())

	def test_staff_can_bulk_delete(self):
		employee_ids = list(Employee.objects.values_list('id', flat=True)[:2])
		response = self.client.post('/employees/bulk-delete/', {'employee_ids': employee_ids})

		self.assertEqual(response.status_code, 302)
		self.assertFalse(Employee.objects.filter(id__in=employee_ids).exists())

	def test_phone_form_uses_philippine_mobile_format(self):
		data = {
			'first_name': 'Test',
			'last_name': 'Phone',
			'email': 'phone@example.com',
			'phone': '0917 123 4567',
			'department': 'People',
			'position': 'Coordinator',
			'date_hired': '2025-01-01',
			'salary': '50000',
		}
		form = EmployeeForm(data=data)

		self.assertTrue(form.is_valid())
		self.assertEqual(form.cleaned_data['phone'], '+639171234567')
