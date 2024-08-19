# coding:utf-8
import os

# 读取 requirements.txt 文件内容
with open('requirements.txt', 'r', encoding='utf-16 LE') as file:
    dependencies = file.readlines()

# 去重并保持顺序
unique_dependencies = list(dict.fromkeys([dep.strip() for dep in dependencies]))

# 重命名原来的 requirements.txt 文件
os.rename('requirements.txt', 'requirements_backup.txt')

# 将去重后的依赖项写入新的 requirements.txt 文件
with open('requirements.txt', 'w', encoding='utf-8') as file:
    for dep in unique_dependencies:
        file.write(dep + '\n')

print("去重后的依赖项已保存为新的 requirements.txt，原文件已重命名为 requirements_backup.txt")
