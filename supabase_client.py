"""
supabase_client.py - Supabase client initialization
"""

from supabase import create_client, Client

SUPABASE_URL = "https://yrcyrvqrbtxlzifvzzlc.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlyY3lydnFyYnR4bHppZnZ6emxjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk5NDY4NjksImV4cCI6MjA3NTUyMjg2OX0.ywZgmn_6LDMwWr8i-rx0nfmfYD0aqurPYeCqDlxXZ-Y"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)