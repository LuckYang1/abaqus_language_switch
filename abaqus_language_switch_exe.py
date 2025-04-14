#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Abaqus语言切换工具 (可打包为EXE版本)
用于切换Abaqus/CAE的语言设置（中文/英文）

打包命令:
    pip install pyinstaller
    
    # 不带图标打包:
    pyinstaller --onefile --console abaqus_language_switch_exe.py
    
    # 带图标打包:
    pyinstaller --onefile --console --icon=icon.ico abaqus_language_switch_exe.py
    
    # 说明:
    # --onefile: 打包为单个可执行文件
    # --console: 显示控制台窗口
    # --icon: 指定应用程序图标文件路径
"""

import os
import re
import sys
import shutil
import ctypes
import traceback
import json
from datetime import datetime

# 配置文件默认路径
DEFAULT_CONFIG_PATH = r"F:\SIMULIA\EstProducts\2021\win_b64\SMA\Configuration\locale.txt"
# 程序设置文件路径 - 使用用户目录存储设置文件
USER_HOME = os.path.expanduser("~")
SETTINGS_DIR = os.path.join(USER_HOME, "AbaqusLangSwitcher")
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "abaqus_lang_settings.json")

# 全局变量
CONFIG_PATH = ""
BACKUP_PATH = ""
PATH_LIST = []

def load_settings():
    """加载配置设置"""
    global CONFIG_PATH, BACKUP_PATH, PATH_LIST
    
    # 确保设置目录存在
    if not os.path.exists(SETTINGS_DIR):
        try:
            os.makedirs(SETTINGS_DIR)
            print(f"已创建设置目录: {SETTINGS_DIR}")
        except Exception as e:
            print(f"警告: 创建设置目录失败: {str(e)}")
    
    # 如果设置文件存在，则从中加载配置路径
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                CONFIG_PATH = settings.get("current_path", DEFAULT_CONFIG_PATH)
                PATH_LIST = settings.get("path_list", [])
                
                # 如果PATH_LIST为空但有current_path，则添加current_path到PATH_LIST
                if not PATH_LIST and CONFIG_PATH != DEFAULT_CONFIG_PATH:
                    PATH_LIST.append({
                        "name": "默认路径",
                        "path": CONFIG_PATH,
                        "added_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                
                # 如果当前路径不在PATH_LIST中，则添加DEFAULT_CONFIG_PATH
                if not PATH_LIST:
                    PATH_LIST.append({
                        "name": "默认路径",
                        "path": DEFAULT_CONFIG_PATH,
                        "added_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    CONFIG_PATH = DEFAULT_CONFIG_PATH
                
                print(f"已从设置文件加载配置路径: {CONFIG_PATH}")
                print(f"已加载 {len(PATH_LIST)} 个保存的路径")
        except Exception as e:
            print(f"警告: 读取设置文件时出错: {str(e)}")
            CONFIG_PATH = DEFAULT_CONFIG_PATH
            PATH_LIST = [{
                "name": "默认路径",
                "path": DEFAULT_CONFIG_PATH,
                "added_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }]
    else:
        CONFIG_PATH = DEFAULT_CONFIG_PATH
        PATH_LIST = [{
            "name": "默认路径",
            "path": DEFAULT_CONFIG_PATH,
            "added_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }]
        print(f"使用默认配置路径: {CONFIG_PATH}")
        # 尝试立即保存默认设置
        save_settings()
    
    BACKUP_PATH = f"{CONFIG_PATH}.bak"

def save_settings():
    """保存配置设置"""
    try:
        # 确保设置目录存在
        if not os.path.exists(SETTINGS_DIR):
            os.makedirs(SETTINGS_DIR)
            
        settings = {
            "current_path": CONFIG_PATH,
            "path_list": PATH_LIST
        }
        
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
            
        print(f"已保存设置到: {SETTINGS_FILE}")
        return True
    except Exception as e:
        print(f"错误: 保存设置时出错: {str(e)}")
        print(traceback.format_exc())
        return False

def is_admin():
    """检查程序是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def print_menu():
    """打印菜单"""
    print("=" * 40)
    print("       Abaqus语言切换工具")
    print("=" * 40)
    print("  1. 切换到中文")
    print("  2. 切换到英文")
    print("  3. 恢复备份")
    print("  4. 管理配置文件路径")
    print("  5. 退出")
    print("=" * 40)

def path_exists_in_list(path):
    """检查路径是否存在于PATH_LIST中"""
    for item in PATH_LIST:
        if item["path"].lower() == path.lower():
            return True
    return False

def add_path_to_list(path, name=None):
    """添加路径到PATH_LIST"""
    if not path_exists_in_list(path):
        if name is None:
            name = f"路径 {len(PATH_LIST) + 1}"
        
        PATH_LIST.append({
            "name": name,
            "path": path,
            "added_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return True
    return False

def create_backup():
    """创建配置文件备份（仅在首次运行时）"""
    # 如果已存在备份，则不再创建
    if os.path.exists(BACKUP_PATH):
        return True
                
    try:
        # 创建备份
        shutil.copy2(CONFIG_PATH, BACKUP_PATH)
        print(f"已创建备份文件: {BACKUP_PATH}")
        return True
    except Exception as e:
        print(f"错误: 创建备份文件时出错: {str(e)}")
        return False

def restore_backup():
    """恢复初始配置文件备份"""
    if not os.path.exists(BACKUP_PATH):
        print(f"错误: 找不到备份文件: {BACKUP_PATH}")
        return False
        
    try:
        # 直接从备份恢复
        shutil.copy2(BACKUP_PATH, CONFIG_PATH)
        print(f"已成功恢复到初始状态!")
        return True
    except Exception as e:
        print(f"错误: 恢复备份时出错: {str(e)}")
        return False

def switch_to_chinese():
    """切换到中文模式"""
    if not os.path.exists(CONFIG_PATH):
        print(f"错误: 找不到配置文件: {CONFIG_PATH}")
        return
        
    try:
        # 读取文件内容
        with open(CONFIG_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # 检查是否已经是中文模式
        if 'Chinese (Simplified)_China.936 = zh_CN' in content and 'zh_CN = 1' in content:
            print("当前已经是中文模式!")
            return
            
        # 添加Chinese (Simplified)_China.936行
        if 'Chinese (Simplified)_China.936 = zh_CN' not in content:
            content = re.sub(
                r'(Chinese_People\'s Republic of China\.936 = zh_CN)', 
                r'\1\nChinese (Simplified)_China.936 = zh_CN', 
                content
            )
            
        # 修改zh_CN默认值
        content = re.sub(r'zh_CN = 0', 'zh_CN = 1', content)
            
        # 写回文件
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("已成功切换到中文模式!")
        print("请重启Abaqus以应用更改。")
        
    except Exception as e:
        print(f"错误: 切换到中文模式时出错: {str(e)}")
        print(traceback.format_exc())

def switch_to_english():
    """切换到英文模式"""
    if not os.path.exists(CONFIG_PATH):
        print(f"错误: 找不到配置文件: {CONFIG_PATH}")
        return
        
    try:
        # 读取文件内容
        with open(CONFIG_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.readlines()
            
        # 检查是否已经是英文模式
        content_str = ''.join(content)
        if 'Chinese (Simplified)_China.936 = zh_CN' not in content_str and 'zh_CN = 0' in content_str:
            print("当前已经是英文模式!")
            return
            
        # 移除Chinese (Simplified)_China.936行
        new_content = []
        for line in content:
            if 'Chinese (Simplified)_China.936 = zh_CN' not in line:
                new_content.append(line)
                
        # 修改zh_CN默认值
        content_str = ''.join(new_content)
        content_str = re.sub(r'zh_CN = 1', 'zh_CN = 0', content_str)
            
        # 写回文件
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(content_str)
            
        print("已成功切换到英文模式!")
        print("请重启Abaqus以应用更改。")
        
    except Exception as e:
        print(f"错误: 切换到英文模式时出错: {str(e)}")
        print(traceback.format_exc())

def manage_config_paths():
    """管理配置文件路径"""
    global CONFIG_PATH, BACKUP_PATH
    
    while True:
        print("\n配置文件路径管理")
        print("=" * 40)
        print(f"当前使用的路径: {CONFIG_PATH}")
        print("=" * 40)
        print("已保存的路径列表:")
        
        for idx, item in enumerate(PATH_LIST):
            exists = os.path.exists(item["path"])
            status = "存在" if exists else "不存在"
            current = " [当前]" if item["path"] == CONFIG_PATH else ""
            print(f"{idx+1}. {item['name']}: {item['path']} [{status}]{current}")
            
        print("\n请选择操作:")
        print("1. 切换到已保存的路径")
        print("2. 添加新路径")
        print("3. 重命名路径")
        print("4. 删除路径")
        print("5. 返回主菜单")
        
        choice = input("请选择 (1-5): ")
        
        if choice == "1":
            # 切换路径
            if not PATH_LIST:
                print("没有已保存的路径!")
                continue
                
            path_idx = input("请选择路径编号: ")
            try:
                idx = int(path_idx) - 1
                if 0 <= idx < len(PATH_LIST):
                    CONFIG_PATH = PATH_LIST[idx]["path"]
                    BACKUP_PATH = f"{CONFIG_PATH}.bak"
                    
                    if save_settings():
                        print(f"已切换到路径: {CONFIG_PATH}")
                        return
                else:
                    print("无效的选择!")
            except ValueError:
                print("请输入有效的数字!")
                
        elif choice == "2":
            # 添加新路径
            add_new_path()
            
        elif choice == "3":
            # 重命名路径
            if not PATH_LIST:
                print("没有已保存的路径!")
                continue
                
            path_idx = input("请选择要重命名的路径编号: ")
            try:
                idx = int(path_idx) - 1
                if 0 <= idx < len(PATH_LIST):
                    new_name = input(f"请输入新名称 (当前: {PATH_LIST[idx]['name']}): ")
                    if new_name:
                        PATH_LIST[idx]["name"] = new_name
                        if save_settings():
                            print(f"已重命名路径为: {new_name}")
                else:
                    print("无效的选择!")
            except ValueError:
                print("请输入有效的数字!")
                
        elif choice == "4":
            # 删除路径
            if not PATH_LIST:
                print("没有已保存的路径!")
                continue
                
            if len(PATH_LIST) == 1:
                print("不能删除唯一的路径!")
                continue
                
            path_idx = input("请选择要删除的路径编号: ")
            try:
                idx = int(path_idx) - 1
                if 0 <= idx < len(PATH_LIST):
                    if PATH_LIST[idx]["path"] == CONFIG_PATH:
                        print("不能删除当前正在使用的路径!")
                    else:
                        deleted = PATH_LIST.pop(idx)
                        if save_settings():
                            print(f"已删除路径: {deleted['name']}")
                else:
                    print("无效的选择!")
            except ValueError:
                print("请输入有效的数字!")
                
        elif choice == "5":
            # 返回主菜单
            return
        else:
            print("无效选择，请重试!")

def add_new_path():
    """添加新路径"""
    global CONFIG_PATH, BACKUP_PATH
    
    print("\n添加新路径")
    print("=" * 40)
    print("请选择添加方式:")
    print("1. 手动输入完整路径")
    print("2. 自动查找常见安装路径")
    print("3. 返回上级菜单")
    
    choice = input("请选择 (1-3): ")
    
    if choice == "1":
        new_path = input("\n请输入locale.txt文件的完整路径: ").strip()
        if not new_path:
            print("路径不能为空!")
            return
            
        exists = os.path.exists(new_path)
        status = "存在" if exists else "不存在"
        print(f"路径状态: [{status}]")
        
        if not exists:
            confirm = input(f"警告: 文件 {new_path} 不存在，是否继续? (y/n): ")
            if confirm.lower() != 'y':
                return
        
        name = input("请为此路径指定一个名称 (回车使用默认名称): ").strip()
        if not name:
            name = f"路径 {len(PATH_LIST) + 1}"
        
        if add_path_to_list(new_path, name):
            print(f"已添加新路径: {name} ({new_path})")
            
            # 询问是否切换到新路径
            switch = input("是否切换到此路径? (y/n): ")
            if switch.lower() == 'y':
                CONFIG_PATH = new_path
                BACKUP_PATH = f"{CONFIG_PATH}.bak"
                
            if save_settings():
                print("已保存路径设置")
        else:
            print("路径已存在，未添加")
        
    elif choice == "2":
        # 常见安装路径
        common_paths = [
            r"F:\SIMULIA\EstProducts\2021\win_b64\SMA\Configuration\locale.txt",
            r"C:\SIMULIA\EstProducts\2021\win_b64\SMA\Configuration\locale.txt",
            r"D:\SIMULIA\EstProducts\2021\win_b64\SMA\Configuration\locale.txt",
            r"E:\SIMULIA\EstProducts\2021\win_b64\SMA\Configuration\locale.txt",
            r"F:\SIMULIA\EstProducts\2022\win_b64\SMA\Configuration\locale.txt",
            r"C:\SIMULIA\EstProducts\2022\win_b64\SMA\Configuration\locale.txt",
            r"D:\SIMULIA\EstProducts\2022\win_b64\SMA\Configuration\locale.txt",
            r"E:\SIMULIA\EstProducts\2022\win_b64\SMA\Configuration\locale.txt",
            r"F:\SIMULIA\EstProducts\2023\win_b64\SMA\Configuration\locale.txt",
            r"C:\SIMULIA\EstProducts\2023\win_b64\SMA\Configuration\locale.txt",
            r"D:\SIMULIA\EstProducts\2023\win_b64\SMA\Configuration\locale.txt",
            r"E:\SIMULIA\EstProducts\2023\win_b64\SMA\Configuration\locale.txt",
        ]
        
        found_paths = []
        print("\n正在查找可能的配置文件...")
        
        for path in common_paths:
            if os.path.exists(path) and not path_exists_in_list(path):
                found_paths.append(path)
                print(f"{len(found_paths)}. {path} [存在]")
        
        if not found_paths:
            print("未找到任何新的有效配置文件路径!")
            
            # 尝试查找SIMULIA目录
            drives = ["C:", "D:", "E:", "F:", "G:"]
            for drive in drives:
                simulia_path = os.path.join(drive, "SIMULIA")
                if os.path.exists(simulia_path):
                    print(f"已找到SIMULIA目录: {simulia_path}")
                    print("请手动浏览该目录下的文件，找到locale.txt文件")
            
            return
        
        path_choice = input("\n请选择要添加的配置文件 (输入序号): ")
        try:
            idx = int(path_choice) - 1
            if 0 <= idx < len(found_paths):
                new_path = found_paths[idx]
                
                name = input("请为此路径指定一个名称 (回车使用默认名称): ").strip()
                if not name:
                    name = f"路径 {len(PATH_LIST) + 1}"
                
                if add_path_to_list(new_path, name):
                    print(f"已添加新路径: {name} ({new_path})")
                    
                    # 询问是否切换到新路径
                    switch = input("是否切换到此路径? (y/n): ")
                    if switch.lower() == 'y':
                        CONFIG_PATH = new_path
                        BACKUP_PATH = f"{CONFIG_PATH}.bak"
                        
                    if save_settings():
                        print("已保存路径设置")
                else:
                    print("路径已存在，未添加")
            else:
                print("无效的选择!")
        except ValueError:
            print("请输入有效的数字!")

def show_file_info():
    """显示配置文件的当前状态信息"""
    if not os.path.exists(CONFIG_PATH):
        print(f"错误: 找不到配置文件: {CONFIG_PATH}")
        return
    
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        is_chinese = 'Chinese (Simplified)_China.936 = zh_CN' in content and 'zh_CN = 1' in content
        is_english = 'zh_CN = 0' in content
        
        print(f"\n当前配置信息:")
        print(f"配置文件: {CONFIG_PATH}")
        print(f"设置文件: {SETTINGS_FILE}")
        print(f"当前语言: {'中文' if is_chinese else '英文' if is_english else '未知'}")
        print(f"已保存路径数: {len(PATH_LIST)} 个")
        
        # 显示备份信息
        if os.path.exists(BACKUP_PATH):
            print(f"备份文件: {BACKUP_PATH} (已存在)")
        else:
            print("备份文件: 不存在")
        
        print("")
    except Exception as e:
        print(f"错误: 获取文件信息时出错: {str(e)}")
        print(traceback.format_exc())

def main():
    """应用程序入口点"""
    print("程序启动...")
    
    try:
        # 加载设置
        load_settings()
        
        # 检查配置文件是否存在
        if not os.path.exists(CONFIG_PATH):
            print(f"错误: 找不到配置文件: {CONFIG_PATH}")
            print(f"请先设置正确的配置文件路径")
            manage_config_paths()
            
            # 再次检查设置后的路径
            if not os.path.exists(CONFIG_PATH):
                print(f"错误: 仍然找不到配置文件，程序将退出")
                input("按Enter键退出...")
                return
        
        # 检查管理员权限
        if not is_admin():
            print("警告: 当前程序未以管理员权限运行，可能无法修改配置文件")
            print("建议右键点击程序，选择'以管理员身份运行'")
            input("按Enter键继续...")
        
        # 首次运行时自动创建备份
        create_backup()
        
        show_file_info()
            
        while True:
            print_menu()
            choice = input("请选择操作 (1-5): ")
            
            if choice == "1":
                switch_to_chinese()
                input("按Enter键继续...")
                show_file_info()
            elif choice == "2":
                switch_to_english()
                input("按Enter键继续...")
                show_file_info()
            elif choice == "3":
                restore_backup()
                input("按Enter键继续...")
                show_file_info()
            elif choice == "4":
                manage_config_paths()
                show_file_info()
            elif choice == "5":
                print("感谢使用Abaqus语言切换工具!")
                break
            else:
                print("无效选择，请重试!")
                input("按Enter键继续...")
    except Exception as e:
        print(f"程序运行时发生错误: {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("程序发生意外错误:")
        print(traceback.format_exc())
        input("按Enter键退出...") 