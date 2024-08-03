from django.urls import path
from .views import CommonQuestionViewSet, PersonalQuestionViewSet, FeedViewSet

common_question_list = CommonQuestionViewSet.as_view({
    'get': 'list'
})

personal_question_list = PersonalQuestionViewSet.as_view({
    'get': 'list'
})



urlpatterns = [
  path('common-questions-list/<int:user_id>/', common_question_list),
  path('personal-questions-list/<int:user_id>/', personal_question_list),
  path('feed/', FeedViewSet.as_view({'get': 'list', 'post': 'create'})),
  path('feed/<int:feed_id>/', FeedViewSet.as_view({'get': 'retrieve', 'put':'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]