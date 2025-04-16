import numpy as np
import matplotlib.pyplot as plt
from scipy.special import spherical_jn

def bessel_up(x, lmax):
    """向上递推计算球贝塞尔函数
    
    Args:
        x: float, 自变量
        lmax: int, 最大阶数
        
    Returns:
        numpy.ndarray, 从0到lmax阶的球贝塞尔函数值
    """
    # 学生在此实现向上递推算法
    # 提示:
    # 1. 初始化结果数组
    # 2. 计算j_0和j_1的初始值
    # 3. 使用递推公式计算高阶项
      j = np.zeros(lmax + 1)
    
    # 处理x=0的特殊情况
    if x == 0:
        j[0] = 1.0  # j0(0)=1
        return j
    
    # 计算初始值
    j[0] = np.sin(x) / x
    if lmax >= 1:
        j[1] = np.sin(x) / (x**2) - np.cos(x) / x
    
    # 向上递推
    for l in range(1, lmax):
        j[l+1] = (2*l + 1)/x * j[l] - j[l-1]
    
    return j

def bessel_down(x, lmax, m_start=None):
    """向下递推计算球贝塞尔函数
    
    Args:
        x: float, 自变量
        lmax: int, 最大阶数
        m_start: int, 起始阶数，默认为lmax + 15
        
    Returns:
        numpy.ndarray, 从0到lmax阶的球贝塞尔函数值
    """
    # 学生在此实现向下递推算法
    # 提示:
    # 1. 设置足够高的起始阶数
    # 2. 初始化临时数组并设置初始值
    # 3. 使用递推公式向下计算
    # 4. 使用j_0(x)进行归一化
     if m_start is None:
        m_start = lmax + 15  # 默认起始阶数
    
    # 初始化数组
    j_temp = np.zeros(m_start + 2)
    
    # 设置初始值（任意小的非零值）
    j_temp[m_start + 1] = 0.0
    j_temp[m_start] = 1.0e-20
    
    # 向下递推
    for l in range(m_start, 0, -1):
        j_temp[l-1] = (2*l + 1)/x * j_temp[l] - j_temp[l+1]
    
    # 归一化
    j0_analytic = np.sin(x)/x if x != 0 else 1.0
    scale = j0_analytic / j_temp[0]
    
    # 返回0到lmax的结果
    return j_temp[:lmax+1] * scale

def plot_comparison(x, lmax):
    """绘制不同方法计算结果的比较图
    
    Args:
        x: float, 自变量
        lmax: int, 最大阶数
    """
    # 学生在此实现绘图功能
    # 提示:
    # 1. 计算三种方法的结果
    # 2. 绘制函数值的半对数图
    # 3. 绘制相对误差的半对数图
    # 4. 添加图例、标签和标题
     # 计算三种方法的结果
    j_up = bessel_up(x, lmax)
    j_down = bessel_down(x, lmax)
    l_values = np.arange(lmax + 1)
    j_scipy = spherical_jn(l_values, x)
    
    # 创建图形
    plt.figure(figsize=(12, 5))
    
    # 绘制函数值比较图
    plt.subplot(1, 2, 1)
    plt.semilogy(l_values, np.abs(j_up), 'o-', label='Upward Recurrence')
    plt.semilogy(l_values, np.abs(j_down), 's-', label='Downward Recurrence')
    plt.semilogy(l_values, np.abs(j_scipy), '^-', label='Scipy Reference')
    plt.xlabel('Order l')
    plt.ylabel('|j_l(x)|')
    plt.title(f'Comparison of Methods (x={x})')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    
    # 绘制相对误差图
    plt.subplot(1, 2, 2)
    with np.errstate(divide='ignore', invalid='ignore'):
        rel_err_up = np.abs((j_up - j_scipy) / j_scipy)
        rel_err_down = np.abs((j_down - j_scipy) / j_scipy)
    
    # 处理j_scipy为零的情况
    mask_up = (j_scipy != 0) & (rel_err_up != 0)
    mask_down = (j_scipy != 0) & (rel_err_down != 0)
    
    plt.semilogy(l_values[mask_up], rel_err_up[mask_up], 'o-', label='Upward Error')
    plt.semilogy(l_values[mask_down], rel_err_down[mask_down], 's-', label='Downward Error')
    plt.xlabel('Order l')
    plt.ylabel('Relative Error')
    plt.title(f'Relative Error (x={x})')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    
    plt.tight_layout()
    plt.show()

def main():
    """主函数"""
    # 设置参数
    lmax = 25
    x_values = [0.1, 1.0, 10.0]
    
    # 对每个x值进行计算和绘图
    for x in x_values:
        plot_comparison(x, lmax)
        
        # 打印特定阶数的结果
        l_check = [3, 5, 8]
        print(f"\nx = {x}:")
        print("l\tUp\t\tDown\t\tScipy")
        print("-" * 50)
        for l in l_check:
            j_up = bessel_up(x, l)[l]
            j_down = bessel_down(x, l)[l]
            j_scipy = spherical_jn(l, x)
            print(f"{l}\t{j_up:.6e}\t{j_down:.6e}\t{j_scipy:.6e}")

if __name__ == "__main__":
    main()
