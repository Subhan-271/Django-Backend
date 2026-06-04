from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated",
    )

    class Meta:
        abstract = True


class Program(TimeStampedModel):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Course(TimeStampedModel):
    COURSE_CLASS_CHOICES = (
        ("CORE", "Core"),
        ("GER", "General"),
        ("ELECTIVE", "Elective"),
    )

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    course_class = models.CharField(
        max_length=20,
        choices=COURSE_CLASS_CHOICES,
        default="CORE",   # ✅ IMPORTANT
    )

    credit_hours_theory = models.PositiveIntegerField(default=0)
    credit_hours_lab = models.PositiveIntegerField(default=0)

    pre_requisites = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="pre_required_for"
    )
    co_requisites = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="co_required_for"
    )

    def __str__(self):
        return f"{self.code} - {self.name}"


class PLO(TimeStampedModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"PLO - {self.program.code}"


class CLO(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"CLO - {self.course.code}"
