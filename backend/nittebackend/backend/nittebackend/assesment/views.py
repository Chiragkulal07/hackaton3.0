from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils import timezone
import json

from .models import Question, AssessmentSubmission, Answer, ReadinessProfile, CareerRecommendation


def home(request):
    return JsonResponse({"message": "Assessment API is running"})


def get_questions(request):
    questions = list(Question.objects.all().values("id", "text", "skill_key", "max_score"))
    return JsonResponse({"questions": questions})


def _aggregate_scores(submission: AssessmentSubmission) -> dict:
    totals = {"problem_solving": [], "communication": [], "teamwork": [], "technical": [], "creativity": []}
    for ans in submission.answers.select_related("question"):
        totals[ans.question.skill_key].append((ans.score, ans.question.max_score))
    result = {}
    for key, pairs in totals.items():
        if not pairs:
            result[key] = 0.0
            continue
        scored = sum(s for s, _ in pairs)
        max_s = sum(m for _, m in pairs)
        result[key] = round((scored / max_s) * 100.0, 2) if max_s else 0.0
    return result


def _compute_readiness(score_by_skill: dict) -> float:
    weights = {
        "problem_solving": 0.3,
        "communication": 0.25,
        "teamwork": 0.15,
        "technical": 0.25,
        "creativity": 0.05,
    }
    readiness = 0.0
    for k, w in weights.items():
        readiness += score_by_skill.get(k, 0.0) * w
    return round(readiness, 2)


def _generate_recommendations(user: User, score_by_skill: dict) -> list:
    recommendations = []
    top_skill = max(score_by_skill, key=lambda k: score_by_skill[k]) if score_by_skill else None
    if top_skill == "technical":
        recommendations.append(("Software Engineer", "Strong technical aptitude"))
        recommendations.append(("Data Analyst", "Good quantitative reasoning"))
    elif top_skill == "communication":
        recommendations.append(("Customer Success Associate", "High communication competency"))
        recommendations.append(("Business Analyst", "Translate requirements clearly"))
    elif top_skill == "problem_solving":
        recommendations.append(("Product Manager", "Strong problem decomposition"))
        recommendations.append(("Operations Analyst", "Optimization mindset"))
    elif top_skill == "teamwork":
        recommendations.append(("Project Coordinator", "Collaboration strength"))
    else:
        recommendations.append(("Generalist Trainee", "Balanced skill profile"))

    CareerRecommendation.objects.filter(user=user).delete()
    objects = [
        CareerRecommendation(user=user, title=title, rationale=rationale)
        for title, rationale in recommendations
    ]
    CareerRecommendation.objects.bulk_create(objects)
    return [
        {"title": obj.title, "rationale": obj.rationale}
        for obj in objects
    ]


@csrf_exempt
def submit_assessment(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    username = payload.get("username")
    answers = payload.get("answers")  # [{question_id, score}]
    if not username or not isinstance(answers, list):
        return HttpResponseBadRequest("username and answers[] required")

    user, _ = User.objects.get_or_create(username=username)
    submission = AssessmentSubmission.objects.create(user=user, created_at=timezone.now())

    answer_objs = []
    for item in answers:
        qid = item.get("question_id")
        score = item.get("score")
        if qid is None or score is None:
            continue
        try:
            q = Question.objects.get(id=qid)
        except Question.DoesNotExist:
            continue
        score_int = int(score)
        if score_int < 0:
            score_int = 0
        if score_int > q.max_score:
            score_int = q.max_score
        answer_objs.append(Answer(submission=submission, question=q, score=score_int))
    if answer_objs:
        Answer.objects.bulk_create(answer_objs)

    skill_scores = _aggregate_scores(submission)
    readiness = _compute_readiness(skill_scores)

    profile, _ = ReadinessProfile.objects.get_or_create(user=user)
    profile.problem_solving = skill_scores.get("problem_solving", 0.0)
    profile.communication = skill_scores.get("communication", 0.0)
    profile.teamwork = skill_scores.get("teamwork", 0.0)
    profile.technical = skill_scores.get("technical", 0.0)
    profile.creativity = skill_scores.get("creativity", 0.0)
    profile.readiness_score = readiness
    profile.save()

    recs = _generate_recommendations(user, skill_scores)

    return JsonResponse({
        "submission_id": submission.id,
        "scores": skill_scores,
        "readiness_score": readiness,
        "recommendations": recs,
    })


def get_profile(request, username: str):
    try:
        user = User.objects.get(username=username)
        profile = user.readiness_profile
    except (User.DoesNotExist, ReadinessProfile.DoesNotExist):
        return HttpResponseBadRequest("User or profile not found")

    recs = list(
        user.career_recommendations.all().values("title", "rationale", "created_at")
    )
    return JsonResponse({
        "user": username,
        "scores": {
            "problem_solving": profile.problem_solving,
            "communication": profile.communication,
            "teamwork": profile.teamwork,
            "technical": profile.technical,
            "creativity": profile.creativity,
        },
        "readiness_score": profile.readiness_score,
        "recommendations": recs,
    })