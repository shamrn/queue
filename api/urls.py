from rest_framework import routers
from django.urls import include, path

from .views import (
    QueueViewSet,
    GroupViewSet,
    HandlerViewSet,
    ElementViewSet,
    QueueElementCreateView,
    ElementCountView,
    HierarchicalGroupsViewSet,
    TitleGroupView,
    ElementGetPidView
)

api_router = routers.DefaultRouter()
api_router.register(r'groups', GroupViewSet)
api_router.register(r'queues', QueueViewSet)
api_router.register(r'handlers', HandlerViewSet)
api_router.register(r'elements', ElementViewSet)
api_router.register(r'hierarchicals-groups', HierarchicalGroupsViewSet)

urlpatterns = [
    path('', include(api_router.urls)),
    path('queues/<queue_pk>/elements/', QueueElementCreateView.as_view()),
    path('queues-elements-count/<queue_pk>/', ElementCountView.as_view()),
    path('title-groups/<group_pk>/', TitleGroupView.as_view()),
    path('elements-pid/', ElementGetPidView.as_view()),
]
