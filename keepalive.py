from supabase import create_client, Client
from flask.cli import load_dotenv
import os
from datetime import datetime, timezone, timedelta

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

time_tanzania = datetime.now(timezone(timedelta(hours=3)))
print(time_tanzania)

try:
    supabase.table("keepalive_log").insert({"pinged_at": time_tanzania.isoformat()}).execute()
    print("Pinged Successful")
except Exception as e:
    print("Ping Failed", e)

cutoff = datetime.now(timezone(timedelta(hours=3))) - timedelta(days=90)

try:
    supabase.table("keepalive_log").delete().lt("pinged_at", cutoff.isoformat()).execute()
    print("Old entries deleted")
except Exception as e:
    print("Deletion Error", e)

