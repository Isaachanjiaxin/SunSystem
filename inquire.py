import numpy as np
import pandas as pd
from astroquery.jplhorizons import Horizons
from astropy.time import Time

# 单位换算系数
AU_TO_M = 1.495978707e11          # 1 AU = 1.495978707e11 m
AUDAY_TO_MS = AU_TO_M / 86400.0   # 1 AU/day = 1.731456e6 m/s

BODY_IDS = {
    '太阳': '10', '水星': '199', '金星': '299', '地球': '399',
    '火星': '499', '木星': '599', '土星': '699', '天王星': '799',
    '海王星': '899', '冥王星': '999', '月球': '301', '冥卫一': '901',
}

MASSES = {
    '太阳':   1.9885e30,
    '水星':   3.3011e23,
    '金星':   4.8675e24,
    '地球':   5.9722e24,
    '火星':   6.4171e23,
    '木星':   1.8982e27,
    '土星':   5.6834e26,
    '天王星': 8.6810e25,
    '海王星': 1.0241e26,
    '冥王星': 1.3030e22,
    '月球':   7.3460e22,
    '冥卫一': 1.5860e21,
}

RADII = {
    '太阳':   6.957e8,
    '水星':   2.4397e6,
    '金星':   6.0518e6,
    '地球':   6.3710e6,
    '火星':   3.3895e6,
    '木星':   6.9911e7,
    '土星':   5.8232e7,
    '天王星': 2.5362e7,
    '海王星': 2.4622e7,
    '冥王星': 1.1883e6,
    '月球':   1.7374e6,
    '冥卫一': 6.0600e5,
}


def query_state(date_str, body_name, center='@sun'):
    """查询位置和速度，返回 SI 单位：位置 m，速度 m/s"""
    body_id = BODY_IDS.get(body_name.strip())
    if body_id is None:
        return None
    epoch = Time(date_str)
    obj = Horizons(id=body_id, location=center, epochs=epoch.jd)
    vec = obj.vectors()

    pos_au = np.array([float(vec['x'][0]), float(vec['y'][0]), float(vec['z'][0])])
    vel_auday = np.array([float(vec['vx'][0]), float(vec['vy'][0]), float(vec['vz'][0])])

    return {
        'pos': pos_au * AU_TO_M,        # m
        'vel': vel_auday * AUDAY_TO_MS, # m/s
    }


def build_dataset(date_str, output_csv='solar_system_data.csv'):
    rows = []
    for name in BODY_IDS:
        state = query_state(date_str, name)
        rows.append({
            '星球名': name,
            '位置': state['pos'] if state else None,
            '速度': state['vel'] if state else None,
            '半径': RADII.get(name),
            '质量': MASSES.get(name),
        })
        print(f"已查询：{name}")

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    return df


if __name__ == '__main__':
    df = build_dataset('2026-10-04', 'solar_system_data.csv')
    print(df)