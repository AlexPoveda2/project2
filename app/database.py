import os
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv

load_dotenv()

def init_db(app):
    register_tortoise(
        app,
        db_url="postgres://postgres:postgres@db:5432/mydatabase",
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
