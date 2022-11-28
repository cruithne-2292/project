# serializers.py
from rest_framework import serializers

from .models import Employee
from .models import Department

class EmployeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Employee
		fields = (
			'id', 
			'first_name', 
			'last_name',
			'position',
			'salary',
			'age',
			'department_id',
		)

class DepartmentCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Department
		fields = (
			'id', 
			'department_name',
			'chief',
		)

class DepartmentListSerializer(serializers.ModelSerializer):
	department_id = serializers.IntegerField()
	# department_name = serializers.CharField(source='department_id.department_name', default=None)
	employee_count = serializers.IntegerField()
	salary_sum = serializers.DecimalField(10,2)
	class Meta:
		model = Employee
		fields = (
			'department_id', 
			'employee_count', 
			'salary_sum', 
			# 'department_name',
		)

