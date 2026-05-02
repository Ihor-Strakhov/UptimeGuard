import os

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.database import SessionLocal
from app.db import models
from pathlib import Path
from app.cfg.logging_config import get_logger

logger = get_logger(Path(__file__).stem)


class Site(BaseModel):
    url: str
    interval_minutes: int


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.post("/site")
async def add_site_to_db(site: Site, db: Session = Depends(get_db)):
    db_site = models.Site(url=site.url, interval_minutes=site.interval_minutes)

    db.add(db_site)
    db.commit()
    db.refresh(db_site)

    logger.info(f"Site '{site.url}' created successfully!")

    return {"message": f"Site '{site.url}' created successfully!"}


@app.get("/sites")
async def get_sites(db: Session = Depends(get_db)):
    sites = db.query(models.Site).all()
    return {"sites": [site.url for site in sites]}


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "static"))
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
