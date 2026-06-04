from rest_framework.routers import DefaultRouter
from .views import ProgramViewSet, CourseViewSet, PLOViewSet, CLOViewSet

router = DefaultRouter(trailing_slash=True)

router.register(
    r"programs",
    ProgramViewSet,
    basename="program"
)
router.register(
    r"courses",
    CourseViewSet,
    basename="course"
)
router.register(
    r"plos",
    PLOViewSet,
    basename="plo"
)
router.register(
    r"clos",
    CLOViewSet,
    basename="clo"
)


urlpatterns = router.urls
