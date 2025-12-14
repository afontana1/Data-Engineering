"""Pydantic schemas for configuring and streaming Game of Life simulations."""
from typing import List, Optional, Tuple

from pydantic import BaseModel, Field, conint, confloat


class SimulationConfig(BaseModel):
    width: conint(gt=0) = Field(50, description="Board width")
    height: conint(gt=0) = Field(50, description="Board height")
    generations: Optional[conint(gt=0)] = Field(
        None, description="Number of generations to run; None for endless"
    )
    delay_ms: conint(ge=0) = Field(200, description="Delay between frames in milliseconds")
    pattern: str = Field("Random", description="Pattern name or 'Random'")
    random_fill: confloat(ge=0, le=1) = Field(
        0.2, description="Fill density for random pattern (0-1)"
    )
    wrap: bool = Field(
        False, description="Whether the board edges wrap (toroidal) or have hard borders"
    )


class GenerationState(BaseModel):
    generation: int
    width: int
    height: int
    alive: List[Tuple[int, int]]
