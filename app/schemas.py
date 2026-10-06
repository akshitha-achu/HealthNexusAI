from typing import Optional, Literal

from pydantic import BaseModel, Field


# ============================================================
# Clinical Data
# ============================================================

class ClinicalData(BaseModel):
    age: Optional[float] = Field(
        default=None,
        ge=1,
        le=120
    )

    sex: Optional[int] = Field(
        default=None,
        ge=0,
        le=1
    )

    cp: Optional[int] = Field(
        default=None,
        ge=0,
        le=3
    )

    trestbps: Optional[float] = Field(
        default=None,
        ge=50,
        le=300
    )

    chol: Optional[float] = Field(
        default=None,
        ge=50,
        le=800
    )

    fbs: Optional[int] = Field(
        default=None,
        ge=0,
        le=1
    )

    restecg: Optional[int] = Field(
        default=None,
        ge=0,
        le=2
    )

    thalach: Optional[float] = Field(
        default=None,
        ge=50,
        le=260
    )

    exang: Optional[int] = Field(
        default=None,
        ge=0,
        le=1
    )

    oldpeak: Optional[float] = Field(
        default=None,
        ge=-5,
        le=20
    )

    slope: Optional[int] = Field(
        default=None,
        ge=0,
        le=2
    )

    ca: Optional[int] = Field(
        default=None,
        ge=0,
        le=3
    )

    thal: Optional[int] = Field(
        default=None,
        ge=0,
        le=3
    )


# ============================================================
# User Health Profile
# ============================================================

class Profile(BaseModel):
    medical_history: str = ""
    family_history: str = ""
    lifestyle: str = ""
    smoking: str = ""
    alcohol: str = ""
    sleep: str = ""

    bmi: Optional[float] = Field(
        default=None,
        ge=10,
        le=80
    )

    symptoms: str = ""

    has_report: bool = False


# ============================================================
# Prediction Request
# ============================================================

class PredictionRequest(BaseModel):
    profile: Profile
    clinical: ClinicalData


# ============================================================
# Prediction Response
# ============================================================

class PredictionResponse(BaseModel):
    prediction_id: int

    risk_probability: float

    risk_label: Literal[
        "lower",
        "higher"
    ]

    model: str

    clinical_coverage: float

    message: str