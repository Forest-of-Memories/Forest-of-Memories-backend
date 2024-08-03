from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommonQuestionViewSet, PersonalQuestionViewSet, MemoryViewSet, ShopItemViewSet, PurchaseItemViewSet

router = DefaultRouter()
router.register(r'common-questions', CommonQuestionViewSet, basename='common-questions')
router.register(r'personal-questions', PersonalQuestionViewSet, basename='personal-questions')
router.register(r'memories', MemoryViewSet, basename='memories')
router.register(r'shop-items', ShopItemViewSet, basename='shop-items')
router.register(r'purchase-item', PurchaseItemViewSet, basename='purchaseitem')


urlpatterns = [
    path('', include(router.urls)),
]
