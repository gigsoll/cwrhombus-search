import matplotlib.pyplot as plt
from classes.point import point_reader
from solutions.smort import smort

squares, rhhombes = smort("dots.json", (0, 50))

fig, ax = plt.subplots(1, 1)
fig.set_figheight(8)
fig.set_figwidth(8)

for r in rhhombes:
    pol = r.to_plt_polygon()
    pol.set_edgecolor("black")
    pol.set_facecolor('none')
    ax.add_patch(pol)

for s in squares:
    pol = s.to_plt_polygon()
    pol.set_edgecolor("blue")
    pol.set_facecolor('none')
    ax.add_patch(pol)

points = point_reader("dots.json")

x_vals = [p.x for p in points]
y_vals = [p.y for p in points]

ax.scatter(x_vals, y_vals, color="red", s=20)

plt.ylim(0, 21)
plt.xlim(0, 21)
plt.show()
