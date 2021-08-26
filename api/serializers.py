from rest_framework import serializers
from .models import Group, Queue, Handler, Element


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор группы
    """

    class Meta:
        model = Group
        fields = '__all__'


class QueueSerializer(serializers.ModelSerializer):
    """
    Сериализатор очереди
    """

    class Meta:
        model = Queue
        fields = '__all__'


class HandlerSerializer(serializers.ModelSerializer):
    """
    Сериализатор обработчика
    """

    class Meta:
        model = Handler
        fields = '__all__'


class ElementSerializer(serializers.ModelSerializer):
    """
    Сериализатор элемента
    """

    class Meta:
        model = Element
        fields = '__all__'


class ElementCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания элемента с учетом очереди
    """

    order_queue = serializers.SerializerMethodField()

    class Meta:
        model = Element
        fields = (
            'entity_id',
            'title',
            'handler_code',
            'note',
            'priority',
            'status',
            'order_queue'
        )

    def create(self, request):
        queue = request["element_queue"]

        last_element = Element.objects.filter(element_queue=queue).last()
        if last_element:
            self._order_queue = last_element.order_queue + 1
        else:
            self._order_queue = 1

        element = Element.objects.create(order_queue=self._order_queue, **request)
        return element

    def get_order_queue(self, obj):
        return self._order_queue


class RecursiveField(serializers.Serializer):
    """
    Используйте этот класс, для рекурсивного вывода данных
    """

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class HierarchicalGroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор групп с вложенными группами и очередями
    """
    parent = serializers.StringRelatedField(read_only=True)
    children = RecursiveField(many=True, read_only=True)
    queues = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'parent', 'title', 'queues', 'children')
