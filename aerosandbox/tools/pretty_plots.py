"""
A set of tools used for making prettier Matplotlib plots.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from typing import Union, Dict, List, Callable
from matplotlib import ticker
import aerosandbox.numpy as np
from aerosandbox.tools.string_formatting import eng_string

# plt.ion()

### Define color palettes
palettes = {
    "categorical": [
        "#4285F4",  # From Google logo, blue
        "#EA4335",  # From Google logo, red
        "#34A853",  # From Google logo, green
        "#ECB22E",  # From Slack logo, gold
        "#9467BD",  # Rest are from Matplotlib "tab10"
        "#8C564B",
        "#E377C2",
        "#7F7F7F",
    ],
}

sns.set_theme(
    palette=palettes["categorical"],
)

mpl.rcParams["figure.dpi"] = 200
mpl.rcParams["axes.formatter.useoffset"] = False
mpl.rcParams["contour.negative_linestyle"] = 'solid'


def set_ticks(
        x_major: Union[float, int] = None,
        x_minor: Union[float, int] = None,
        y_major: Union[float, int] = None,
        y_minor: Union[float, int] = None
):
    ax = plt.gca()
    if x_major is not None:
        ax.xaxis.set_major_locator(ticker.MultipleLocator(base=x_major))
    if x_minor is not None:
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(base=x_minor))
    if y_major is not None:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(base=y_major))
    if y_minor is not None:
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(base=y_minor))


def equal():
    plt.gca().set_aspect("equal", adjustable='box')


def adjust_lightness(color, amount=1.0):
    """
    Converts a color to HLS space, then mulitplies the lightness by `amount`, then converts back to RGB.

    Args:
        color: A color, in any format that matplotlib understands.
        amount: The amount to multiply the lightness by. Valid range is 0 to infinity.

    Returns: A color, as an RGB tuple.

    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])


def show_plot(
        title: str = None,
        xlabel: str = None,
        ylabel: str = None,
        tight_layout: bool = True,
        legend: bool = None,
        legend_frame: bool = True,
        show: bool = True,
        pretty_grids: bool = True,
):
    """
    Finalize and show a plot.
    Args:
        title:
        xlabel:
        ylabel:
        tight_layout:
        legend:
        show:
        pretty_grids:

    Returns:

    """
    fig = plt.gcf()
    axes = fig.get_axes()

    if pretty_grids:
        for ax in axes:
            if not ax.get_label() == '<colorbar>':
                ax.grid(True, 'major', axis='both', linewidth=1.6)
                ax.grid(True, 'minor', axis='both', linewidth=0.7)

    ### Determine if a legend should be shown
    if legend is None:
        lines = plt.gca().lines
        if len(lines) <= 1:
            legend = False
        else:
            legend = False
            for line in lines:
                if line.get_label()[0] != "_":
                    legend = True
                    break

    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if title is not None:
        if len(axes) <= 1:
            plt.title(title)
        else:
            plt.suptitle(title)
    if tight_layout:
        plt.tight_layout()
    if legend:
        plt.legend(frameon=legend_frame)
    if show:
        plt.show()


def contour(
        X: np.ndarray,
        Y: np.ndarray,
        Z: np.ndarray,
        levels: Union[int, List, np.ndarray] = 31,
        colorbar: bool = True,
        linelabels: bool = True,
        cmap=mpl.cm.get_cmap('viridis'),
        alpha: float = 0.7,
        extend: str = "both",
        linecolor="k",
        linewidths: float = 0.5,
        extendrect: bool = True,
        linelabels_format: Union[str, Callable[[float], str]] = eng_string,
        linelabels_fontsize: float = 8,
        colorbar_label: str = None,
        z_log_scale: bool = False,
        contour_kwargs: Dict = None,
        contourf_kwargs: Dict = None,
        colorbar_kwargs: Dict = None,
        linelabels_kwargs: Dict = None,
        **kwargs,
):
    """
    An analogue for plt.contour and plt.tricontour and friends that produces a much prettier default graph.

    Can take inputs with either contour or tricontour syntax.

    See syntax here:
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contour.html
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contourf.html
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.tricontour.html
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.tricontourf.html

    Args:
        X: See contour docs.
        Y: See contour docs.
        Z: See contour docs.
        levels: See contour docs.
        colorbar: Should we draw a colorbar?
        linelabels: Should we add line labels?
        cmap: What colormap should we use?
        alpha: What transparency should all plot elements be?
        extend: See contour docs.
        linecolor: What color should the line labels be?
        linewidths: See contour docs.
        extendrect: See colorbar docs.
        linelabels_format: See ax.clabel docs.
        linelabels_fontsize: See ax.clabel docs.
        contour_kwargs: Additional keyword arguments for contour.
        contourf_kwargs: Additional keyword arguments for contourf.
        colorbar_kwargs: Additional keyword arguments for colorbar.
        linelabels_kwargs: Additional keyword arguments for the line labels (ax.clabel).
        **kwargs: Additional keywords, which are passed to both contour and contourf.

    Returns: A tuple of (contour, contourf, colorbar) objects.

    """

    if contour_kwargs is None:
        contour_kwargs = {}
    if contourf_kwargs is None:
        contourf_kwargs = {}
    if colorbar_kwargs is None:
        colorbar_kwargs = {}
    if linelabels_kwargs is None:
        linelabels_kwargs = {}

    args = [
        X,
        Y,
        Z,
    ]

    shared_kwargs = kwargs
    if levels is not None:
        shared_kwargs["levels"] = levels
    if alpha is not None:
        shared_kwargs["alpha"] = alpha
    if extend is not None:
        shared_kwargs["extend"] = extend
    if z_log_scale:

        shared_kwargs = {
            "norm": mpl.colors.LogNorm(),
            "locator": mpl.ticker.LogLocator(
                subs = np.geomspace(1, 10, 4+1)[:-1]
            ),
            **shared_kwargs
        }

    if colorbar_label is not None:
        colorbar_kwargs["label"] = colorbar_label

    contour_kwargs = {
        "colors"    : linecolor,
        "linewidths": linewidths,
        **shared_kwargs,
        **contour_kwargs
    }
    contourf_kwargs = {
        "cmap": cmap,
        **shared_kwargs,
        **contourf_kwargs
    }

    colorbar_kwargs = {
        "extendrect": extendrect,
        **colorbar_kwargs
    }

    linelabels_kwargs = {
        "inline"  : 1,
        "fontsize": linelabels_fontsize,
        "fmt"     : linelabels_format,
        **linelabels_kwargs
    }

    try:
        cont = plt.contour(*args, **contour_kwargs)
        contf = plt.contourf(*args, **contourf_kwargs)
    except TypeError as e:
        try:
            cont = plt.tricontour(*args, **contour_kwargs)
            contf = plt.tricontourf(*args, **contourf_kwargs)
        except TypeError:
            raise e

    if colorbar:
        cbar = plt.colorbar(**colorbar_kwargs)

        if z_log_scale:
            cbar.ax.yaxis.set_major_locator(mpl.ticker.LogLocator())
            cbar.ax.yaxis.set_major_formatter(mpl.ticker.LogFormatter())
    else:
        cbar = None

    if linelabels:
        plt.gca().clabel(cont, **linelabels_kwargs)

    return cont, contf, cbar
