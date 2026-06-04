from rest_framework.routers import DefaultRouter
from .views import AssessmentViewSet, QuestionViewSet

router = DefaultRouter()
router.register('', AssessmentViewSet, basename='assessment')
router.register('questions', QuestionViewSet, basename='questions')

urlpatterns = router.urls
