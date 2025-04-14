# Abaqus语言切换工具

[![版本](https://img.shields.io/badge/版本-1.0.0-blue.svg)](https://github.com/LuckYang1/abaqus_language_switch/releases/tag/v1.0.0)
[![Abaqus](https://img.shields.io/badge/Abaqus-2016~2025-orange.svg)](https://www.3ds.com/products-services/simulia/products/abaqus/)
[![许可证](https://img.shields.io/badge/许可证-MIT-green.svg)](LICENSE)

> For English version of this document, please click [here](README_EN.md)

## 项目介绍

这是一个用于切换Abaqus界面语言（中英文）的小工具，无需修改系统区域设置，便捷快速。

## 下载

您可以通过以下方式获取本工具：

- **[下载已编译的可执行文件](https://github.com/LuckYang1/abaqus_language_switch/releases/latest)** - 无需Python环境，直接运行
- 或者按照下方说明获取源代码并自行运行/编译

## 获取代码

### 使用Git克隆

如果您已安装Git，可以通过以下命令克隆仓库：

```
git clone https://github.com/LuckYang1/abaqus_language_switch.git
cd abaqus_language_switch
```

### 直接下载

您也可以通过[GitHub下载页面](https://github.com/LuckYang1/abaqus_language_switch/archive/refs/heads/main.zip)直接下载ZIP文件。

## 直接运行源代码

1. 确保您的系统安装了Python 3.6或更高版本
2. 将`abaqus_language_switch_exe.py`文件下载到本地
3. 右键点击该文件，选择"以管理员身份运行"（或者通过命令行以管理员身份运行）
   ```
   python abaqus_language_switch_exe.py
   ```
4. 按照界面提示操作即可

注意：直接运行Python脚本同样需要管理员权限，因为需要修改Abaqus安装目录下的配置文件。

## 关于配置文件

### locale.txt

本工具主要修改的是Abaqus的语言配置文件`locale.txt`。此文件是Abaqus的原始语言配置文件，通常位于以下路径：

```
C:\SIMULIA\EstProducts\2021\win_b64\SMA\Configuration\locale.txt
```

路径可能因Abaqus版本不同而略有差异。该文件包含了Abaqus界面语言的配置信息，主要控制了软件界面显示的语言（英文、中文或日文）。

工具通过修改配置文件中的以下设置实现语言切换：
- `[Alias]`部分：定义系统区域设置与Abaqus使用语言的映射关系
- `[Default]`部分：设置是否默认使用本地语言（`1 = 是`，`0 = 否`）

本项目中包含的`locale_en.txt`是英文模式的参考配置文件，可用于恢复英文界面。

### abaqus_lang_settings.json

工具在用户目录下创建并使用一个设置文件`abaqus_lang_settings.json`，位于：

```
C:\Users\你的用户名\AbaqusLangSwitcher\abaqus_lang_settings.json
```

此文件存储了以下信息：
- `current_path`：当前使用的Abaqus配置文件路径
- `path_list`：用户添加的所有Abaqus安装路径，包含路径名称、完整路径和添加时间

当添加或切换Abaqus安装路径时，工具会自动更新此文件。如果您有多个Abaqus版本或安装位置，此功能允许您在不同配置之间轻松切换。

## 可打包为可执行文件

### 前提条件

1. 电脑上已安装Python 3.6或更高版本
2. 网络连接正常（用于安装打包工具）

### 打包步骤

1. 首先安装PyInstaller打包工具:
   ```
   pip install pyinstaller
   ```

2. 打开命令提示符(cmd)，切换到脚本所在目录:
   ```
   cd 文件所在路径
   ```

3. 基本打包命令:
   ```
   pyinstaller --onefile --console abaqus_language_switch_exe.py
   ```
   带自定义图标的打包命令:
   ```
   pyinstaller --onefile --console --icon=icon.ico abaqus_language_switch_exe.py
   ```
   如需使用自定义图标，请确保在脚本同目录下有`icon.ico`文件，或修改上述命令中的图标路径。

4. 等待打包完成，这可能需要几分钟时间

5. 打包完成后，在当前目录下的`dist`文件夹中可以找到生成的exe文件
   (`dist/abaqus_language_switch_exe.exe`)

6. 将生成的exe文件复制到任意位置即可使用

## 使用说明

1. 由于程序需要修改系统文件，请右键点击exe文件或Python脚本，选择"以管理员身份运行"

2. 首次运行时，程序会自动创建Abaqus配置文件的备份

3. 按照界面提示选择相应操作:
   - 选项1: 切换到中文模式
   - 选项2: 切换到英文模式
   - 选项3: 恢复初始备份
   - 选项4: 管理配置文件路径
   - 选项5: 退出程序

## 注意事项

1. 如果您的Abaqus安装路径与脚本中默认路径不同，可以通过程序中的"管理配置文件路径"选项添加新路径

2. 生成的exe文件可直接在Windows系统上运行，无需安装Python或其他依赖

3. 如果运行时出现"拒绝访问"等错误，请确保以管理员身份运行程序

4. 备份文件保存在与配置文件相同的目录下，文件名为`locale.txt.bak`

## 扩展其他语言支持

当前工具支持中英文切换，如果您需要支持其他语言（如日语），可以修改`abaqus_language_switch_exe.py`文件来实现。主要修改点如下：

1. 在`switch_to_chinese()`函数的基础上，添加类似的`switch_to_japanese()`函数
2. 修改相应的正则表达式，找到并更新日语相关的配置行
3. 在主菜单`print_menu()`函数中添加日语切换选项

例如，要添加日语支持，可以参考以下代码片段：

```python
def switch_to_japanese():
    """切换到日语模式"""
    if not os.path.exists(CONFIG_PATH):
        print(f"错误: 找不到配置文件: {CONFIG_PATH}")
        return
        
    try:
        # 读取文件内容
        with open(CONFIG_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # 检查是否已经是日语模式
        if 'Japanese_Japan.932 = ja_JP' in content and 'ja_JP = 1' in content:
            print("当前已经是日语模式!")
            return
            
        # 修改ja_JP默认值
        content = re.sub(r'ja_JP = 0', 'ja_JP = 1', content)
            
        # 写回文件
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("已成功切换到日语模式!")
        print("请重启Abaqus以应用更改。")
        
    except Exception as e:
        print(f"错误: 切换到日语模式时出错: {str(e)}")
        print(traceback.format_exc())
```

参考`locale_en.txt`文件中的配置信息，可以了解各语言的设置方式，从而扩展支持更多语言。

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。 