from fastapi import FastAPI
import redis
import uuid
import os

app = FastAPI()

def get_redis():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs")
def create_job():
    r = get_redis()

    job_id = str(uuid.uuid4())

    r.lpush("jobs", job_id)
    r.hset(f"job:{job_id}", "status", "queued")

    return {"job_id": job_id, "status": "queued"}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    r = get_redis()

    status = r.hget(f"job:{job_id}", "status")

    if status is None:
        return {"error": "not found"}

    return {"job_id": job_id, "status": status}






# from fastapi import FastAPI
# import redis
# import uuid
# import os

# app = FastAPI()

# redis_host = os.getenv("REDIS_HOST", "localhost")
# r = redis.Redis(host=redis_host, port=6379, decode_responses=True)


# @app.get("/")
# def root():
#     return {"message": "API is running"}


# @app.get("/health")
# def health():
#     return {"status": "ok"}


# @app.post("/jobs")
# def create_job():
#     job_id = str(uuid.uuid4())

# # FIX: consistent queue name
#     r.lpush("jobs", job_id)
#     r.hset(f"job:{job_id}", "status", "queued")
#     return {"job_id": job_id, "status": "queued"}


# @app.get("/jobs/{job_id}")
# def get_job(job_id: str):
#     status = r.hget(f"job:{job_id}", "status")
#     # FIX: proper None check
#     if status is None:
#         return {"error": "not found"}

#     return {"job_id": job_id, "status": status}
