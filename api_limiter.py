import time
import redis
from flask import request, jsonify
from functools import wraps
from config import Config
from models import Users
from redis_client import redis_client


SUSPICIOUS_IPS = set()

def get_user_plan(api_key):
    user = Users.query.filter_by(api_key=api_key).first()
    if user:
        return user.plan
    return None

def get_rate_limit(plan):
    limits = {
        "Free": (100, 24 * 60 * 60),
        "Basic": (1000, 24 * 60 * 60),
        "Pro": (float('inf'), 0)
    }
    return limits.get(plan, (0, 0))

def is_suspicious(ip_address):
    spam_key = f'spam:{ip_address}'
    spam_count = redis_client.incr(spam_key)

    if spam_count == 1:
        redis_client.expire(spam_key, 10)  

    return spam_count > 5 

def rate_limit_and_security(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip_address = request.remote_addr
        
        if redis_client.sismember('suspicious_ips', ip_address):
            return jsonify({"error": "Your IP has been flagged as suspicious."}), 429

        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return jsonify({"error": "API Key is missing."}), 401

        user_plan = get_user_plan(api_key)
        if not user_plan:
            return jsonify({"error": "Invalid API Key."}), 401

        limit, window = get_rate_limit(user_plan)
        
        if limit == float('inf'):
            return f(*args, **kwargs)

        key = f'rate_limit:{api_key}:{ip_address}'
        count = redis_client.incr(key)
        
        if count == 1:
            redis_client.expire(key, window)
        
        if count > limit:
            return jsonify({"error": "Rate limit exceeded."}), 429
        
        if is_suspicious(ip_address):
            redis_client.sadd('suspicious_ips', ip_address)
            return jsonify({"error": "Suspicious activity detected. Your IP has been blocked."}), 429
        
        return f(*args, **kwargs)
    return decorated_function