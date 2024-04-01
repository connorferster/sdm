from __future__ import annotations
from typing import Optional, Any, Union
import pathlib

from colour import Color
from matplotlib.figure import Figure
from matplotlib.patches import Polygon
import numpy as np
import parse

from papermodels.db.data_model import Annotation


def plot_annotations(
    annots: list[Annotation] | dict[Annotation, dict],
    figsize: tuple[float, float] = (17, 11),
    dpi: float = 100,
    plot_tags: bool = False,
) -> Figure:
    """
    Plots that annotations, 'annots' in matplotlib. Size and dpi can be adjusted
    to make the plot bigger/smaller. Size is in inches and dpi stands for
    "dots per inch". For a biggish plot, values of size=12, dpi=200 gives
    good results.
    """
    fig = Figure(figsize=figsize, dpi=dpi, tight_layout=True)
    ax = fig.gca()
    annotation_dict = isinstance(annots, dict)
    has_tags = False
    minx = float('inf')
    miny = float('inf')
    maxx = float("-inf")
    maxy = float("-inf")

    for idx, annot in enumerate(annots):
        if annotation_dict:
            has_tags = "tag" in annots[annot]
        if annot.object_type.lower() in (
            "polygon",
            "square",
            "rectangle",
            "rectangle sketch to scale",
        ):
            xy = xy_vertices(annot.vertices, dpi)
            ax.add_patch(
                Polygon(
                    xy=xy.T,
                    closed=True,
                    linestyle=annot.line_type,
                    linewidth=float(annot.line_weight),
                    ec=tuple(float(elem) for elem in annot.line_color),
                    fc=tuple(float(elem) for elem in annot.fill_color),
                    alpha=float(annot.fill_opacity),
                    zorder=idx,
                )
            )
        elif annot.object_type.lower() in ("line", "polyline"):
            xy = xy_vertices(annot.vertices, dpi)
            ax.plot(
                xy[0],
                xy[1],
                linestyle=annot.line_type,
                linewidth=float(annot.line_weight),
                color=tuple(float(elem) for elem in annot.line_color),
                alpha=float(annot.line_opacity),
                zorder=idx,
            )
        if annotation_dict and has_tags and plot_tags:
            tag = annots[annot]["tag"]
            geom = annots[annot]["geometry"]
            centroid = np.array(geom.centroid.coords[0])
            ax.annotate(
                tag,
                centroid * dpi / 72,
                zorder=100 * len(annots),
            )
        minx = min(np.min(xy[0]), minx)
        miny = min(np.min(xy[1]), miny)
        maxx = max(np.max(xy[0]), maxx)
        maxy = max(np.max(xy[1]), maxy)
    ax.set_aspect("equal")
    ax.set_xlim(minx * 0.95, maxx * 1.05)
    ax.set_ylim(miny * 0.95, maxy * 1.05)
    return fig


def xy_vertices(vertices: str, dpi: float, close=False) -> list[list[float]]:
    """
    Returns a list of lists of floats to emulate a 2d numpy array of x, y values
    """
    x = []
    y = []
    for idx, ordinate in enumerate(vertices):
        if idx % 2:
            y.append(float(ordinate))
        else:
            x.append(float(ordinate))
    scaled_vertices = np.asarray([x, y]) * dpi / 72
    return scaled_vertices
