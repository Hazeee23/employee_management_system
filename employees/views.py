import csv

from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Min, Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .models import Employee
from .forms import EmployeeForm

staff_required = user_passes_test(lambda user: user.is_staff)


def filtered_employees(request):
    employees = Employee.objects.all()
    search = request.GET.get('search', '')
    department = request.GET.get('department', '')
    position = request.GET.get('position', '')

    if search:
        employees = employees.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
            | Q(department__icontains=search)
            | Q(position__icontains=search)
        )
    if department:
        employees = employees.filter(department=department)
    if position:
        employees = employees.filter(position=position)

    return employees, search, department, position


@login_required
def dashboard(request):
    return render(
        request,
        'dashboard.html',
        {
            'total_employees': Employee.objects.count(),
            'department_count': Employee.objects.values('department').distinct().count(),
            'recent_hires': Employee.objects.order_by('-date_hired', 'last_name')[:4],
            'average_salary': Employee.objects.aggregate(value=Avg('salary'))['value'],
            'department_summary': Employee.objects.values('department').annotate(total=Count('id')).order_by('-total', 'department'),
            'hire_summary': Employee.objects.values('date_hired__year').annotate(total=Count('id')).order_by('date_hired__year'),
            'salary_min': Employee.objects.aggregate(value=Min('salary'))['value'],
            'salary_max': Employee.objects.aggregate(value=Max('salary'))['value'],
        },
    )


@login_required
def departments(request):
    department_summary = Employee.objects.values('department').annotate(
        total=Count('id'),
        average_salary=Avg('salary'),
        latest_hire=Max('date_hired'),
    ).order_by('department')
    return render(request, 'departments.html', {'department_summary': department_summary})


@login_required
def reports(request):
    return render(
        request,
        'reports.html',
        {
            'total_employees': Employee.objects.count(),
            'average_salary': Employee.objects.aggregate(value=Avg('salary'))['value'],
            'salary_min': Employee.objects.aggregate(value=Min('salary'))['value'],
            'salary_max': Employee.objects.aggregate(value=Max('salary'))['value'],
            'department_summary': Employee.objects.values('department').annotate(
                total=Count('id'), average_salary=Avg('salary')
            ).order_by('-total', 'department'),
            'hire_summary': Employee.objects.values('date_hired__year').annotate(
                total=Count('id')
            ).order_by('date_hired__year'),
        },
    )


@login_required
def employee_list(request):
    employees, search, department, position = filtered_employees(request)
    sort = request.GET.get('sort', 'name')

    sort_options = {
        'name': ('last_name', 'first_name'),
        'name_desc': ('-last_name', '-first_name'),
        'newest': ('-date_hired', 'last_name'),
        'oldest': ('date_hired', 'last_name'),
        'salary_high': ('-salary', 'last_name'),
        'salary_low': ('salary', 'last_name'),
    }
    if sort not in sort_options:
        sort = 'name'
    employees = employees.order_by(*sort_options[sort])

    paginator = Paginator(employees, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(
        request,
        'employee_list.html',
        {
            'employees': page_obj,
            'page_obj': page_obj,
            'search': search,
            'department': department,
            'position': position,
            'sort': sort,
            'departments': Employee.objects.values_list('department', flat=True).distinct().order_by('department'),
            'positions': Employee.objects.values_list('position', flat=True).distinct().order_by('position'),
            'total_employees': Employee.objects.count(),
            'department_count': Employee.objects.values('department').distinct().count(),
        }
    )


@login_required
def export_employees(request):
    employees, _, _, _ = filtered_employees(request)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    writer = csv.writer(response)
    writer.writerow(['First name', 'Last name', 'Email', 'Phone', 'Department', 'Position', 'Date hired', 'Salary'])
    for employee in employees.order_by('last_name', 'first_name'):
        writer.writerow([
            employee.first_name,
            employee.last_name,
            employee.email,
            employee.phone,
            employee.department,
            employee.position,
            employee.date_hired,
            employee.salary,
        ])
    return response


@login_required
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'employee_detail.html', {'employee': employee})


@login_required
@staff_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(
        request,
        'add_employee.html',
        {'form': form}
    )
@login_required
@staff_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)

        if form.is_valid():
            form.save()
            messages.success(request, 'Employee details updated successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(
        request,
        'edit_employee.html',
        {'form': form}
    )

@login_required
@staff_required
def delete_employee(request, employee_id):
    if request.method != 'POST':
        return redirect('employee_list')
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    messages.success(request, 'Employee record deleted.')

    return redirect('employee_list')


@login_required
@staff_required
def bulk_delete_employees(request):
    if request.method != 'POST':
        return redirect('employee_list')
    employee_ids = request.POST.getlist('employee_ids')
    deleted_count, _ = Employee.objects.filter(id__in=employee_ids).delete()
    if deleted_count:
        messages.success(request, f'{deleted_count} employee record(s) deleted.')
    else:
        messages.info(request, 'Select at least one employee to delete.')
    return redirect('employee_list')