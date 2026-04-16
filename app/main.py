from pathlib import Path

from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import Base, engine, get_session
from app.models import Delivery
from app.schemas import DeliveryCreate, DeliveryOut

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="Delivery App")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_session)) -> HTMLResponse:
    deliveries = db.execute(select(Delivery).order_by(Delivery.created_at.desc())).scalars().all()
    return templates.TemplateResponse(
        "index.html", {"request": request, "deliveries": deliveries}
    )


@app.get("/deliveries", response_model=list[DeliveryOut])
def list_deliveries(db: Session = Depends(get_session)) -> list[Delivery]:
    return db.execute(select(Delivery).order_by(Delivery.created_at.desc())).scalars().all()


@app.post("/deliveries", response_model=DeliveryOut, status_code=status.HTTP_201_CREATED)
def add_delivery(payload: DeliveryCreate, db: Session = Depends(get_session)) -> Delivery:
    delivery = Delivery(**payload.model_dump())
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    return delivery


@app.delete("/deliveries/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_delivery(delivery_id: int, db: Session = Depends(get_session)) -> None:
    delivery = db.get(Delivery, delivery_id)
    if delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    db.delete(delivery)
    db.commit()


@app.post("/ui/deliveries")
def ui_add_delivery(
    recipient: str = Form(...),
    address: str = Form(...),
    item: str = Form(...),
    status_: str = Form("pending", alias="status"),
    db: Session = Depends(get_session),
) -> RedirectResponse:
    db.add(Delivery(recipient=recipient, address=address, item=item, status=status_))
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/ui/deliveries/{delivery_id}/delete")
def ui_remove_delivery(delivery_id: int, db: Session = Depends(get_session)) -> RedirectResponse:
    delivery = db.get(Delivery, delivery_id)
    if delivery is not None:
        db.delete(delivery)
        db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
