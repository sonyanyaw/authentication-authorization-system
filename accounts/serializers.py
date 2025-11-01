from rest_framework import serializers
from .models import User, Role, BusinessElement, AccessRule

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # Поле password будет приниматься при создании/обновлении, но не будет включено в JSON-ответ
    password = serializers.CharField(write_only=True) 
    # Поле role будет вложенным объектом (RoleSerializer), и только для чтения (при выводе)
    role = RoleSerializer(read_only=True)  

    class Meta:
        # Указываем модель
        model = User
        # Поля, которые будут сериализованы/десериализованы
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'email', 'role', 'is_active', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Пароль не будет в ответе
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        # Устанавливаем роль по умолчанию ('user'), если она не передана
        validated_data.setdefault('role', Role.objects.get(name='user')) 
        # Создаём экземпляр модели User с оставшимися данными
        user = User(**validated_data)
        # Вызываем метод модели для хеширования пароля
        user.set_password(password)  
        user.save()
        return user

    def update(self, instance, validated_data):
        # Обновляем только переданные поля
        for attr, value in validated_data.items():
            if attr == 'password':
                # Если обновляется пароль — хешируем
                instance.set_password(value)  
            else:
                # В остальных случаях просто присваиваем значение атрибуту
                setattr(instance, attr, value)
        instance.save()
        return instance

# class BusinessElementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BusinessElement
#         fields = '__all__'

class AccessRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRule
        fields = '__all__'