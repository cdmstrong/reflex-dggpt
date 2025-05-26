import reflex as rx
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'), override=True)

config = rx.Config(
    app_name="app",
    # api_url="http://localhost:8000",
    frontend_port=8003,
    # backend_port=8000,
    # loglevel="debug",
    # frontend_path="/home",
    cors_allowed_origins=[
        "http://localhost:8003",
        "http://43.153.7.130:8003"
    ],
    db_url=f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_SERVER')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)