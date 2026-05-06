#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖检查脚本
"""

import sys
import subprocess
import pkg_resources

def check_dependencies():
    """检查依赖包是否已安装"""
    required_packages = [
        'flask',
        'paddleocr',
        'opencv-python',
        'Pillow',
        'requests',
        'python-dotenv',
        'numpy'
    ]

    missing_packages = []
    installed_packages = []

    print("🔍 检查依赖包...")
    print("=" * 40)

    for package in required_packages:
        try:
            pkg_resources.get_distribution(package)
            print(f"✅ {package} 已安装")
            installed_packages.append(package)
        except pkg_resources.DistributionNotFound:
            print(f"❌ {package} 未安装")
            missing_packages.append(package)

    print("=" * 40)

    if missing_packages:
        print(f"❌ 缺少 {len(missing_packages)} 个依赖包")
        print("\n请运行以下命令安装依赖：")
        print("pip install -r requirements.txt")
        return False
    else:
        print("✅ 所有依赖包已安装")
        return True

def test_imports():
    """测试模块导入"""
    print("\n🧪 测试模块导入...")
    print("=" * 40)

    modules_to_test = [
        ('flask', 'Flask'),
        ('paddleocr', 'PaddleOCR'),
        ('cv2', 'cv2'),
        ('PIL', 'Image'),
        ('requests', 'requests'),
        ('numpy', 'numpy'),
    ]

    all_success = True

    for module_name, import_name in modules_to_test:
        try:
            if import_name:
                exec(f"import {import_name}")
            else:
                exec(f"import {module_name}")
            print(f"✅ {module_name} 导入成功")
        except ImportError as e:
            print(f"❌ {module_name} 导入失败: {e}")
            all_success = False

    print("=" * 40)
    return all_success

def test_system_components():
    """测试系统组件"""
    print("\n🔧 测试系统组件...")
    print("=" * 40)

    try:
        # 测试配置加载
        sys.path.append('.')
        from config import Config
        print("✅ 配置模块加载成功")

        # 测试目录存在
        import os
        if os.path.exists(Config.UPLOAD_FOLDER):
            print("✅ 上传目录存在")
        else:
            print("❌ 上传目录不存在")
            return False

        if os.path.exists(Config.RESULT_FOLDER):
            print("✅ 结果目录存在")
        else:
            print("❌ 结果目录不存在")
            return False

        return True

    except Exception as e:
        print(f"❌ 系统组件测试失败: {e}")
        return False

def main():
    """主函数"""
    print("数学试卷批改系统依赖检查")
    print("=" * 50)

    # 检查Python版本
    python_version = sys.version_info
    if python_version < (3, 8):
        print(f"❌ Python版本过低: {python_version.major}.{python_version.minor}")
        print("需要Python 3.8或更高版本")
        return False
    else:
        print(f"✅ Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")

    # 检查依赖
    deps_ok = check_dependencies()
    if not deps_ok:
        return False

    # 测试导入
    imports_ok = test_imports()
    if not imports_ok:
        return False

    # 测试系统组件
    components_ok = test_system_components()
    if not components_ok:
        return False

    print("\n所有检查通过！系统可以正常运行")
    print("\n启动命令：")
    print("python app.py")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)