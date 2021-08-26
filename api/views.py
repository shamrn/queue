from rest_framework import status
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.db.models import Q

from .models import Group, Queue, Handler, Element

from .serializers import (QueueSerializer,
                          GroupSerializer,
                          HandlerSerializer,
                          ElementSerializer,
                          ElementCreateSerializer,
                          HierarchicalGroupSerializer,
                          )

from .service.element_get_pid import ElementGetPid


class GroupViewSet(viewsets.ModelViewSet):
    """
    endpoints:
    * Список групп
    * Конкретная группа
    * CRUD группы
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filterset_fields = ['parent']


class QueueViewSet(viewsets.ModelViewSet):
    """
    endpoints:
    * Список очередей
    * Конкретная очередь
    * CRUD очереди
    """

    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    filterset_fields = ['group']


class HandlerViewSet(viewsets.ModelViewSet):
    """
    endpoints:
    * Список обработчиков
    * Конкретный обработчик
    * CRUD обработчика
    """

    queryset = Handler.objects.all()
    serializer_class = HandlerSerializer
    filterset_fields = ['queue', 'handler_code', 'is_active']


class ElementViewSet(viewsets.ModelViewSet):
    """
    endpoints:
    * Список элементов
    * Конкретный элемент
    * CRUD элемента
    """

    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    filterset_fields = ['element_queue', 'handler_code', 'priority', 'status']


class QueueElementCreateView(CreateAPIView):
    """
    Добавление новых элементов в очередь,c учетом очереди
    для терминала
    """

    queryset = Queue.objects.all()
    serializer_class = ElementCreateSerializer

    def perform_create(self, serializer):
        queue = get_object_or_404(Queue, pk=self.kwargs['queue_pk'])
        serializer.save(element_queue=queue)


class ElementCountView(APIView):
    """
    Кол-во элементов в очереди
    """

    def get(self, request, queue_pk):
        queue = get_object_or_404(Queue, pk=queue_pk)
        element_count = Element.objects.filter(Q(element_queue=queue, status__isnull=True) |
                                               Q(status=1)).count()

        data = {'queue_id': queue.pk, 'element_count': element_count}
        return Response(status=status.HTTP_200_OK, data=data)


class HierarchicalGroupsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Иерархический список групп с очередями
    """
    queryset = Group.objects.all()
    serializer_class = HierarchicalGroupSerializer


class TitleGroupView(APIView):
    """
    Наименование верхней группы ( Наименование МО )
    """

    def get(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)

        while group:
            title = group.title
            group = group.parent

        data = {'title': title}
        return Response(status=status.HTTP_200_OK, data=data)


class ElementGetPidView(ElementGetPid, APIView):
    """
    Получить Entity_id (PID) пациента
    """

    def get(self, request):
        data = request.GET

        if self.check_missing_elements(data):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'error': "Необходимые поля должны быть заполнены: 'Фамилия', 'Имя', 'Год', 'Месяц', 'День'"
                })

        elif self.check_name(data):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'error': "Поля: 'Фамилия', 'Имя', 'Отчество' должны содержать символы русского алфавита"
                })

        elif self.check_date(data):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'error': "Поля: 'Год', 'Месяц', 'День' должны содержать только цифры"
                })

        element = self.get_elements(data)

        if element is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'error': 'Пациент с такими данными не существует. Обратитесь в регистратуру'
                },
            )

        elif element is False:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "error": "Найдено несколько похожих пациентов. Пожалуйста, заполните поле 'Снилс'"
                }
            )

        else:
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'pid': element[0].entity_id
                }
            )
