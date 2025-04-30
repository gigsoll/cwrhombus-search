import matplotlib.pyplot as plt
from classes.point import point_reader
from solutions.smort import smort

plt.style.use("style/yorha.mplstyle")

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

squares, rhhombes = smort("dots.json", (0, 50))

fig, ax = plt.subplots(1, 1)
fig.set_figheight(8)
fig.set_figwidth(8)

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

points = point_reader("dots.json")

x_vals = [p.x for p in points]
y_vals = [p.y for p in points]

ax.scatter(x_vals, y_vals, s=20, marker="s", color=colors[2])

plt.ylim(0, 21)
plt.xlim(0, 21)
plt.show()
