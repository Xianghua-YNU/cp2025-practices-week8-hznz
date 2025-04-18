# integration.py
import numpy as np
import matplotlib.pyplot as plt
import time

def f(x):
    """被积函数 f(x) = sqrt(1-x^2)"""
    return np.sqrt(1 - x**2)

def rectangle_method(f, a, b, N):
    """矩形法（左矩形法）计算积分"""
    h = (b - a) / N
    integral = 0.0
    for i in range(N):
        x_i = a + i * h
        integral += f(x_i) * h
    return integral

def trapezoid_method(f, a, b, N):
    """梯形法计算积分"""
    h = (b - a) / N
    integral = (f(a) + f(b)) * 0.5 * h
    for i in range(1, N):
        x_i = a + i * h
        integral += f(x_i) * h
    return integral

def calculate_errors(a, b, exact_value):
    """计算不同N值下各方法的相对误差"""
    N_values = [10, 100, 1000, 10000, 100000]
    h_values = []
    rect_errors = []
    trap_errors = []
    for N in N_values:
        h = (b - a) / N
        h_values.append(h)
        rect_result = rectangle_method(f, a, b, N)
        trap_result = trapezoid_method(f, a, b, N)
        rect_errors.append(abs(rect_result - exact_value) / abs(exact_value))
        trap_errors.append(abs(trap_result - exact_value) / abs(exact_value))
    return (N_values, h_values, rect_errors, trap_errors)

def plot_errors(h_values, rect_errors, trap_errors):
    """绘制误差-步长双对数图"""
    plt.loglog(h_values, rect_errors, 'o-', label='Rectangle Method')
    plt.loglog(h_values, trap_errors, 's-', label='Trapezoid Method')
    h_ref = np.array(h_values)
    plt.loglog(h_ref, h_ref, '--', label='O(h)')
    plt.loglog(h_ref, h_ref**2, '--', label='O(h²)')
    plt.xlabel('Step Size (h)')
    plt.ylabel('Relative Error')
    plt.title('Error vs. Step Size for Integration Methods')
    plt.legend()
    plt.grid(True)
    plt.show()

def print_results(N_values, rect_results, trap_results, exact_value):
    """打印结果表格"""
    print("N\tRectangle Result\tTrapezoid Result\tExact Value")
    for N, rect, trap in zip(N_values, rect_results, trap_results):
        print(f"{N}\t{rect:.10f}\t{trap:.10f}\t{exact_value:.10f}")

def time_performance_test(a, b, max_time=1.0):
    """测试在限定时间内各方法的最高精度"""
    exact_value = 0.5 * np.pi
    # 测试矩形法
    start = time.time()
    N_rect = 1
    best_rect_error = float('inf')
    while time.time() - start < max_time:
        t0 = time.time()
        result = rectangle_method(f, a, b, N_rect)
        t1 = time.time()
        if t1 - start > max_time:
            break
        error = abs(result - exact_value) / exact_value
        if error < best_rect_error:
            best_rect_error = error
            best_N_rect = N_rect
        N_rect *= 2
    # 测试梯形法
    start = time.time()
    N_trap = 1
    best_trap_error = float('inf')
    while time.time() - start < max_time:
        t0 = time.time()
        result = trapezoid_method(f, a, b, N_trap)
        t1 = time.time()
        if t1 - start > max_time:
            break
        error = abs(result - exact_value) / exact_value
        if error < best_trap_error:
            best_trap_error = error
            best_N_trap = N_trap
        N_trap *= 2
    print(f"矩形法最佳N: {best_N_rect}, 误差: {best_rect_error:.2e}")
    print(f"梯形法最佳N: {best_N_trap}, 误差: {best_trap_error:.2e}")

def calculate_convergence_rate(h_values, errors):
    """计算收敛阶数（最小二乘法拟合）"""
    log_h = np.log(np.array(h_values))
    log_e = np.log(np.array(errors))
    A = np.vstack([log_h, np.ones(len(log_h))]).T
    slope, _ = np.linalg.lstsq(A, log_e, rcond=None)[0]
    return slope

def main():
    a, b = -1.0, 1.0
    exact_value = 0.5 * np.pi
    print(f"积分 ∫_{a}^{b} √(1-x²) dx 的精确值: {exact_value:.10f}")

    N_values = [10, 100, 1000, 10000]
    rect_results = [rectangle_method(f, a, b, N) for N in N_values]
    trap_results = [trapezoid_method(f, a, b, N) for N in N_values]

    print_results(N_values, rect_results, trap_results, exact_value)
    N_values, h_values, rect_errors, trap_errors = calculate_errors(a, b, exact_value)
    plot_errors(h_values, rect_errors, trap_errors)

    rect_rate = calculate_convergence_rate(h_values, rect_errors)
    trap_rate = calculate_convergence_rate(h_values, trap_errors)
    print(f"\n收敛阶数：矩形法 {rect_rate:.2f}, 梯形法 {trap_rate:.2f}")

    time_performance_test(a, b)

if __name__ == "__main__":
    main()
