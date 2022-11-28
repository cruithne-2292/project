from django.db import models

# Create your models here.
class Employee(models.Model):

	first_name = models.CharField(max_length=32)
	last_name = models.CharField(max_length=32)
	position = models.SmallIntegerField()
	salary = models.DecimalField(max_digits=12, decimal_places=2)
	age = models.SmallIntegerField()
	department_id = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return f'{self.first_name} {self.last_name}'
	class Meta:
		indexes = [
		    models.Index(fields=['last_name', 'department_id'], name='last_name_department_id_idx'),
		]

class Department(models.Model):

	department_name = models.CharField(max_length=32)
	chief = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return f'{self.department_name}'
