from enum import Enum

class Diagnosis(Enum):
    HEART_ATTACK = auto() # each key is auto-assigned a value 1, 2, 3, etc
    ANAPHYLAXIS = auto()
    HYPOGLYCEMIA = auto()
    HYPERGLYCEMIA = auto()
    # etc