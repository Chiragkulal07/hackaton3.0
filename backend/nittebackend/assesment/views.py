# 🔹 Django / DRF imports
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

# 🔹 Local imports
from models import Question
from serializer import QuestionSerializer

# 🔹 External libraries
import openai
import os
import json
load_dotenv() 

# 🔹 Set OpenAI API key from settings.py
openai.api_key = os.getenv("OPENAI_API_KEY")


@api_view(['GET'])
def get_assessment_questions(request):
    category = request.GET.get('category', 'general')

    # Prompt to generate 1 multiple choice question with 4 options
    prompt = f"""
    Generate 1 multiple choice question on '{category}'.
    Provide question text and 4 options labeled A, B, C, D in JSON format like:
    {{
        "question_text": "...",
        "option_a": "...",
        "option_b": "...",
        "option_c": "...",
        "option_d": "..."
    }}
    """

    try:
        # Call OpenAI to generate the question
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful question generator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )

        ai_output = response['choices'][0]['message']['content']
        question_data = json.loads(ai_output)  # Convert AI string to dict

        # 🔹 Create Question instance (not necessarily saving to DB)
        question_instance = Question(
            question_text=question_data['question_text'],
            option_a=question_data['option_a'],
            option_b=question_data['option_b'],
            option_c=question_data['option_c'],
            option_d=question_data['option_d']
        )

        # 🔹 Serialize the Question instance
        serializer = QuestionSerializer(question_instance)

        return Response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
