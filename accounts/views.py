from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import User, Role, AccessRule
from .serializers import UserSerializer, AccessRuleSerializer

# Create your views here.
@api_view(['POST'])
def register_view(request):
    # Получаем данные из тела запроса
    data = request.data
    email = data.get('email')
    password = data.get('password')
    password_confirm = data.get('password_confirm')

    # Проверяем, совпадают ли пароли
    if password != password_confirm:
        return Response({'error': 'Пароли не совпадают'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Проверяем, существует ли уже пользователь с таким email
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Пользователь с таким email уже существует'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Находим роль "user" по умолчанию
    try:
        default_role = Role.objects.get(name='user')  
    except Role.DoesNotExist:
        # Если роль "user" не создана, возвращаем ошибку сервера
        return Response({'error': 'Роль "user" не найдена в базе данных'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
     # Создаём нового пользователя с указанными данными
    user = User(
        first_name = data.get('first_name'),
        last_name = data.get('last_name', ''),
        patronymic = data.get('patronymic', ''),
        email = email,
        role = default_role
    )
    user.set_password(password)  
    user.save() 

    # Генерируем JWT-токен для нового пользователя
    token = user.generate_jwt()

    return Response({'token': token}, status=status.HTTP_201_CREATED)

# --- Вход пользовавтеля ---
@api_view(['POST'])
def login_view(request):
    # Получаем email и password из тела запроса
    email = request.data.get('email')
    password = request.data.get('password')

    # Проверяем, существует ли пользователь с таким email и он активен
    try:
        user = User.objects.get(email=email, is_active=True)
    except User.DoesNotExist:
        # Если пользователя нет или он неактивен, возвращаем 401
        return Response({'error': 'Неверный email или пароль'}, status=status.HTTP_401_UNAUTHORIZED)

    # Проверяем, совпадает ли введённый пароль с хешем в БД
    if not user.check_password(password):
        return Response({'error': 'Неверный email или пароль'}, status=status.HTTP_401_UNAUTHORIZED)

    # Генерируем JWT-токен
    token = user.generate_jwt()
    # Возвращаем токен с кодом 200 (OK)
    return Response({'token': token}, status=status.HTTP_200_OK)

# --- Выход пользователя ---
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    return Response({'message': 'Вы успешно вышли'}, status=status.HTTP_200_OK)


# --- Профиль ---
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    # request.user — это объект User
    user = request.user 

    if request.method == 'GET':
        # Возвращаем данные пользователя в JSON
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Обновляем только указанные поля профиля 
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.patronymic = request.data.get('patronymic', user.patronymic)
        user.save()
        # Возвращаем обновлённые данные
        return Response(UserSerializer(user).data)

    elif request.method == 'DELETE':
        # Мягкое удаление is_active=False
        user.is_active = False
        user.save()
        return Response({'message': 'Аккаунт удален'}, status=status.HTTP_204_NO_CONTENT)


# --- Права доступа (только для админа) ---
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def access_rules_view(request):
    # Проверяем, является ли пользователь администратором
    if not hasattr(request.user, 'role') or request.user.role.name != 'admin':
        return Response({'error': 'Нет прав'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # Возвращаем список всех прав доступа
        rules = AccessRule.objects.all()
        serializer = AccessRuleSerializer(rules, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Создаём новое правило доступа
        serializer = AccessRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Возвращаем созданное правило
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Если данные невалидны — возвращаем ошибки
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- Конкретное правило доступа (только для админа) ---
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def access_rule_detail_view(request, rule_id):
    # Пытаемся найти правило доступа по ID
    try:
        rule = AccessRule.objects.get(id=rule_id)
    except AccessRule.DoesNotExist:
        return Response({'error': 'Правило не найдено'}, status=status.HTTP_404_NOT_FOUND)

    # Проверяем, что пользователь — админ
    if request.user.role.name != 'admin':
        return Response({'error': 'Нет прав'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # Возвращаем конкретное правило
        serializer = AccessRuleSerializer(rule)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']: 
        # PUT — полное обновление, PATCH — частичное
        # partial=True позволяет обновлять только переданные поля
        partial = request.method == 'PATCH'
        serializer = AccessRuleSerializer(rule, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
