gimport matplotlib.pyplot as plt
from classes.point import point_reader, Point
from classes.rhombus import Rhombus
from classes.square import Square


def plot_data(squares: list[Square],
              rhhombes: list[Rhombus],
              points: list[Point]) -> None:
    plt.style.use("style/yorha.mplstyle")

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    fig, ax = plt.subplots(1, 1)
    fig.set_figheight(7)
    fig.set_figwidth(7)

    for r in rhhombes:
        pol = r.to_plt_polygon()
        pol.set_edgecolor(colors[0])
        pol.set_facecolor('none')
        ax.add_patch(pol)

    for s in squares:
        pol = s.to_plt_polygon()
        pol.set_edgecolor(colors[1])
        pol.set_facecolor('none')
        ax.add_patch(pol)

    x_vals = [p.x for p in points]
    y_vals = [p.y for p in points]

    ax.scatter(x_vals, y_vals, s=20, marker="s", color=colors[2])

    plt.ylim(0, 21)
    plt.xlim(0, 21)
    plt.savefig("media/result.png")
