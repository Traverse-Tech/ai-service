from vertexai.generative_models import GenerativeModel
from vertexai import init
import json

logs=[
    {
      "datetime": "2024-03-22T12:00:00",
      "is_completed": True,
      "activity": {
        "title": "Minum obat penenang",
        "activity_category": {"name": "Medicine"}
      }
    },
    {
      "datetime": "2024-03-21T15:30:00",
      "is_completed": False,
      "activity": {
        "title": "Daily workout",
        "activity_category": {"name": "Kesehatan"}
      }
    }
  ]
# Initialize Vertex AI
init(project="869266946470", location="us-central1")

# Load Gemini model
model = GenerativeModel("gemini-2.0-flash-001")

# Generate a summary
response = model.generate_content(
    "Berikut ini adalah log aktivitas seorang pasien demensia selama satu minggu. Rangkum log berikut menjadi satu paragraf yang mudah dibaca:\n" + json.dumps(logs, indent=2),
    generation_config={"temperature": 0.2, "max_output_tokens": 256}
)

print(response.text.strip())