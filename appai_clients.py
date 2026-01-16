import os
import uuid
from .config import OUTPUT_DIR

def generate_script_openai(topic, duration, language="ar"):
    # TODO: استبدل هذا باستدعاء OpenAI الفعلي
    script = f"Hook: كيف سقطت {topic}؟\n\nالمقدمة...\n\n(نص تجريبي — استبدل بالـ OpenAI call)."
    return script

def plan_scenes_from_script(script_text):
    paragraphs = [p for p in script_text.split("\n\n") if p.strip()]
    scenes = []
    for i, p in enumerate(paragraphs):
        scenes.append({
            "scene": i+1,
            "duration": 60,
            "type": "image" if i % 2 == 0 else "cinematic",
            "description": p[:250]
        })
    return scenes

def generate_image(prompt, out_filename=None):
    out_filename = out_filename or f"{OUTPUT_DIR}/images/{uuid.uuid4().hex}.jpg"
    os.makedirs(os.path.dirname(out_filename), exist_ok=True)
    # TODO: call Stable Diffusion / DALL·E and write image bytes
    open(out_filename, "wb").close()
    return out_filename

def generate_voice(text, out_filename=None):
    out_filename = out_filename or f"{OUTPUT_DIR}/audio/{uuid.uuid4().hex}.mp3"
    os.makedirs(os.path.dirname(out_filename), exist_ok=True)
    # TODO: call ElevenLabs and save mp3
    open(out_filename, "wb").close()
    return out_filename

def generate_cinematic_video(prompt, out_filename=None, duration=6):
    out_filename = out_filename or f"{OUTPUT_DIR}/videos/{uuid.uuid4().hex}.mp4"
    os.makedirs(os.path.dirname(out_filename), exist_ok=True)
    # TODO: call Runway/Pika and save mp4
    open(out_filename, "wb").close()
    return out_filename
