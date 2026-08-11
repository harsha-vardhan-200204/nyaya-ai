import os
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal, Base
from app.models.auth import User
from app.models.legal import LegalAct, LegalSection, Judgment
from app.utils.security import get_password_hash
from app.routers import auth, cases, legal, chat, admin
from app.services.classifier import classifier

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NyayaAI API",
    description="Backend API for AI-Powered Legal Case Analysis & Outcome Prediction System",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development ease
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(cases.router)
app.include_router(legal.router)
app.include_router(chat.router)
app.include_router(admin.router)

# Dynamic Seeding Routine
def seed_database():
    db: Session = SessionLocal()
    try:
        # 1. Seed Users
        if db.query(User).count() == 0:
            print("Seeding default users...")
            default_users = [
                User(username="admin", email="admin@nyaya.ai", password_hash=get_password_hash("admin123"), role="Admin"),
                User(username="lawyer", email="lawyer@nyaya.ai", password_hash=get_password_hash("lawyer123"), role="Lawyer"),
                User(username="client", email="client@nyaya.ai", password_hash=get_password_hash("client123"), role="Client")
            ]
            db.add_all(default_users)
            db.commit()
            print("Default users seeded: admin/admin123, lawyer/lawyer123, client/client123")

        # 2. Seed Legal Sections
        if db.query(LegalSection).count() == 0:
            csv_path = "H:/intern/project/nyaya-ai/data/demo/legal_sections.csv"
            if os.path.exists(csv_path):
                print("Seeding legal sections from CSV...")
                df = pd.read_csv(csv_path)
                
                # Group by Act to create LegalAct first (deduplicated by name only)
                acts = df[["act_name", "year"]].drop_duplicates(subset=["act_name"])
                act_map = {}
                
                for _, row in acts.iterrows():
                    act = LegalAct(
                        name=row["act_name"],
                        year=int(row["year"]),
                        source_url=None
                    )
                    db.add(act)
                    db.commit()
                    db.refresh(act)
                    act_map[row["act_name"]] = act.id
                
                # Add sections
                for _, row in df.iterrows():
                    sec = LegalSection(
                        act_id=act_map[row["act_name"]],
                        section_number=str(row["section"]),
                        title=row["title"],
                        description=row["description"],
                        keywords=row["keywords"],
                        domain=row["domain"],
                        active_status=row["active_status"]
                    )
                    db.add(sec)
                db.commit()
                print(f"Successfully seeded {len(df)} legal sections.")
            else:
                print(f"Sections CSV not found at {csv_path}. Skipping section seeding.")

        # 3. Seed Judgments
        if db.query(Judgment).count() == 0:
            csv_path = "H:/intern/project/nyaya-ai/data/demo/legal_cases.csv"
            if os.path.exists(csv_path):
                print("Seeding historical judgments from CSV...")
                df = pd.read_csv(csv_path)
                
                for _, row in df.iterrows():
                    jdg = Judgment(
                        case_name=row["case_name"],
                        court=row["court"],
                        state=row["state"],
                        judgment_date=row["judgment_date"],
                        case_type=row["case_type"],
                        acts=row["acts"],
                        sections=row["sections"],
                        keywords=row["keywords"],
                        facts=row["facts"],
                        legal_issue=row["legal_issue"],
                        arguments=row["arguments"],
                        evidence=row["evidence"],
                        judgment_summary=row["judgment_summary"],
                        outcome=row["outcome"],
                        precedent=row["precedent"],
                        source_url=row["source_url"],
                        verified=row["verified"] == "True" or row["verified"] is True
                    )
                    db.add(jdg)
                db.commit()
                print(f"Successfully seeded {len(df)} historical judgments.")
                
                # Trigger classifier retraining now that judgments are in the DB
                classifier.train()
            else:
                print(f"Cases CSV not found at {csv_path}. Skipping judgment seeding.")
    except Exception as e:
        print(f"Seeding failed: {str(e)}")
        db.rollback()
    finally:
        db.close()

# Run seed
seed_database()

# Mount frontend static files if compiled in production
from fastapi.staticfiles import StaticFiles
frontend_dist_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend", "dist")
if os.path.exists(frontend_dist_path):
    print(f"Mounting production frontend from: {frontend_dist_path}")
    app.mount("/", StaticFiles(directory=frontend_dist_path, html=True), name="static")
else:
    @app.get("/")
    def read_root():
        return {
            "status": "online",
            "system": "NyayaAI API System",
            "description": "Indian Legal Case Analysis and Outcome Prediction Assistant",
            "docs_url": "/docs"
        }
