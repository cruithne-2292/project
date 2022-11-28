from rest_framework import routers
from app.views import EmployeeViewSet
from app.views import DepartmentViewSet

router = routers.DefaultRouter()
router.register('employee', EmployeeViewSet, basename='employee')
router.register('department', DepartmentViewSet, basename='department')
