from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

# 👇 ye aap ka PURANA import / logic rehne do
# from .models import Assessment
# from .serializers import AssessmentSerializer
# from .services.old_logic import something

# 👇 sirf ye naya import add hota hai
from .services.gemini_service import generate_assessment_pdf


class AssessmentViewSet(ViewSet):
    """
    EXISTING AssessmentViewSet
    (purane methods bilkul same rahen ge)
    """

    # ===============================
    # 👇 PURANA METHOD (EXAMPLE)
    # ===============================
    def list(self, request):
        # aap ka existing logic
        return Response({"message": "Old assessment list working"})

    def create(self, request):
        # aap ka existing logic
        return Response({"message": "Old create assessment working"})

    # ===============================
    # 👇 NEW METHOD (ONLY ADD THIS)
    # ===============================
    @action(detail=False, methods=["post"], url_path="generate-pdf")
    def generate_pdf(self, request):
        """
        Gemini-based PDF generation
        (new feature, purana code untouched)
        """
        try:
            data = request.data
            filename = generate_assessment_pdf(data)

            return Response(
                {
                    "message": "Assessment PDF generated successfully",
                    "pdfUrl": f"http://127.0.0.1:8000/generated_pdfs/{filename}"
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ===============================
# 👇 QuestionViewSet AS IT WAS
# ===============================
class QuestionViewSet(ViewSet):
    def list(self, request):
        return Response({"message": "Questions working"})
