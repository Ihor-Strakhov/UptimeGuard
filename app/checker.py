import time
import requests
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import Site, CheckResult


def wait_for_db_ready():

    db = None

    while True:
        try:
            db = SessionLocal()
            print("DB + tables are ready")
            break
        except Exception as e:
            print("Waiting for DB schema...")
            time.sleep(2)
        finally:
            if db:
                db.close()

def normalize_url(url: str) -> str:
    if not url.startswith("http://") and not url.startswith("https://"):
        return f"https://{url}"
    return url


def check_site(url):
    normalized_url = normalize_url(url)
    try:
        headers = {"User-Agent": "UptimeGuard/1.0"}
        response = requests.get(normalized_url, timeout=5, allow_redirects=True, headers=headers)

        if response.status_code < 500:
            return "UP", response.status_code

        return "DOWN", response.status_code

    except requests.RequestException as exc:
        print(f"[CHECKER] request error for {normalized_url}: {exc}")
        return "DOWN", None


def site_is_due_for_check(site, db):
    last_result = (
        db.query(CheckResult)
        .filter(CheckResult.site_id == site.id)
        .order_by(CheckResult.checked_at.desc())
        .first()
    )

    if last_result is None:
        return True

    next_check_time = last_result.checked_at + timedelta(minutes=site.interval_minutes)
    return datetime.utcnow() >= next_check_time


def run_checker():
    wait_for_db_ready()

    while True:
        db = SessionLocal()
        try:
            sites = db.query(Site).all()
            print(f"[CHECKER] sites: {len(sites)}")

            for site in sites:
                if not site_is_due_for_check(site, db):
                    print(f"[CHECKER] skip {site.url}, interval not passed")
                    continue

                status, status_code = check_site(site.url)
                result = CheckResult(
                    site_id=site.id,
                    status=status,
                    status_code=status_code,
                )
                db.add(result)
                db.commit()
                db.refresh(result)
                print(
                    f"[CHECKER] {site.url} -> {status} "
                    f"({status_code if status_code is not None else 'no code'})"
                )

        except Exception as e:
            print(f"[CHECKER ERROR] {e}")
            db.rollback()

        finally:
            db.close()

        time.sleep(10)


if __name__ == "__main__":
    run_checker()