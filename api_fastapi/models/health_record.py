from dataclasses import dataclass


@dataclass
class HealthRecord:
    id: int
    patient_name: str
    description: str
