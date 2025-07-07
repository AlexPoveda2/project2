# app/db.py
from tortoise.contrib.fastapi import register_tortoise

def init_db(app):
    register_tortoise(
        app,
        db_url = "postgres://alex:alex@db:5432/mydatabase",
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
