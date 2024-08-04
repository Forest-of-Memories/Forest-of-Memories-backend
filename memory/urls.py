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


router.register(r'common-questions', CommonQuestionViewSet, basename='common-questions')
router.register(r'personal-questions', PersonalQuestionViewSet, basename='personal-questions')
router.register(r'memories', MemoryViewSet, basename='memories')
router.register(r'shop-items', ShopItemViewSet, basename='shop-items')
router.register(r'purchase-item', PurchaseItemViewSet, basename='purchaseitem')

urlpatterns = [
    path('', include(router.urls)),
    path('common-questions/<int:family_id>/commoncomment/', CommonCommentList.as_view(), name='commoncomment-list'),
    path('home/', FamilyListView.as_view(), name='family-list'),
    path('home/<int:family_id>/', FamilyDetailView.as_view(), name='family-detail'),
    path('home/<int:family_id>/water/', WaterUpdateView.as_view(), name='water-update'),
]