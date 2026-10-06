import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Item import Star, System
import pandas as pd
FPS = 120

TRAIL_LEN = 900      # 每个点保留最近多少帧的轨迹
MIU = 1              # 指定快放倍率，智能是大于0的实数
MIU_0 = 1e6          # 额外的快放倍率，改变实际物理参数，容易导致模拟失真，计算误差在1e3(m)数量级左右，建议不要随意修改
BOUND = 5.0e12
# ============ 指定天体的初始状态 ============
"""pos 位置, radius 半径, vel 速度, mass 质量（可以不指定，会根据半径和密度计算）"""
df = pd.read_csv('solar_system_data.csv')
df['位置'] = df['位置'].apply(lambda x: np.fromstring(x.strip('[]'), sep=' ') if pd.notna(x) else None)
df['速度'] = df['速度'].apply(lambda x: np.fromstring(x.strip('[]'), sep=' ') if pd.notna(x) else None)
stars = []
for _, row in df.iterrows():
    if row['位置'] is not None and row['速度'] is not None:
        defult_radius = 2
        if row['星球名'] == '太阳':
            defult_radius = 38
        elif row['星球名'] == '地球' or row['星球名'] == '火星':
            defult_radius = 6
        elif row['星球名'] == '木星':
            defult_radius = 20
        elif row['星球名'] == '土星':
            defult_radius = 12
        elif row['星球名'] == '金星' or row['星球名'] == '水星':
            defult_radius = 3
        star = Star(
            pos=row['位置'],
            vel=row['速度'] * MIU_0,
            radius=defult_radius,
            mass=row['质量'] * MIU_0**2,
        )
        stars.append(star)
# =========== 指定天体系统初始化 ============
system = System(stars)
print(f"系统中天体数量：{len(system.stars)}")
sys_pos = system.plot_pos
sun_pos = df.loc[df['星球名'] == '太阳', '位置'].iloc[0]
sun_vel = df.loc[df['星球名'] == '太阳', '速度'].iloc[0]
earth_pos = df.loc[df['星球名'] == '地球', '位置'].iloc[0]
earth_vel = df.loc[df['星球名'] == '地球', '速度'].iloc[0]
earth_orbit_normal = np.cross(earth_pos - sun_pos, earth_vel - sun_vel)
earth_orbit_normal /= np.linalg.norm(earth_orbit_normal)


n = len(system.stars)
positions = system.plot_pos          # (3, n)
sizes = system.radius.flatten()      # (n,)
colors = system.colors               # (n, 3)



# 下面是渲染逻辑，用户不需要修改区域

# 每个点的历史轨迹
trails = [[] for _ in range(n)]

# ============ 画布 ============
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-BOUND, BOUND)
ax.set_ylim(-BOUND, BOUND)
ax.set_zlim(-BOUND, BOUND)
ax.set_xlabel('X') 
ax.set_ylabel('Y')
ax.set_zlabel('Z')



# 当前点
scatter = ax.scatter(
    positions[0], positions[1], positions[2],
    s=sizes, c=colors, alpha=0.9, edgecolors='none'
)

# 每个点一条轨迹线（颜色用该点自己的颜色）
trail_lines = []
for i in range(n):
    ln, = ax.plot(
        [], [], [],
        color=colors[i],
        linewidth=1.2,
        alpha=0.5,
    )
    trail_lines.append(ln)


# ============ 更新函数 ============
def update(frame):
    global positions, sizes, colors

    system.step(dt=1 / FPS)
    positions = system.plot_pos
    sizes = system.radius.flatten()
    # 更新当前点
    scatter._offsets3d = (positions[0], positions[1], positions[2])
    scatter.set_sizes(sizes)
    scatter.set_color(colors)
    # 更新每个点的轨迹
    for i in range(n):
        trails[i].append(positions[:, i].copy())
        if len(trails[i]) > TRAIL_LEN:
            trails[i].pop(0)

        arr = np.array(trails[i])          # (k, 3)
        trail_lines[i].set_data(arr[:, 0], arr[:, 1])
        trail_lines[i].set_3d_properties(arr[:, 2])

    ax.set_title(f'frame {frame}')
    return [scatter] + trail_lines


anim = FuncAnimation(fig, update, frames=9999, interval=1000 / FPS / MIU)
plt.show()