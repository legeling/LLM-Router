#!/usr/bin/env python3
"""
LLM网关 - 交互式Git管理脚本
用于提交代码到GitHub仓库
"""
import os
import sys
import subprocess
from datetime import datetime

# 远程仓库地址
REMOTE_REPO = "git@github.com:legeling/LLM_server.git"

def run_command(command, show_output=True):
    """运行shell命令并返回结果"""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True)
        if show_output and result.stdout:
            print(result.stdout)
        return result.stdout, True
    except subprocess.CalledProcessError as e:
        print(f"错误: {e}")
        if e.stderr:
            print(f"详细信息: {e.stderr}")
        return e.stderr, False

def is_git_repo():
    """检查当前目录是否为git仓库"""
    return os.path.exists(".git")

def init_repo():
    """初始化git仓库"""
    if not is_git_repo():
        print("初始化Git仓库...")
        run_command("git init")
        run_command(f"git remote add origin {REMOTE_REPO}")
        print(f"已添加远程仓库: {REMOTE_REPO}")
    else:
        print("Git仓库已存在")
        # 检查远程仓库
        stdout, success = run_command("git remote -v", show_output=False)
        if REMOTE_REPO not in stdout:
            choice = input(f"是否更新远程仓库地址为 {REMOTE_REPO}? (y/n): ").lower()
            if choice == 'y':
                if "origin" in stdout:
                    run_command(f"git remote set-url origin {REMOTE_REPO}")
                else:
                    run_command(f"git remote add origin {REMOTE_REPO}")
                print(f"已更新远程仓库地址: {REMOTE_REPO}")

def show_status():
    """显示当前仓库状态"""
    print("\n=== 当前仓库状态 ===")
    run_command("git status")

def add_files():
    """添加文件到暂存区"""
    show_status()
    print("\n=== 添加文件 ===")
    choice = input("选择操作: \n1. 添加所有文件 \n2. 添加指定文件\n请选择 (1/2): ")
    
    if choice == "1":
        run_command("git add .")
        print("已添加所有文件")
    elif choice == "2":
        files = input("输入要添加的文件(用空格分隔): ")
        if files.strip():
            run_command(f"git add {files}")
            print(f"已添加指定文件: {files}")
    else:
        print("无效选择")

def commit_changes():
    """提交更改"""
    print("\n=== 提交更改 ===")
    default_msg = f"更新 LLM网关 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    msg = input(f"输入提交信息 (默认: '{default_msg}'): ")
    
    if not msg.strip():
        msg = default_msg
    
    run_command(f'git commit -m "{msg}"')
    print(f"已提交更改: {msg}")

def push_changes():
    """推送更改到远程仓库"""
    print("\n=== 推送更改 ===")
    
    # 获取当前分支
    stdout, success = run_command("git branch --show-current", show_output=False)
    current_branch = stdout.strip() if success else "main"
    if not current_branch:
        current_branch = "main"
    
    branch = input(f"输入要推送的分支 (默认: '{current_branch}'): ")
    if not branch.strip():
        branch = current_branch
    
    print(f"正在推送到 {branch} 分支...")
    stdout, success = run_command(f"git push -u origin {branch}")
    
    if success:
        print(f"成功推送到 {REMOTE_REPO} 的 {branch} 分支")
    else:
        print("推送失败，请检查错误信息")

def pull_changes():
    """拉取远程仓库更改"""
    print("\n=== 拉取更改 ===")
    
    # 获取当前分支
    stdout, success = run_command("git branch --show-current", show_output=False)
    current_branch = stdout.strip() if success else "main"
    if not current_branch:
        current_branch = "main"
    
    branch = input(f"输入要拉取的分支 (默认: '{current_branch}'): ")
    if not branch.strip():
        branch = current_branch
    
    print(f"正在从 {branch} 分支拉取...")
    run_command(f"git pull origin {branch}")

def create_branch():
    """创建新分支"""
    print("\n=== 创建分支 ===")
    branch = input("输入新分支名称: ")
    
    if branch.strip():
        run_command(f"git checkout -b {branch}")
        print(f"已创建并切换到分支: {branch}")
    else:
        print("分支名称不能为空")

def switch_branch():
    """切换分支"""
    print("\n=== 切换分支 ===")
    stdout, _ = run_command("git branch", show_output=False)
    print("可用分支:")
    print(stdout)
    
    branch = input("输入要切换的分支名称: ")
    if branch.strip():
        run_command(f"git checkout {branch}")
        print(f"已切换到分支: {branch}")
    else:
        print("分支名称不能为空")

def show_menu():
    """显示主菜单"""
    print("\n=== LLM网关 Git管理 ===")
    print("1. 显示仓库状态")
    print("2. 添加文件")
    print("3. 提交更改")
    print("4. 推送到远程仓库")
    print("5. 拉取远程更改")
    print("6. 创建新分支")
    print("7. 切换分支")
    print("8. 快速提交并推送")
    print("0. 退出")
    
    choice = input("\n请选择操作 (0-8): ")
    return choice

def quick_commit_push():
    """快速提交并推送"""
    print("\n=== 快速提交并推送 ===")
    run_command("git add .")
    print("已添加所有文件")
    
    default_msg = f"更新 LLM网关 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    msg = input(f"输入提交信息 (默认: '{default_msg}'): ")
    if not msg.strip():
        msg = default_msg
    
    run_command(f'git commit -m "{msg}"')
    
    # 获取当前分支
    stdout, success = run_command("git branch --show-current", show_output=False)
    current_branch = stdout.strip() if success else "main"
    if not current_branch:
        current_branch = "main"
    
    print(f"正在推送到 {current_branch} 分支...")
    run_command(f"git push -u origin {current_branch}")
    print(f"已成功提交并推送到 {current_branch} 分支")

def main():
    """主函数"""
    print("欢迎使用 LLM网关 Git管理工具")
    
    # 初始化仓库
    init_repo()
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            show_status()
        elif choice == "2":
            add_files()
        elif choice == "3":
            commit_changes()
        elif choice == "4":
            push_changes()
        elif choice == "5":
            pull_changes()
        elif choice == "6":
            create_branch()
        elif choice == "7":
            switch_branch()
        elif choice == "8":
            quick_commit_push()
        elif choice == "0":
            print("感谢使用，再见！")
            sys.exit(0)
        else:
            print("无效选择，请重试")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n操作已取消")
        sys.exit(0) 