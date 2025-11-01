from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import BusinessElement, AccessRule

class AccessPermission(BasePermission):
    element_name = None 

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            # DRF сам вызывает 401, если пользователь не аутентифицирован
            return False

        try:
            business_element = BusinessElement.objects.get(name=self.element_name)
        except BusinessElement.DoesNotExist:
            raise PermissionDenied("Объект не найден в системе контроля доступа.")

        try:
            rule = AccessRule.objects.get(role=user.role, business_element=business_element)
        except AccessRule.DoesNotExist:
            raise PermissionDenied("У вас нет прав на доступ к этому ресурсу.")

        method = request.method

        if method == 'GET':
            if rule.read_all_permission or rule.read_permission:
                request.user_role_rule = rule
                return True
        elif method == 'POST':
            if rule.create_permission:
                request.user_role_rule = rule
                return True
        elif method in ['PUT', 'PATCH']:
            if rule.update_all_permission or rule.update_permission:
                request.user_role_rule = rule
                return True
        elif method == 'DELETE':
            if rule.delete_all_permission or rule.delete_permission:
                request.user_role_rule = rule
                return True

        raise PermissionDenied("У вас нет прав на это действие.")


class AccessPermissionForProducts(AccessPermission):
    element_name = 'products'

class AccessPermissionForOrders(AccessPermission):
    element_name = 'orders'

class AccessPermissionForUsers(AccessPermission):
    element_name = 'users'

class AccessPermissionForAccessRules(AccessPermission):
    element_name = 'access_rules'