from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import (
    AccessPermissionForProducts,
    AccessPermissionForOrders,
)

@api_view(['GET', 'POST'])
@permission_classes([AccessPermissionForProducts]) 
def products_view(request):
    # Обработка GET-запроса: возвращаем список товаров
    if request.method == 'GET':
        # Если у пользователя есть право 'read_all_permission', показываем все товары
        if request.user_role_rule and request.user_role_rule.read_all_permission:
            # Возвращаем "все" товары (mock-данные)
            data = [
                {"id": 1, "name": "Товар 1", "owner_id": 123},
                {"id": 2, "name": "Товар 2", "owner_id": 456}
            ]
        else:
            # Иначе — возвращаем только "свои" товары
            # owner_id совпадает с id текущего пользователя
            data = [
                {"id": 1, "name": "Товар 1", "owner_id": request.user.id}
            ]
        return Response(data)

    # Обработка POST-запроса: создание нового товара
    elif request.method == 'POST':
        # Получаем имя товара из тела запроса
        name = request.data.get('name')

        # Проверим, передано ли имя
        if not name:
            return Response(
                {"error": "Поле 'name' обязательно для создания товара."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Создаём mock-объект товара
        new_product = {
            "id": 999, 
            "name": name, 
            "owner_id": request.user.id
        }
        return Response(new_product, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AccessPermissionForOrders]) 
def orders_view(request):
    # Обработка GET-запроса: возвращаем список заказов
    if request.method == 'GET':
        data = [
            {"id": 1, "status": "paid", "owner_id": request.user.id},
            {"id": 2, "status": "pending", "owner_id": request.user.id}
        ]
        return Response(data)

    # Обработка PUT-запроса: обновление заказа
    elif request.method == 'PUT':
        updated_order = {"id": 1, "status": "shipped", "owner_id": request.user.id}
        return Response(updated_order)

    # Обработка DELETE-запроса: удаление заказа
    elif request.method == 'DELETE':
        return Response({"message": "Заказ удален"}, status=status.HTTP_204_NO_CONTENT)