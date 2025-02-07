import os
import shutil
import hashlib
import chardet

def encrypt_filename(filename):
    """
    使用 SHA256 哈希算法加密文件名
    """
    encrypted = hashlib.sha256(filename.encode()).hexdigest()  # 对文件名进行SHA256加密
    return encrypted  # 返回加密后的文件名


def is_encrypted(filename):
    """
    检查文件名是否已加密
    """
    try:
        bytes.fromhex(filename)  # 尝试将字符串转换为16进制字节，如果成功则认为是加密的
        return True
    except ValueError:
        return False


def save_filenames():
    """
    保存当前文件夹中所有指定格式的文件名到记事本文件中
    """
    current_dir = os.getcwd()  # 获取当前文件夹路径
    extensions = ('.mp4', '.ts', '.mov', '.avi', '.m4v', '.MP4')  # 指定要处理的文件后缀格式
    filenames_path = 'filenames.txt'
    backup_path = 'filenames_backup.txt'

    # 如果 filenames.txt 已存在，先备份
    if os.path.exists(filenames_path):
        shutil.copy(filenames_path, backup_path)

    files = [file for file in os.listdir(current_dir) if file.endswith(extensions)]  # 获取符合条件的文件列表
    encrypted_files = [file for file in files if is_encrypted(os.path.splitext(file)[0])]  # 获取已加密的文件列表

    if len(encrypted_files) > len(files) // 2:  # 如果加密文件超过一半，则不保存
        print("文件多数处于加密状态，取消保存")
        return

    with open(filenames_path, 'w', encoding='utf-8') as f:  # 打开一个写入模式的记事本文件，并指定编码格式为 UTF-8
        for file in files:  # 遍历符合条件的文件
            f.write(file + '\n')  # 将文件名写入记事本文件中
    print("文件名已保存到 filenames.txt")  # 打印操作完成的消息


def rename_files():
    """
    读取保存的文件名列表，并将文件名加密后重命名，同时修改文件后缀
    """
    encoding = detect_encoding('filenames.txt')  # 检测文件的编码格式
    with open('filenames.txt', 'r', encoding=encoding) as f:  # 打开记事本文件读取文件名
        filenames = f.read().splitlines()  # 将文件名逐行读取并存储到列表中

    for filename in filenames:  # 遍历所有文件名
        name, ext = os.path.splitext(filename)  # 分离文件名和后缀
        encrypted_name = encrypt_filename(name)  # 加密文件名
        new_ext = '.enc'  # 假设加密文件后缀为 .enc
        new_filename = encrypted_name + new_ext  # 生成新的文件名（加密名+新后缀）

        # 检查文件是否已经加密，避免重复加密
        if not filename.endswith('.enc'):
            os.rename(filename, new_filename)  # 重命名文件
    print("文件名和后缀已加密并修改")  # 打印操作完成的消息


def decrypt_filename(encrypted_filename, original_filenames):
    """
    根据加密文件名恢复原始文件名
    """
    for original_filename in original_filenames:
        name, ext = os.path.splitext(original_filename)  # 分离原始文件名和后缀
        encrypted_name = encrypt_filename(name)  # 加密原始文件名
        if encrypted_filename.startswith(encrypted_name):  # 如果加密文件名匹配
            return original_filename  # 返回原始文件名
    return None  # 如果没有匹配，返回 None


def detect_encoding(file_path):
    """
    检测文件的编码格式
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def restore_filenames():
    """
    读取保存的原始文件名列表，将加密文件名和后缀恢复为原始文件名和后缀
    """
    encoding = detect_encoding('filenames.txt')  # 检测文件的编码格式
    with open('filenames.txt', 'r', encoding=encoding) as f:  # 使用检测到的编码格式读取文件
        original_filenames = f.read().splitlines()  # 将文件名逐行读取并存储到列表中

    for file in os.listdir(os.getcwd()):  # 遍历当前文件夹的所有文件
        name, ext = os.path.splitext(file)  # 分离加密文件名和后缀
        original_filename = decrypt_filename(name, original_filenames)  # 尝试恢复原始文件名
        if original_filename:
            os.rename(file, original_filename)  # 重命名文件为原始文件名和后缀
    print("文件名和后缀已恢复")  # 打印操作完成的消息


def main():
    import sys  # 引入sys模块，用于处理命令行参数
    #save_filenames()
    #rename_files()  # 调用加密文件名并重命名函数
    #restore_filenames() # 调用解密文件名并恢复函数
    if len(sys.argv) != 2:  # 检查命令行参数数量是否正确
        print("请输入要执行的操作（save, encrypt, decrypt）")  # 提示用户输入操作类型
        return
    action = sys.argv[1].strip().lower()  # 获取用户输入的操作类型，并转换为小写
    if action == "save":
        save_filenames()  # 调用保存文件名函数
    elif action == "encrypt":
        rename_files()  # 调用加密文件名并重命名函数
    elif action == "decrypt":
        restore_filenames()  # 调用解密文件名并恢复函数
    else:
        print("无效操作！")  # 如果输入的操作类型无效，打印提示


if __name__ == "__main__":
    main()  # 调用主函数
