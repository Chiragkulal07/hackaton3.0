
# 🔹 Django / DRF imports
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

# 🔹 Django models
from django.contrib.auth.models import User  # if you are using default User model
from models import QuizResult  # your model to save scores

# 🔹 External libraries
import openai
import os
import json
load_dotenv() 

# 🔹 Set OpenAI API key from settings.py
openai.api_key =  os.getenv("OPENAI_API_KEY")


@api_view(['POST'])
def feedback_viewt(request):
    user_id = request.data.get('user_id')
    category = request.data.get('category')
    answers = request.data.get('answers', [])

    total_score = 0
    for ans in answers:
        if ans['chosen_option'] == ans['correct_option']:
            total_score += 1  # 1 point per correct answer

    # Save in DB
    user = User.objects.get(id=user_id)
    QuizResult.objects.create(
        user=user,
        category=category,
        score=total_score
    )

    # Generate career suggestions using AI
    career_prompt = f"""
    A student scored {total_score}/4 in {category} assessment.
    Suggest suitable career paths and improvement tips in JSON like:
    {{
        "career_paths": ["..."],
        "improvement_tips": ["..."]
    }}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful career advisor."},
            {"role": "user", "content": career_prompt}
        ],
        max_tokens=200
    )
    career_data = json.loads(response['choices'][0]['message']['content'])

    return Response({
        "total_score": total_score,
        "career_suggestions": career_data
    })
