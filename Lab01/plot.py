import json
import matplotlib.pyplot as plt
import math
import os

def parse_clock_value(clock_str):
    return float(clock_str.replace('GHz', ''))

def parse_log_size_value(size_str):
    return int(math.log2(int(size_str.replace('kB', ''))))

def plot_performance_data(json_file, output_dir, title, ylabel):
    plt.figure(figsize=(10, 6))
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # 提取时钟频率和对应的值
    clocks = [float(parse_clock_value(k)) for k in data.keys()]
    values = [float(v) for v in data.values()]
    
    # 绘制数据点
    plt.plot(clocks, values, marker='o')
    
    # 设置图表属性
    plt.title(title)
    plt.xlabel('Clock Frequency (GHz)')
    plt.ylabel(ylabel)
    plt.grid(True)
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存图表
    output_file = os.path.join(output_dir, f"{title.lower().replace(' ', '_')}.png")
    plt.savefig(output_file)
    plt.close()  # 关闭图表，避免内存泄漏


def plot_CPI(insts_file, cycles_file, output_dir, title, ylabel):
    with open(insts_file, 'r') as f:
        insts_data = json.load(f)
    with open(cycles_file, 'r') as f:
        cycles_data = json.load(f)
    
    clocks = [float(parse_clock_value(k)) for k in insts_data.keys()]
    insts = [float(v) for v in insts_data.values()]
    cycles = [float(v) for v in cycles_data.values()]
    
    cpi = [cycles[i] / insts[i] for i in range(len(clocks))]
    
    plt.figure(figsize=(10, 6))
    plt.plot(clocks, cpi, marker='o')
    
    plt.title(title)
    plt.xlabel('Clock Frequency (GHz)')
    plt.ylabel(ylabel)
    plt.grid(True)
    
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"{title.lower().replace(' ', '_')}.png")
    plt.savefig(output_file)
    plt.close()

def plot_miss_rate(miss_rate_file, output_dir, title, ylabel):
    with open(miss_rate_file, 'r') as f:
        miss_rate_data = json.load(f)
    
    sizes = [parse_log_size_value(k) for k in miss_rate_data.keys()]
    # y in percentage
    miss_rates = [float(v) * 100 for v in miss_rate_data.values()]
    
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, miss_rates, marker='o')
    
    plt.title(title)
    plt.xlabel('Cache Size (log2(kB))')
    plt.ylabel('Miss Rate (%)')
    plt.grid(True)
    
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"{title.lower().replace(' ', '_')}.png")
    plt.savefig(output_file)
    plt.close()
    

def miss_rates_vs_line_size(miss_rate_file, output_dir, title, ylabel):
    with open(miss_rate_file, 'r') as f:
        miss_rate_data = json.load(f)
    
    line_sizes = [parse_log_size_value(k) for k in miss_rate_data.keys()]
    miss_rates = [float(v) * 100 for v in miss_rate_data.values()]
    
    plt.figure(figsize=(10, 6))
    plt.plot(line_sizes, miss_rates, marker='o')
    
    plt.title(title)
    plt.xlabel('Line Size (log2(B))')
    plt.ylabel(ylabel)
    plt.grid(True)

    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"{title.lower().replace(' ', '_')}.png")
    plt.savefig(output_file)
    plt.close()

def main():
    output_dir = './results/plots'
    # lab 1-1
    plot_performance_data(
        './results/lab1-1/result_clock.json',
        output_dir,
        'Execution Time vs Clock Frequency',
        'Execution Time (seconds)'
    )
    
    plot_CPI(
        './results/lab1-1/result_insts.json',
        './results/lab1-1/result_cycles.json',
        output_dir,
        'CPI vs Clock Frequency',
        'CPI'
    )
    # lab 1-2
    plot_miss_rate(
        './results/lab1-2/result_miss.json',
        output_dir,
        'L1ICache Miss Rate vs Cache Size',
        'L1ICache Miss Rate (%)'
    )
    # lab 1-3
    plot_miss_rate(
        './results/lab1-3/result_miss.json',
        output_dir,
        'L1DCache Miss Rate vs Cache Size',
        'L1DCache Miss Rate (%)'
    )
    # lab 1-4
    plot_miss_rate(
        './results/lab1-4/result_miss.json',
        output_dir,
        'L2Cache Miss Rate vs Cache Size',
        'L2Cache Miss Rate (%)'
    )
    # lab 1-5   
    miss_rates_vs_line_size(
        './results/lab1-5/result_miss_l1d.json',
        output_dir,
        'L1DCache Miss Rate vs Line Size',
        'L1DCache Miss Rate (%)'
    )
    miss_rates_vs_line_size(
        './results/lab1-5/result_miss_l1i.json',
        output_dir,
        'L1ICache Miss Rate vs Line Size',
        'L1ICache Miss Rate (%)'
    )
    miss_rates_vs_line_size(
        './results/lab1-5/result_miss_l2.json',
        output_dir,
        'L2Cache Miss Rate vs Line Size',
        'L2Cache Miss Rate (%)'
    )

if __name__ == '__main__':
    main()
