from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, require_admin_jwt
from app.domain.user import User as UserEntity, Role
from app.repositories.location_repo import LocationRepository
from app.schemas.location import LocationIn, LocationOut, LastLocation
from app.ws.manager import manager
from app.core.security import decode_access_token

router = APIRouter(prefix="/tracking", tags=["tracking"])

# ---- REST Fallback (opsiyonel): mobil konum POST
@router.post("/point", response_model=LocationOut)
def post_point(payload: LocationIn, db: Session = Depends(get_db), me: UserEntity = Depends(get_current_user)):
    repo = LocationRepository(db)
    p = repo.save_point(me.id, payload.lat, payload.lon)
    return {"user_id": me.id, "lat": p.lat, "lon": p.lon, "created_at": p.created_at}

# ---- REST: kendi günün noktaları (user)
@router.get("/my/day", response_model=list[LocationOut])
def my_day(day: date = Query(...), db: Session = Depends(get_db), me: UserEntity = Depends(get_current_user)):
    repo = LocationRepository(db)
    pts = repo.list_points_for_day(me.id, day)
    return [{"user_id": me.id, "lat": p.lat, "lon": p.lon, "created_at": p.created_at} for p in pts]

# ---- REST: admin için snapshot (tüm user'ların son konumu)
@router.get("/admin/last", response_model=list[LastLocation])
def admin_last(db: Session = Depends(get_db), _admin: UserEntity = Depends(require_admin_jwt)):
    repo = LocationRepository(db)
    rows = repo.last_points_for_all_users()
    out = []
    for u, p in rows:
        out.append({"user_id": u.id, "first_name": u.first_name, "last_name": u.last_name,
                    "lat": p.lat, "lon": p.lon, "created_at": p.created_at})
    return out

# ---- WS auth yardımcı
async def _auth_ws_token(raw_token: str) -> dict:
    # raw_token = "...jwt..."
    payload = decode_access_token(raw_token)
    return payload

# ---- WS: kullanıcı konum gönderir
@router.websocket("/ws/track")
async def ws_track(websocket: WebSocket, token: str):
    # token query-param ile gelir: ws://..../ws/track?token=<JWT>
    payload = await _auth_ws_token(token)
    user_id = int(payload.get("sub", "0"))
    role = payload.get("role")
    if role not in ("user", "admin"):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION); return

    await manager.connect_user(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()  # {"type":"loc","lat":..,"lon":..}
            if data.get("type") != "loc":
                continue
            lat = float(data["lat"]); lon = float(data["lon"])
            # DB'ye yaz
            from app.db.session import SessionLocal
            db: Session = SessionLocal()
            try:
                repo = LocationRepository(db)
                p = repo.save_point(user_id, lat, lon, datetime.utcnow())
            finally:
                db.close()
            # adminlere yayınla
            await manager.broadcast_to_admins({
                "event": "loc",
                "user_id": user_id,
                "lat": lat, "lon": lon,
                "created_at": p.created_at.isoformat()
            })
            # isteğe bağlı ack
            await websocket.send_json({"ok": True})
    except Exception:
        pass
    finally:
        manager.disconnect_user(user_id, websocket)



# ---- WS: admin canlı dinler
@router.websocket("/ws/admin")
async def ws_admin(websocket: WebSocket, token: str):
    payload = await _auth_ws_token(token)
    role = payload.get("role")
    if role != "admin":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION); return

    await manager.connect_admin(websocket)

    # bağlanınca snapshot gönder
    from app.db.session import SessionLocal
    db: Session = SessionLocal()
    try:
        repo = LocationRepository(db)
        rows = repo.last_points_for_all_users()
        await websocket.send_json({
            "event": "snapshot",
            "items": [
                {"user_id": u.id, "first_name": u.first_name, "last_name": u.last_name,
                 "lat": p.lat, "lon": p.lon, "created_at": p.created_at.isoformat()}
                for u, p in rows
            ]
        })
    finally:
        db.close()

    try:
        # admin WS'den gelen mesajları şimdilik yok say
        while True:
            await websocket.receive_text()
    except Exception:
        pass
    finally:
        manager.disconnect_admin(websocket)
