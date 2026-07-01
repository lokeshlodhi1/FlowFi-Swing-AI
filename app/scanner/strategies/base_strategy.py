from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class StrategyResult:

    valid: bool

    setup: str

    confidence: int

    entry: float

    stop_loss: float

    target1: float

    target2: float

    risk_reward: float

    reason: str


class BaseStrategy(ABC):

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    @abstractmethod
    def scan(self):

        pass