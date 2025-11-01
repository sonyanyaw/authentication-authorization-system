from django.core.management.base import BaseCommand
from accounts.models import Role, BusinessElement, AccessRule, User

class Command(BaseCommand):
    help = 'Инициализация тестовыми данными: роли, элементы, правила, пользователи.'

    def handle(self, *args, **options):
        self.stdout.write('Создание ролей...')
        admin_role, _ = Role.objects.get_or_create(name='admin')
        user_role, _ = Role.objects.get_or_create(name='user')
        manager_role, _ = Role.objects.get_or_create(name='manager')

        self.stdout.write('Создание бизнес-элементов...')
        products, _ = BusinessElement.objects.get_or_create(name='products')
        orders, _ = BusinessElement.objects.get_or_create(name='orders')
        users, _ = BusinessElement.objects.get_or_create(name='users')
        access_rules_element, _ = BusinessElement.objects.get_or_create(name='access_rules')

        self.stdout.write('Создание прав доступа...')

        # Права для администратора
        AccessRule.objects.get_or_create(
            role=admin_role,
            business_element=products,  
            read_permission=True,
            read_all_permission=True,
            create_permission=True,
            update_permission=True,
            update_all_permission=True,
            delete_permission=True,
            delete_all_permission=True,
        )
        AccessRule.objects.get_or_create(
            role=admin_role,
            business_element=orders,  
            read_permission=True,
            read_all_permission=True,
            create_permission=True,
            update_permission=True,
            update_all_permission=True,
            delete_permission=True,
            delete_all_permission=True,
        )
        AccessRule.objects.get_or_create(
            role=admin_role,
            business_element=users,  
            read_permission=True,
            read_all_permission=True,
            create_permission=False,
            update_permission=True,
            update_all_permission=True,
            delete_permission=True,
            delete_all_permission=True,
        )
        AccessRule.objects.get_or_create(
            role=admin_role,
            business_element=access_rules_element,  
            read_permission=True,
            read_all_permission=True,
            create_permission=True,
            update_permission=True,
            update_all_permission=True,
            delete_permission=True,
            delete_all_permission=True,
        )

        # Права для обычного пользователя
        AccessRule.objects.get_or_create(
            role=user_role,
            business_element=products,  
            read_permission=True,
            read_all_permission=False,  
            create_permission=True,
            update_permission=False,
            update_all_permission=False,
            delete_permission=False,
            delete_all_permission=False,
        )
        AccessRule.objects.get_or_create(
            role=user_role,
            business_element=orders,  
            read_permission=True,
            read_all_permission=False,  
            create_permission=True,
            update_permission=False,
            update_all_permission=False,
            delete_permission=False,
            delete_all_permission=False,
        )

        # Права для менеджера
        AccessRule.objects.get_or_create(
            role=manager_role,
            business_element=orders,  
            read_permission=True,
            read_all_permission=True,  
            create_permission=False,
            update_permission=True,
            update_all_permission=True,
            delete_permission=False,
            delete_all_permission=False,
        )
        AccessRule.objects.get_or_create(
            role=manager_role,
            business_element=products,  
            read_permission=True,
            read_all_permission=False,  
            create_permission=False,  
            update_permission=False,
            update_all_permission=False,
            delete_permission=False,
            delete_all_permission=False,
        )

        self.stdout.write('Создание пользователей...')
        admin_user, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'first_name': 'Админ',
                'last_name': 'Главный',
                'role': admin_role,
                'is_active': True
            }
        )
        if created:
            admin_user.set_password('adminpass123')
            admin_user.save()
            self.stdout.write(f'Создан админ: {admin_user.email}')

        user_user, created = User.objects.get_or_create(
            email='user@example.com',
            defaults={
                'first_name': 'Обычный',
                'last_name': 'Пользователь',
                'role': user_role,
                'is_active': True
            }
        )
        if created:
            user_user.set_password('userpass123')
            user_user.save()
            self.stdout.write(f'Создан пользователь: {user_user.email}')

        manager_user, created = User.objects.get_or_create(
            email='manager@example.com',
            defaults={
                'first_name': 'Менеджер',
                'last_name': 'По Заказам',
                'role': manager_role,
                'is_active': True
            }
        )
        if created:
            manager_user.set_password('managerpass123')
            manager_user.save()
            self.stdout.write(f'Создан менеджер: {manager_user.email}')

        self.stdout.write(
            self.style.SUCCESS('Тестовые данные успешно созданы!')
        )
