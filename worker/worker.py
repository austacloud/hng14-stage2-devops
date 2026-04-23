import redis
import time

# FIX: safe Redis connection + auto decode
r = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)
print("Worker started... waiting for jobs")

def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)  # simulate work
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")
   

while True:
    job = r.brpop("jobs", timeout=5)
    if job:
        _, job_id = job
        process_job(job_id)
    else:
        print("No jobs in queue...")   