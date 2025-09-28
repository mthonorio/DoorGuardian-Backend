import os
from supabase import create_client, Client

def get_supabase_client() -> Client:
    """Get Supabase client with anon key"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    
    return create_client(url, key)

def get_supabase_admin_client() -> Client:
    """Get Supabase client with service role key for admin operations"""
    url = os.environ.get("SUPABASE_URL")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not service_key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment variables")
    
    return create_client(url, service_key)