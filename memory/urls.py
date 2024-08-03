from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommonQuestionViewSet, PersonalQuestionViewSet

router = DefaultRouter()
router.register(r'common-questions', CommonQuestionViewSet, basename='common-questions')
router.register(r'personal-questions', PersonalQuestionViewSet, basename='personal-questions')

urlpatterns = [
    path('', include(router.urls)),
]
