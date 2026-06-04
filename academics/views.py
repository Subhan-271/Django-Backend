from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Program, Course, PLO, CLO
from .serializers import (
    ProgramSerializer,
    CourseSerializer,
    PLOSerializer,
    CLOSerializer,
)
import pandas as pd


# =========================
# PROGRAM
# =========================
class ProgramViewSet(ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    @action(detail=False, methods=["post"], url_path="bulk-import")
    def bulk_import(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "Excel file required"}, status=400)

        df = pd.read_excel(file)

        for _, row in df.iterrows():
            Program.objects.get_or_create(
                code=row["code"],
                defaults={"name": row["name"]},
            )

        return Response({"message": "Programs imported successfully"})


# =========================
# COURSE
# =========================
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=False, methods=["post"], url_path="bulk-import")
    def bulk_import(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "Excel file required"}, status=400)

        df = pd.read_excel(file)

        for _, row in df.iterrows():
            program = Program.objects.get(code=row["program_code"])

            course, created = Course.objects.get_or_create(
                code=row["code"],
                defaults={
                    "name": row["name"],
                    "course_class": row["course_class"],  # CORE / GER
                    "credit_hours_theory": row["credit_hours_theory"],
                    "credit_hours_lab": row["credit_hours_lab"],
                    "program": program,
                },
            )

            # -------- PRE-REQUISITES --------
            if not pd.isna(row.get("pre_requisites")):
                pre_codes = str(row["pre_requisites"]).split(",")
                for pre_code in pre_codes:
                    pre_course = Course.objects.filter(
                        code=pre_code.strip()
                    ).first()
                    if pre_course:
                        course.pre_requisites.add(pre_course)

            # -------- CO-REQUISITES --------
            if not pd.isna(row.get("co_requisites")):
                co_codes = str(row["co_requisites"]).split(",")
                for co_code in co_codes:
                    co_course = Course.objects.filter(
                        code=co_code.strip()
                    ).first()
                    if co_course:
                        course.co_requisites.add(co_course)

        return Response({"message": "Courses imported successfully"})


# =========================
# PLO
# =========================
class PLOViewSet(ModelViewSet):
    queryset = PLO.objects.all()
    serializer_class = PLOSerializer

    @action(detail=False, methods=["post"], url_path="bulk-import")
    def bulk_import(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "Excel file required"}, status=400)

        df = pd.read_excel(file)

        for _, row in df.iterrows():
            program = Program.objects.get(code=row["program_code"])

            PLO.objects.create(
                program=program,
                description=row["description"],
            )

        return Response({"message": "PLOs imported successfully"})


# =========================
# CLO
# =========================
class CLOViewSet(ModelViewSet):
    queryset = CLO.objects.all()
    serializer_class = CLOSerializer

    @action(detail=False, methods=["post"], url_path="bulk-import")
    def bulk_import(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "Excel file required"}, status=400)

        df = pd.read_excel(file)

        for _, row in df.iterrows():
            course = Course.objects.get(code=row["course_code"])

            CLO.objects.create(
                course=course,
                description=row["description"],
            )

        return Response({"message": "CLOs imported successfully"})
