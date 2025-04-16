# harmonic_sum.py
import numpy as np
import matplotlib.pyplot as plt

def sum_up(N):
    """【正向求和】从小到大计算调和级数前N项和（1 + 1/2 + ... + 1/N）"""
    sum_val = 0.0  # 初始化和值
    # 从1到N遍历，逐个加上当前项的倒数
    for i in range(1, N + 1):
        sum_val += 1.0 / i
    return sum_val

def sum_down(N):
    """【逆向求和】从大到小计算调和级数前N项和（1/N + ... + 1/2 + 1）"""
    sum_val = 0.0  # 初始化和值
    # 从N到1倒序遍历，逐个加上当前项的倒数
    for i in range(N, 0, -1):
        sum_val += 1.0 / i
    return sum_val

def calculate_relative_difference(N):
    """计算两种求和方法的相对差异"""
    s_up = sum_up(N)    # 获取正向求和结果
    s_down = sum_down(N) # 获取逆向求和结果
    avg = (s_up + s_down) / 2  # 计算平均值作为分母
    # 处理分母为零的特殊情况
    return abs(s_up - s_down) / avg if avg != 0 else 0.0

def plot_differences():
    """绘制相对差异随N变化的双对数坐标图"""
    # 生成对数分布的N值（10^1到10^4共50个点）
    N_values = np.logspace(1, 4, 50, dtype=int)
    unique_N = np.unique(N_values)  # 去除重复值
    
    # 计算每个N对应的相对差异
    deltas = [calculate_relative_difference(N) for N in unique_N]
    
    # 配置绘图参数
    plt.figure(figsize=(10, 6))
    # 绘制红色圆点连线图，点大小为4，线宽1
    plt.loglog(unique_N, deltas, 'ro-', markersize=4, linewidth=1)
    plt.xlabel("N值（对数坐标）", fontsize=12)
    plt.ylabel("相对差异（对数坐标）", fontsize=12)
    plt.title("调和级数求和顺序差异分析", fontsize=14)
    plt.grid(True, which="both", linestyle="--", alpha=0.6)  # 添加网格线
    plt.tight_layout()  # 自动调整布局
    plt.show()

def print_results():
    """打印典型N值的计算结果"""
    N_values = [10, 100, 1000, 10000]
    # 打印表头
    print("\nN值      正向求和        逆向求和        相对差异")
    print("-" * 55)
    # 遍历每个N值计算结果
    for N in N_values:
        s_up = sum_up(N)
        s_down = sum_down(N)
        delta = calculate_relative_difference(N)
        # 格式化输出：N值左对齐，数值保留6位小数，差异用科学计数法显示
        print(f"{N:<8} {s_up:<16.6f} {s_down:<16.6f} {delta:.3e}")

def main():
    """主执行流程"""
    print_results()   # 打印关键结果
    plot_differences()  # 生成差异分析图

if __name__ == "__main__":
    main()
