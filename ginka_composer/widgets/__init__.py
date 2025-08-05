#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义控件模块
包含预览窗口、可预览的复选框和背景项目等控件
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QCheckBox, QFrame, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QRect
from PyQt6.QtGui import QFont, QPixmap, QImage

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class LayerPreviewWindow(QWidget):
    """图层预览窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setFixedSize(300, 400)
        
        # 设置样式
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border: 2px solid #007bff;
                border-radius: 8px;
            }
            QLabel {
                color: #ffffff;
                background: transparent;
                padding: 8px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # 图层名称标签
        self.name_label = QLabel()
        self.name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label)
        
        # 图像预览标签
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(280, 300)
        self.image_label.setStyleSheet("border: 1px solid #555555; background-color: #3c3c3c;")
        layout.addWidget(self.image_label)
        
        # 信息标签
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("font-size: 9px; color: #cccccc;")
        layout.addWidget(self.info_label)
    
    def showPreview(self, layer_name, image_path, layer_info=None):
        """显示图层预览"""
        self.name_label.setText(layer_name)
        
        # 加载并显示图像
        if os.path.exists(image_path):
            try:
                # 使用PIL加载图像以支持更多格式
                pil_image = Image.open(image_path)
                if pil_image.mode != 'RGBA':
                    pil_image = pil_image.convert('RGBA')
                
                # 计算缩放比例以适应预览窗口
                img_width, img_height = pil_image.size
                max_width, max_height = 270, 280
                
                scale = min(max_width / img_width, max_height / img_height, 1.0)
                if scale < 1.0:
                    new_width = int(img_width * scale)
                    new_height = int(img_height * scale)
                    pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 转换为QPixmap
                data = pil_image.tobytes('raw', 'RGBA')
                width, height = pil_image.size
                qimage = QImage(data, width, height, QImage.Format.Format_RGBA8888)
                pixmap = QPixmap.fromImage(qimage)
                
                self.image_label.setPixmap(pixmap)
                
                # 设置信息文本
                if layer_info:
                    info_text = f"尺寸: {layer_info.get('size', [0, 0])[0]}×{layer_info.get('size', [0, 0])[1]}\n"
                    info_text += f"ID: {layer_info.get('layer_id', 'N/A')}"
                    self.info_label.setText(info_text)
                else:
                    self.info_label.setText(f"尺寸: {img_width}×{img_height}")
                
            except Exception as e:
                print(f"预览图像加载失败: {e}")
                self.image_label.setText("预览加载失败")
                self.info_label.setText("图像文件损坏")
        else:
            self.image_label.setText("图像文件不存在")
            self.info_label.setText(f"路径: {image_path}")
    
    def showAtPosition(self, global_pos):
        """在指定位置显示预览窗口"""
        # 获取屏幕尺寸
        screen = QApplication.primaryScreen()
        if screen:
            screen_rect = screen.geometry()
        else:
            screen_rect = QRect(0, 0, 1920, 1080)  # 默认尺寸
        
        # 计算窗口位置，确保不超出屏幕边界
        x = global_pos.x() + 20  # 鼠标右侧
        y = global_pos.y() - 200  # 鼠标上方
        
        # 边界检查
        if x + self.width() > screen_rect.right():
            x = global_pos.x() - self.width() - 20  # 鼠标左侧
        if y < screen_rect.top():
            y = global_pos.y() + 20  # 鼠标下方
        if y + self.height() > screen_rect.bottom():
            y = screen_rect.bottom() - self.height()
        
        self.move(x, y)
        self.show()
        self.raise_()


class PreviewableCheckBox(QCheckBox):
    """支持预览的复选框"""
    previewRequested = pyqtSignal(object, QPoint)  # 发送图层信息和鼠标位置
    
    def __init__(self, text, layer_info=None):
        super().__init__(text)
        self.layer_info = layer_info
        self.setMouseTracking(True)
    
    def enterEvent(self, event):
        """鼠标进入事件"""
        super().enterEvent(event)
        if self.layer_info:
            global_pos = self.mapToGlobal(QPoint(self.width(), 0))
            self.previewRequested.emit(self.layer_info, global_pos)
    
    def leaveEvent(self, event):
        """鼠标离开事件"""
        super().leaveEvent(event)
        # 预览窗口会通过定时器自动隐藏


class PreviewableBackgroundItem(QFrame):
    """支持预览的背景项目"""
    backgroundSelected = pyqtSignal(str)  # 发送背景文件名
    previewRequested = pyqtSignal(str, QPoint)  # 发送背景文件名和鼠标位置
    
    def __init__(self, bg_filename, bg_path):
        super().__init__()
        self.bg_filename = bg_filename
        self.bg_path = bg_path
        self.setMouseTracking(True)
        self.setupUI()
        
    def setupUI(self):
        """设置UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        
        # 选择按钮
        self.select_btn = QPushButton("选择")
        self.select_btn.setMaximumWidth(60)
        self.select_btn.clicked.connect(lambda: self.backgroundSelected.emit(self.bg_filename))
        layout.addWidget(self.select_btn)
        
        # 背景名称标签
        name_label = QLabel(self.bg_filename)
        name_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        layout.addWidget(name_label)
        
        layout.addStretch()
        
        # 设置框架样式
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #555555;
                border-radius: 4px;
                background-color: #4a4a4a;
                margin: 2px;
            }
            QFrame:hover {
                border: 2px solid #007bff;
                background-color: #3c3c3c;
            }
        """)
    
    def enterEvent(self, event):
        """鼠标进入事件"""
        super().enterEvent(event)
        global_pos = self.mapToGlobal(QPoint(self.width(), 0))
        self.previewRequested.emit(self.bg_filename, global_pos)
    
    def leaveEvent(self, event):
        """鼠标离开事件"""
        super().leaveEvent(event)
        # 预览窗口会通过定时器自动隐藏
