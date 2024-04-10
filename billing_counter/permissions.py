from rest_framework.permissions import BasePermission
from billing_counter.models import Employee


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        employee = Employee.objects.get(user=request.user)
        if employee:
            return True
        return False
