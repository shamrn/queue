from django.shortcuts import render
from api.models import Queue, Element, Group
from datetime import datetime
from django.conf import settings


def queues_list(request):
    """
    Представление списка всех очередей.
    """
    group_name = settings.GROUP_NAME
    groups = Group.objects.all()
    context = {'group_name': group_name, 'groups': groups}
    return render(request, 'scoreboard/queues_list.html', context)


def queue(request, queue_pk):
    """
    Представление очереди и ее элементов.
    """
    time = datetime.now().time()
    left_title = settings.BOARD_LEFT_TITLE
    right_title = settings.BOARD_RIGHT_TITLE
    queue = Queue.objects.get(pk=queue_pk)
    elements = Element.objects.filter(element_queue=queue, status__isnull=True)[0:12]
    elements_handler = Element.objects.filter(element_queue=queue, status=1)[0:6]

    context = {'time': time, 'queue': queue, 'left_title': left_title, 'right_title': right_title,
               'elements': elements, 'elements_handler': elements_handler}

    return render(request, 'scoreboard/scoreboard.html', context)
