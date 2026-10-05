# 使用spaceGame进行太阳系的模拟
## 依赖安装
```bash
pip install numpy matplotlib
```
## 启动方式
进入文件夹后输入命令，或点击运行
```bash
python main.py
```

## 文件说明
-[] soloar_system_data.csv 一个用于保存确定时间点的各个星体位置与固定物理参数的表格，主程序中通过读取该表格进行数据的初始化
-[] inquire.py 使用NASA的数据库进行查询，其中星体质量和半径为硬编码()查询权威数据后手动填入，位置和速度参数为网站上抓取的信息，若在国内运行需要使用国外代理进行网络连接
-[] 其他文件与SpaceGame仓库中功能相同，尚未封装成软件包