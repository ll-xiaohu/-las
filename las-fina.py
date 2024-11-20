import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import time

def update_progress(current, total, start_time, src_file):
    elapsed_time = time.time() - start_time
    if elapsed_time > 0:
        speed = (os.path.getsize(src_file) / (1024 * 1024)) / elapsed_time
        speed_str = f" ({speed:.2f} MB/s)"
    else:
        speed_str = ""
    progress_var.set((current / total) * 100)
    log_text.insert(tk.END, f"已处理 {current} 个文件，共 {total} 个文件{speed_str}\n")
    log_text.see(tk.END)

def copy_and_rename_las_files(src_folder, dst_folder):
    global running
    no_las_folders = []
    total_files = 0
    processed_files = 0
    start_time = time.time()

    # 计算总文件数
    for root, dirs, files in os.walk(src_folder):
        if 'terra_las' in dirs:
            src_terra_las_folder = os.path.join(root, 'terra_las')
            total_files += len([f for f in os.listdir(src_terra_las_folder) if f.endswith('.las')])

    if total_files == 0:
        messagebox.showinfo("提示", "没有找到 .las 文件")
        return

    for root, dirs, files in os.walk(src_folder):
        if not running:
            break

        if 'terra_las' in dirs:
            src_terra_las_folder = os.path.join(root, 'terra_las')
            top_folder_name = os.path.basename(os.path.dirname(root))
            dst_subfolder = os.path.join(dst_folder, top_folder_name)

            if not os.path.exists(dst_subfolder):
                os.makedirs(dst_subfolder)
                log_text.insert(tk.END, f"创建目录: {dst_subfolder}\n")
                log_text.see(tk.END)

            las_files = [f for f in os.listdir(src_terra_las_folder) if f.endswith('.las')]
            if not las_files:
                no_las_folders.append(top_folder_name)
                continue

            # 重置局部计数器
            local_counter = 1

            for filename in las_files:
                if not running:
                    break

                src_file = os.path.join(src_terra_las_folder, filename)
                dst_file = os.path.join(dst_subfolder, f'{top_folder_name}-{local_counter}.las')
                shutil.copy(src_file, dst_file)
                log_text.insert(tk.END, f"复制文件: {dst_file}\n")
                log_text.see(tk.END)
                local_counter += 1
                processed_files += 1
                update_progress(processed_files, total_files, start_time, src_file)

    if no_las_folders:
        with open('no_las_folders.txt', 'w') as f:
            for folder in no_las_folders:
                f.write(f"{folder}\n")

    if running:
        messagebox.showinfo("提示", "文件复制完成")
    else:
        messagebox.showinfo("提示", "文件复制已暂停")

def select_source_folder():
    global src_path
    src_path = filedialog.askdirectory()
    src_path_var.set(src_path)

def select_destination_folder():
    global dst_path
    dst_path = filedialog.askdirectory()
    dst_path_var.set(dst_path)

def start_copy():
    if not src_path or not dst_path:
        messagebox.showwarning("警告", "请选择源路径和目标路径")
        return

    global running
    running = True
    copy_thread = threading.Thread(target=lambda: copy_and_rename_las_files(src_path, dst_path))
    copy_thread.start()

def pause_copy():
    global running
    running = False

# 初始化变量
src_path = ""
dst_path = ""
running = False

# 创建主窗口
root = tk.Tk()
root.title("las复制工具")

# 源路径选择
src_path_var = tk.StringVar()
tk.Label(root, text="las源路径:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=src_path_var, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="选择源路径", command=select_source_folder, width=15).grid(row=0, column=2, padx=10, pady=10)

# 目标路径选择
dst_path_var = tk.StringVar()
tk.Label(root, text="目标路径:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=dst_path_var, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="选择目标路径", command=select_destination_folder, width=15).grid(row=1, column=2, padx=10, pady=10)

# 开始和暂停按钮
tk.Button(root, text="开始", command=start_copy, width=15).grid(row=2, column=0, padx=10, pady=10)
tk.Button(root, text="暂停", command=pause_copy, width=15).grid(row=2, column=1, padx=10, pady=10)

# 进度条
progress_var = tk.DoubleVar()
progress_bar = Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# 日志显示
log_text = tk.Text(root, height=10, width=70)
log_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# 运行主循环
root.mainloop()
