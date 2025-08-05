#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GINKA 立绘搭配软件 - 主程序入口
模块化的PyQt6版本
"""

import sys
import os
import webbrowser
from PyQt6.QtWidgets import QApplication, QMessageBox
from ginka_composer.ui import ModernCharacterComposer


def open_live2d_tools():
    """打开Live2D工具套件"""
    try:
        # 获取当前目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Live2D工具页面路径
        tools_paths = {
            'demo': os.path.join(current_dir, 'live2d_projects', 'tgina01_l', 'web_preview', 'demo.html'),
            'moc3_guide': os.path.join(current_dir, 'live2d_projects', 'tgina01_l', 'web_preview', 'moc3_guide.html'),
            'viewer': os.path.join(current_dir, 'live2d_projects', 'tgina01_l', 'web_preview', 'live2d_viewer.html'),
            'tools_guide': os.path.join(current_dir, 'tools', 'README.md')
        }
        
        # 检查文件是否存在
        if os.path.exists(tools_paths['demo']):
            # 打开演示页面
            webbrowser.open(f'file:///{tools_paths["demo"].replace(os.sep, "/")}')
            print("🎭 Live2D工具套件已打开！")
            return True
        else:
            print("❌ Live2D工具文件未找到，请先运行Live2D转换工具")
            return False
            
    except Exception as e:
        print(f"❌ 打开Live2D工具失败: {e}")
        return False


def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == '--live2d' or sys.argv[1] == '-l':
            print("🚀 启动Live2D工具套件...")
            open_live2d_tools()
            return
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("""
🎭 GINKA 立绘搭配软件 - 使用帮助

用法:
  python main.py              # 启动角色编辑器
  python main.py --live2d     # 打开Live2D工具套件  
  python main.py -l           # 打开Live2D工具套件(简写)
  python main.py --help       # 显示此帮助信息
  python main.py -h           # 显示此帮助信息(简写)

功能:
  • 现代化的角色编辑器 (PyQt6)
  • Live2D模型转换和预览
  • Web端模型查看和交互
  • 完整的项目管理工具

Live2D工具包括:
  • 模型查看器 - 实时预览和交互
  • 文件加载器 - 支持拖放.moc3文件
  • 项目管理器 - 完整的文件管理
  • 制作指南 - 详细的.moc3创建教程
            """)
            return
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("GINKA 立绘搭配软件")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("GINKA Team")
    
    try:
        # 创建主窗口
        window = ModernCharacterComposer()
        window.show()
        
        # 运行应用程序
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
