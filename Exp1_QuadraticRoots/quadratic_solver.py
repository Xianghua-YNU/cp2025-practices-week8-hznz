
import numpy as np

def standard_formula(a, b, c):
    """使用标准公式求解二次方程 ax^2 + bx + c = 0
    
    参数:
        a (float): 二次项系数
        b (float): 一次项系数
        c (float): 常数项
    
    返回:
        tuple: 方程的两个根 (x1, x2) 或 None(无实根)
    """
    D = b**2 - 4*a*c
    if D < 0:
        return None
    sqrt_D = np.sqrt(D)
    x1 = (-b + sqrt_D) / (2*a)
    x2 = (-b - sqrt_D) / (2*a)
    return (x1, x2)

def alternative_formula(a, b, c):
    """使用替代公式求解二次方程，避免灾难性抵消
    
    参数:
        a (float): 二次项系数
        b (float): 一次项系数
        c (float): 常数项
    
    返回:
        tuple: 方程的两个根 (x1, x2) 或 None(无实根)
    """
    D = b**2 - 4*a*c
    if D < 0:
        return None
    sqrt_D = np.sqrt(D)
    if b >= 0:
        denominator = -b - sqrt_D
        x1 = (2*c) / denominator
        x2 = denominator / (2*a)  # 等效于标准公式中的减法形式
    else:
        denominator = -b + sqrt_D
        x1 = (2*c) / denominator
        x2 = denominator / (2*a)  # 等效于标准公式中的加法形式
    return (x1, x2)

def stable_formula(a, b, c):
    """稳定的二次方程求根程序，综合标准公式和替代公式
    
    参数:
        a (float): 二次项系数
        b (float): 一次项系数
        c (float): 常数项
    
    返回:
        tuple: 方程的两个根 (x1, x2) 或 None(无实根)
    """
    if a == 0:
        # 处理线性方程
        if b == 0:
            return None  # 无解
        x = -c / b
        return (x, x)    # 线性方程单根重复两次
    D = b**2 - 4*a*c
    if D < 0:
        return None
    sqrt_D = np.sqrt(D)
    if D == 0:
        x = -b / (2*a)
        return (x, x)
    # 根据b的符号选择稳定的计算方式
    if b >= 0:
        denominator = -b - sqrt_D
        x1 = denominator / (2*a)
        x2 = (2*c) / denominator
    else:
        denominator = -b + sqrt_D
        x1 = denominator / (2*a)
        x2 = (2*c) / denominator
    return (x1, x2)

def main():
    test_cases = [
        (1, 2, 1),             # 简单情况（重复根）
        (1, 1e5, 1),           # 大b值测试
        (0.001, 1000, 0.001),  # 实验说明中的测试用例
    ]
    
    for a, b, c in test_cases:
        print("\n" + "="*50)
        print(f"测试方程：{a}x² + {b}x + {c} = 0")
        
        # 标准公式计算结果
        roots_std = standard_formula(a, b, c)
        print("\n标准公式结果:")
        print(roots_std if roots_std else "无实根")
        
        # 替代公式计算结果
        roots_alt = alternative_formula(a, b, c)
        print("\n替代公式结果:")
        print(roots_alt if roots_alt else "无实根")
        
        # 稳定公式计算结果
        roots_stable = stable_formula(a, b, c)
        print("\n稳定公式结果:")
        print(roots_stable if roots_stable else "无实根")

if __name__ == "__main__":
    main()
