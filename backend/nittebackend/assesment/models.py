from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    SKILL_TYPE_CHOICES = [
        ("problem_solving", "Problem Solving"),
        ("communication", "Communication"),
        ("teamwork", "Teamwork"),
        ("technical", "Technical"),
        ("creativity", "Creativity"),
    ]

    text = models.TextField()
    skill_key = models.CharField(max_length=50, choices=SKILL_TYPE_CHOICES)
    max_score = models.PositiveIntegerField(default=5)

    def __str__(self):
        return f"{self.get_skill_key_display()}: {self.text[:40]}"


class AssessmentSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assessment_submissions")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.id} by {self.user.username}"


class Answer(models.Model):
    submission = models.ForeignKey(AssessmentSubmission, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()

    class Meta:
        unique_together = ("submission", "question")

    def __str__(self):
        return f"{self.submission_id}-{self.question_id}: {self.score}"


class ReadinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="readiness_profile")
    # Aggregated scores per skill
    problem_solving = models.FloatField(default=0)
    communication = models.FloatField(default=0)
    teamwork = models.FloatField(default=0)
    technical = models.FloatField(default=0)
    creativity = models.FloatField(default=0)
    readiness_score = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ReadinessProfile({self.user.username})={self.readiness_score:.1f}"


class CareerRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="career_recommendations")
    title = models.CharField(max_length=120)
    rationale = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.title}"
