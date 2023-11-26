from pydantic import BaseModel

from enum import StrEnum


class MachineType(StrEnum):
    TRUEBEAM = "TrueBeam"
    VITALBEAM = "VitalBeam"
    UNIQUE = "Unique"


class CancerType(BaseModel):
    region: str
    machine_options: list[MachineType]
    fraction_options: list[int]
    avg_duration: int # minutes
    probability: float # 0 to 1

    def __hash__(self):
        return hash(self.region)


CRANIOSPINAL = CancerType(
    region="craniospinal",
    machine_options=[MachineType.TRUEBEAM, MachineType.TRUEBEAM],
    fraction_options=[13, 17, 20, 30],
    avg_duration=30,
    probability=0.01,
)

BREAST = CancerType(
    region="breast",
    machine_options=[MachineType.TRUEBEAM, MachineType.VITALBEAM, MachineType.UNIQUE],
    fraction_options=[15, 19, 25, 30],
    avg_duration=12,
    probability=0.25,
)

BREAST_SPECIAL = CancerType(
    region="breast special",
    machine_options=[MachineType.TRUEBEAM],
    fraction_options=[15, 19, 25, 30],
    avg_duration=20,
    probability=0.05,
)

HEAD_AND_NECK = CancerType(
    region="head & neck",
    machine_options=[MachineType.TRUEBEAM, MachineType.VITALBEAM],
    fraction_options=[5, 10, 15, 25, 30, 33, 35],
    avg_duration=12,
    probability=0.1,
)

ABDOMEN = CancerType(
    region="abdomen",
    machine_options=[MachineType.TRUEBEAM, MachineType.VITALBEAM],
    fraction_options=[1, 3, 5, 8, 10, 12, 15, 18, 20, 30],
    avg_duration=12,
    probability=0.1,
)

PELVIS = CancerType(
    region="pelvis",
    machine_options=[MachineType.TRUEBEAM, MachineType.VITALBEAM],
    fraction_options=[1, 3, 5, 10, 15, 22, 23, 28, 35],
    avg_duration=12,
    probability=0.18,
)

CRANE = CancerType(
    region="crane",
    machine_options=[MachineType.TRUEBEAM, MachineType.VITALBEAM],
    fraction_options=[1, 5, 10, 13, 25, 30],
    avg_duration=10,
    probability=0.04,
)

LUNG = CancerType(
    region="lung",
    machine_options=[MachineType.TRUEBEAM, MachineType.VITALBEAM],
    fraction_options=[1, 5, 10, 15, 20, 25, 30, 33],
    avg_duration=12,
    probability=0.12,
)

LUNG_SPECIAL = CancerType(
    region="lung special",
    machine_options=[MachineType.TRUEBEAM, MachineType.VITALBEAM],
    fraction_options=[3, 5, 8],
    avg_duration=15,
    probability=0.05,
)

WHOLE_BRAIN = CancerType(
    region="whole brain",
    machine_options=[MachineType.VITALBEAM, MachineType.UNIQUE],
    fraction_options=[5, 10, 12],
    avg_duration=10,
    probability=0.1,
)

cancer_types = [
    CRANIOSPINAL,
    BREAST,
    BREAST_SPECIAL,
    HEAD_AND_NECK,
    ABDOMEN,
    PELVIS,
    CRANE,
    LUNG,
    LUNG_SPECIAL,
    WHOLE_BRAIN,
]

cancer_type_map = {c.region: c for c in cancer_types}

def get_cancer_type(region: str) -> CancerType:
    return cancer_type_map[region.lower()]
