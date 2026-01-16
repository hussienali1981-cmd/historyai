import os
import uuid
from redis import Redis
from rq import Queue
from .config import REDIS_URL, OUTPUT_DIR
from .ai_clients import generate_script_openai, plan_scenes_from_script, generate_image, generate_voice, generate_cinematic_video
from .db import SessionLocal
from .models import Job
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

redis_conn = Redis.from_url(REDIS_URL)
q = Queue("default", connection=redis_conn)

def render_video_from_assets(images, audio_path, output_path):
    clips = []
    for path, dur in images:
        clip = ImageClip(path).set_duration(dur)
        clips.append(clip)
    video = concatenate_videoclips(clips, method="compose")
    if os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        final = video.set_audio(audio)
    else:
        final = video
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    return output_path

def job_worker(job_id):
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    try:
        job.status = "running"
        db.commit()

        script = generate_script_openai(job.topic, job.duration_minutes, job.language)
        scenes = plan_scenes_from_script(script)

        images_with_duration = []
        for s in scenes:
            desc = s.get("description", "")[:300]
            if s.get("type") == "image":
                img = generate_image(f"{desc} Ultra cinematic historical documentary, 16:9")
                images_with_duration.append((img, max(5, s.get("duration", 60)/len(scenes))))
            else:
                vid = generate_cinematic_video(f"{desc} cinematic", duration=6)
                images_with_duration.append((vid, max(5, s.get("duration", 60)/len(scenes))))

        audio_path = generate_voice(script)
        out_file = f"{OUTPUT_DIR}/final/{uuid.uuid4().hex}.mp4"
        render_video_from_assets(images_with_duration, audio_path, out_file)

        job.status = "done"
        job.result_path = out_file
        db.commit()
    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        db.commit()
        raise
    finally:
        db.close()

def enqueue_job(job_id):
    q.enqueue(job_worker, job_id)
