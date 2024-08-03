from django.urls import path
from .views import CommonQuestionViewSet, PersonalQuestionViewSet

common_question_list = CommonQuestionViewSet.as_view({
    'get': 'list'
})

personal_question_list = PersonalQuestionViewSet.as_view({
    'get': 'list'
})

urlpatterns = [
  path('common-questions/<int:user_id>/', common_question_list),
  path('personal-questions/<int:user_id>/', personal_question_list)
]