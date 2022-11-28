from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum

from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from app.models import Employee
from app.serializers import EmployeeSerializer
from app.paginations import EmployeePagination

from app.models import Department
from app.serializers import DepartmentCreateSerializer
from app.serializers import DepartmentListSerializer

class EmployeeViewSet(viewsets.GenericViewSet):
	permission_classes = [IsAuthenticated]
	serializer_class = EmployeeSerializer
	pagination_class = EmployeePagination

	def list(self, request):
		# define filters
		filters = {}
		last_name = request.GET.get('last_name')
		department_id = request.GET.get('department_id')
		if last_name: filters['last_name'] = last_name;
		if department_id: filters['department_id'] = department_id;
		# fetch data
		employees_qs = self.paginate_queryset(Employee.objects.select_related('department_id').filter(**filters))
		employee_serializers = EmployeeSerializer(employees_qs, many=True)
		return Response(employee_serializers.data, status=status.HTTP_200_OK)

	def retrieve(self, request, pk=None):
		employee = get_object_or_404(Employee, id=pk)
		employee_serializers = self.serializer_class(employee)
		return Response(employee_serializers.data, status=status.HTTP_200_OK)

	def create(self, request):
		employee_serializers = self.serializer_class(data=request.data)
		employee_serializers.is_valid(raise_exception=True)
		employee_serializers.save()
		return Response(employee_serializers.data, status=status.HTTP_201_CREATED)

	def delete(self,request, pk=None):
		employee = get_object_or_404(Employee, id=pk)
		employee.delete()
		return Response({'id': pk}, status=status.HTTP_204_NO_CONTENT)


class DepartmentPermission(permissions.BasePermission):

	def has_permission(self, request, view):
		return True if request.method in ['GET'] else False


class DepartmentViewSet(viewsets.GenericViewSet):
	permission_classes = [IsAuthenticated | DepartmentPermission]
	serializer_class = DepartmentListSerializer
	pagination_class = None

	def list(self, request):
		query_set = Employee.objects.values('department_id').annotate(employee_count=Count('id'), salary_sum=Sum('salary'))
		department_serializers = self.serializer_class(query_set, many=True)
		return Response(department_serializers.data, status=status.HTTP_200_OK)

	def retrieve(self, request, pk=None):
		department = get_object_or_404(Department, id=pk)
		department_serializers = self.serializer_class(department)
		return Response(department_serializers.data, status=status.HTTP_200_OK)

	def create(self, request):
		department_serializers = DepartmentCreateSerializer(data=request.data)
		department_serializers.is_valid(raise_exception=True)
		department_serializers.save()
		return Response(department_serializers.data, status=status.HTTP_201_CREATED)

	def delete(self,request, pk=None):
		department = get_object_or_404(Department, id=pk)
		department.delete()
		return Response({'id': pk}, status=status.HTTP_204_NO_CONTENT)
