import typing as t

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from infer import get_loan_prediction
from config import MODEL_NAME, SCRIPT_NAME

# ----- Models -----


class LoanRequest(BaseModel):
    dob_ssn: str
    zipcode: str
    age: int
    income: int
    emp_length: int
    loan_amount: int
    int_rate: float


class LoanDecision(BaseModel):
    loan_decision: str
    probabilities: t.List[float]


# ----- Routes -----

router = r = APIRouter()


@r.post(
    "/predict",
    response_model=LoanDecision,
    name="loan:predict",
    operation_id="predict_loan",
)
async def get_loan_pred(lr: LoanRequest):

    try:
        score, probabilities = await get_loan_prediction(
            lr.dob_ssn,
            lr.zipcode,
            lr.age,
            lr.income,
            lr.emp_length,
            lr.loan_amount,
            lr.int_rate,
            SCRIPT_NAME,
            MODEL_NAME,
        )
        loan_decision = "Approved" if score[0] == 1 else "Denied"
        probabilities = list(probabilities[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"loan_decision": loan_decision, "probabilities": probabilities}
