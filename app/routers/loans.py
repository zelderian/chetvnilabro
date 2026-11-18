from fastapi import APIRouter, Depends, Header, Response, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import current_member_id
from app.schemas import LoanCreate, LoanOut
from app.services import loans as svc

router = APIRouter(prefix="/api/v1", tags=["loans"])


@router.post("/loans", response_model=LoanOut, status_code=status.HTTP_201_CREATED)
def borrow(
    data: LoanCreate,
    response: Response,
    idempotency_key: str | None = Header(default=None, max_length=64),
    member_id: int = Depends(current_member_id),
    db: Session = Depends(get_db),
):
    loan, replayed = svc.borrow_book(db, member_id, data.book_id, data.days, idempotency_key)
    if replayed:
        response.headers["Idempotent-Replayed"] = "true"
    return svc.to_out(loan)


@router.post("/loans/{loan_id}/return", response_model=LoanOut)
def return_loan(
    loan_id: int,
    member_id: int = Depends(current_member_id),
    db: Session = Depends(get_db),
):
    return svc.to_out(svc.return_book(db, member_id, loan_id))


@router.get("/me/loans", response_model=list[LoanOut])
def my_loans(
    active: bool = False,
    member_id: int = Depends(current_member_id),
    db: Session = Depends(get_db),
):
    return [svc.to_out(l) for l in svc.list_member_loans(db, member_id, active)]
