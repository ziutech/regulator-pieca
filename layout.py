from typing import Callable, List, Union
import dash as d


__fields: List = []


def range(
    id: str, label: str, min: float = 0, max: float = 50, step: float = 1
) -> d.html.Div:
    __fields.append(id)
    return d.html.Div(
        [
            d.html.Label(label),
            d.dcc.RangeSlider(
                id=id,
                min=min,
                max=max,
                step=step,
                value=[min, max],
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
            ),
        ]
    )


def num_input(
    id: str,
    label: str,
    min: float = 0,
    max: float = 50,
    step: float = 1,
    default: Union[float, Callable[[float, float], float]] = lambda min, max: (
        min + max
    )
    / 2,
) -> d.html.Div:
    __fields.append(id)
    return d.html.Div(
        [
            d.html.Label(label),
            d.dcc.Slider(
                id=id,
                min=min,
                max=max,
                step=step,
                value=default(min, max) if isinstance(default, Callable) else default,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
            ),
        ]
    )


def fields():
    return __fields.copy()
