import os
import shutil

def copy_and_rename_las_files(src_folder, dst_folder):
    # 初始化局部计数器
    local_counter = 1

    for root, dirs, files in os.walk(src_folder):
        if 'terra_las' in dirs:  # 只处理名为"terra_las"的子文件夹
            src_terra_las_folder = os.path.join(root, 'terra_las')

            # 获取一级文件夹的名称
            top_folder_name = os.path.basename(os.path.dirname(root))

            # 创建目标二级文件夹
            dst_subfolder = os.path.join(dst_folder, top_folder_name)
            if not os.path.exists(dst_subfolder):
                os.makedirs(dst_subfolder)
                print(f"创建目录: {dst_subfolder}")

            for filename in os.listdir(src_terra_las_folder):
                if filename.endswith('.las'):
                    src_file = os.path.join(src_terra_las_folder, filename)
                    dst_file = os.path.join(dst_subfolder, f'{top_folder_name}-{local_counter}.las')

                    # 复制并重命名文件
                    shutil.copy(src_file, dst_file)
                    print(f"复制文件: {dst_file}")
                    local_counter += 1

# 获取用户输入的源路径和目标路径
src_path = input("请输入las文件所在路径: ")  # 用户输入源路径
dst_path = input("请输入需要存放las文件的路径: ")  # 用户输入目标路径

# 开始遍历并处理每个子文件夹
for foldername in os.listdir(src_path):
    src_folder = os.path.join(src_path, foldername)
    if os.path.isdir(src_folder):
        copy_and_rename_las_files(src_folder, dst_path)