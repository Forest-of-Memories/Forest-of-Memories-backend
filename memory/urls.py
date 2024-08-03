from django.urls import path, include
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

# router.register(r'commoncomment', CommonCommentViewSet)
router.register(r'common-questions', CommonQuestionViewSet, basename='common-questions')
router.register(r'personal-questions', PersonalQuestionViewSet, basename='personal-questions')
router.register(r'memories', MemoryViewSet, basename='memories')
router.register(r'shop-items', ShopItemViewSet, basename='shop-items')
router.register(r'purchase-item', PurchaseItemViewSet, basename='purchaseitem')

urlpatterns = [
  path('', include(router.urls)),

  path('commoncomment/', CommonCommentList.as_view(), name='commoncomment-list'),
  path('home/', FamilyDetailView.as_view(), name='family-detail'),
  path('home/water/', WaterUpdateView.as_view(), name='water-update'),

  # path('common-questions-list/<int:user_id>/', common_question_list),
  # path('personal-questions-list/<int:user_id>/', personal_question_list),
  # path('feed/', FeedViewSet.as_view({'get': 'list', 'post': 'create'})),
  # path('feed/<int:feed_id>/', FeedViewSet.as_view({'get': 'retrieve', 'put':'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]