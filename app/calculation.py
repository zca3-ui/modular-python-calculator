from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class Calculation:
    """Represent one calculator calculation."""

    left: float
    operation: str
    right: float
    result: float
    timestamp: str

    @classmethod
    def create(
        cls,
        left,
        operation,
        right,
        result,
    ):
        """Create a calculation with the current UTC timestamp."""
        return cls(
            left,
            operation,
            right,
            result,
            datetime.now(timezone.utc).isoformat(),
        )

