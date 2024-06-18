import os
from enum import Enum


class EnvVariables(Enum):
    DEBUG = os.getenv("DEBUG", default="1")
    ENVIRONMENT = os.getenv("ENVIRONMENT", default="development")
    DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", default="unsafe-secret-key")
    DATABASE_NAME = os.getenv("DATABASE_NAME", default="postgres")
    DATABASE_USER = os.getenv("DATABASE_USER", default="postgres")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", default="postgres")
    DATABASE_HOST = os.getenv("DATABASE_HOST", default="localhost")
    DATABASE_PORT = os.getenv("DATABASE_PORT", default="5432")
    SUPABASE_DB_NAME= os.getenv("SUPABASE_DB_NAME", default="postgres")
    SUPABASE_DB_USER= os.getenv("SUPABASE_DB_USER", default="postgres.mufexywealhbqphmpmgq")
    SUPABASE_DB_PASSWORD= os.getenv("SUPABASE_DB_PASSWORD", default="postgres")
    SUPABASE_DB_HOST= os.getenv("SUPABASE_DB_HOST", default="aws-0-ap-south-1.pooler.supabase.com")
    SUPABASE_DB_PORT= os.getenv("SUPABASE_DB_PORT", default="6543")