from django.urls import path, include, re_path
########## ALL ###############
from .views import *
from rest_framework.routers import DefaultRouter

# common_question_list = CommonQuestionViewSet.as_view({
#     'get': 'list'
# })

# personal_question_list = PersonalQuestionViewSet.as_view({
#     'get': 'list'
# })


router = DefaultRouter()


router.register(r'common-questions', CommonQuestionViewSet, basename='common-questions')
# router.register(r'personal-questions', PersonalQuestionViewSet, basename='personal-questions')
router.register(r'memories', MemoryViewSet, basename='memories')
router.register(r'shop-items', ShopItemViewSet, basename='shop-items')
router.register(r'purchase-item', PurchaseItemViewSet, basename='purchaseitem')


urlpatterns = [
    path('', include(router.urls)),
    path('common-questions/<int:family_id>/commoncomment/', CommonCommentList.as_view(), name='commoncomment-list'),
    path('personal-questions/', PersonalQuestionViewSet.as_view({'get': 'list'}), name='personal-questions-list'),
    path('personal-questions/<int:family_id>/', PersonalQuestionViewSet.as_view({'get': 'list'}), name='personal-questions-family-list'),
    path('personal-questions/<int:family_id>/personalcomment/', PersonalCommentList.as_view(), name='personalcomment-list'),
    path('home/', FamilyListView.as_view(), name='family-list'),
    path('home/<int:family_id>/', FamilyDetailView.as_view(), name='family-detail'),
    path('home/<int:family_id>/water/', WaterUpdateView.as_view(), name='water-update'),
    path('feed/', FeedViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('feed/<int:feed_id>/', FeedViewSet.as_view({'get': 'retrieve', 'put':'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('common-questions/<int:family_id>/commonanswer/', CommonAnswerList.as_view(), name='commonanswer-list'),
    path('personal-questions/<int:family_id>/personalanswer/', PersonalAnswerList.as_view(), name='personalanswer-list'),
]