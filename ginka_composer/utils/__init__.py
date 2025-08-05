#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具模块
包含样式管理、图像处理等工具函数
"""

import os
from pathlib import Path
from PyQt6.QtGui import QPixmap, QImage

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def get_modern_style():
    """获取现代化样式表"""
    return """
    /* 主窗口样式 */
    QMainWindow {
        background-color: #2b2b2b;
        color: #ffffff;
    }

    /* 标签页样式 */
    QTabWidget::pane {
        border: 1px solid #555555;
        background-color: #3c3c3c;
    }

    QTabBar::tab {
        background-color: #4a4a4a;
        color: #ffffff;
        padding: 8px 16px;
        margin-right: 2px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
    }

    QTabBar::tab:selected {
        background-color: #007bff;
    }

    QTabBar::tab:hover {
        background-color: #0056b3;
    }

    /* 分组框样式 */
    QGroupBox {
        font-weight: bold;
        border: 2px solid #555555;
        border-radius: 8px;
        margin-top: 1ex;
        color: #ffffff;
        background-color: #3c3c3c;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #007bff;
        font-size: 12px;
    }

    /* 按钮样式 */
    QPushButton {
        background-color: #007bff;
        border: none;
        color: white;
        padding: 8px 16px;
        font-size: 12px;
        border-radius: 6px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #0056b3;
    }

    QPushButton:pressed {
        background-color: #004085;
    }

    QPushButton:disabled {
        background-color: #6c757d;
        color: #adb5bd;
    }

    /* 下拉框样式 */
    QComboBox {
        border: 2px solid #555555;
        border-radius: 6px;
        padding: 6px;
        background-color: #4a4a4a;
        color: #ffffff;
        font-weight: bold;
    }

    QComboBox:hover {
        border-color: #007bff;
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #555555;
        background-color: #555555;
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
    }

    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #ffffff;
    }

    QComboBox QAbstractItemView {
        border: 2px solid #007bff;
        background-color: #4a4a4a;
        color: #ffffff;
        selection-background-color: #007bff;
    }

    /* 滑块样式 */
    QSlider::groove:horizontal {
        border: 1px solid #555555;
        height: 8px;
        background: #4a4a4a;
        margin: 2px 0;
        border-radius: 4px;
    }

    QSlider::handle:horizontal {
        background: #007bff;
        border: 1px solid #0056b3;
        width: 18px;
        margin: -2px 0;
        border-radius: 9px;
    }

    QSlider::handle:horizontal:hover {
        background: #0056b3;
    }

    /* 数值输入框样式 */
    QSpinBox, QDoubleSpinBox {
        border: 2px solid #555555;
        border-radius: 4px;
        padding: 4px;
        background-color: #4a4a4a;
        color: #ffffff;
        font-weight: bold;
    }

    QSpinBox:hover, QDoubleSpinBox:hover {
        border-color: #007bff;
    }

    QSpinBox::up-button, QDoubleSpinBox::up-button {
        background-color: #555555;
        border-left: 1px solid #666666;
        border-bottom: 1px solid #666666;
        border-top-right-radius: 4px;
    }

    QSpinBox::down-button, QDoubleSpinBox::down-button {
        background-color: #555555;
        border-left: 1px solid #666666;
        border-top: 1px solid #666666;
        border-bottom-right-radius: 4px;
    }

    QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
    QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
        background-color: #007bff;
    }

    /* 列表样式 */
    QListWidget {
        border: 2px solid #555555;
        border-radius: 6px;
        background-color: #4a4a4a;
        color: #ffffff;
        padding: 4px;
    }

    QListWidget::item {
        padding: 6px;
        border-bottom: 1px solid #555555;
        border-radius: 3px;
        margin: 1px;
    }

    QListWidget::item:selected {
        background-color: #007bff;
        color: #ffffff;
    }

    QListWidget::item:hover {
        background-color: #0056b3;
    }

    /* 复选框样式 */
    QCheckBox {
        color: #ffffff;
        font-weight: bold;
    }

    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #555555;
        border-radius: 3px;
        background-color: #4a4a4a;
    }

    QCheckBox::indicator:checked {
        background-color: #007bff;
        border-color: #0056b3;
    }

    QCheckBox::indicator:hover {
        border-color: #007bff;
    }

    /* 单选按钮样式 */
    QRadioButton {
        color: #ffffff;
        font-weight: bold;
    }

    QRadioButton::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #555555;
        border-radius: 9px;
        background-color: #4a4a4a;
    }

    QRadioButton::indicator:checked {
        background-color: #007bff;
        border-color: #0056b3;
    }

    QRadioButton::indicator:hover {
        border-color: #007bff;
    }

    /* 滚动区域样式 */
    QScrollArea {
        border: 1px solid #555555;
        border-radius: 6px;
        background-color: #4a4a4a;
    }

    QScrollBar:vertical {
        background-color: #4a4a4a;
        width: 12px;
        border-radius: 6px;
    }

    QScrollBar::handle:vertical {
        background-color: #007bff;
        border-radius: 6px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: #0056b3;
    }

    /* 标签样式 */
    QLabel {
        color: #ffffff;
    }

    /* 工具栏样式 */
    QToolBar {
        background-color: #3c3c3c;
        border: none;
        spacing: 8px;
    }

    QToolBar QToolButton {
        background-color: #4a4a4a;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 6px;
        color: #ffffff;
    }

    QToolBar QToolButton:hover {
        background-color: #007bff;
        border-color: #0056b3;
    }

    /* 状态栏样式 */
    QStatusBar {
        background-color: #3c3c3c;
        color: #ffffff;
        border-top: 1px solid #555555;
    }

    /* 进度条样式 */
    QProgressBar {
        border: 2px solid #555555;
        border-radius: 6px;
        text-align: center;
        color: #ffffff;
        background-color: #4a4a4a;
        font-weight: bold;
    }

    QProgressBar::chunk {
        background-color: #007bff;
        border-radius: 4px;
    }

    /* 分割器样式 */
    QSplitter::handle {
        background-color: #555555;
    }

    QSplitter::handle:horizontal {
        width: 2px;
    }

    QSplitter::handle:vertical {
        height: 2px;
    }

    QSplitter::handle:pressed {
        background-color: #007bff;
    }
    """


def organize_layers_by_type(layers):
    """根据图层名称智能分组"""
    groups = {
        '眉毛': [],
        '眼睛': [],
        '嘴巴': [],
        '脸颊': [],
        '身体': [],
        '服装': [],
        '其他': []
    }
    
    for layer in layers:
        name = layer['name']
        if '眉' in name:
            groups['眉毛'].append(layer)
        elif '目' in name or '眼' in name:
            groups['眼睛'].append(layer)
        elif '口' in name or '嘴' in name:
            groups['嘴巴'].append(layer)
        elif '頬' in name or '脸' in name:
            groups['脸颊'].append(layer)
        elif 'base' in name or '身' in name:
            groups['身体'].append(layer)
        elif any(h in name for h in ['h1', 'h2', 'h3', 'h4', '装', '服']):
            groups['服装'].append(layer)
        else:
            groups['其他'].append(layer)
    
    # 移除空分组
    return {k: v for k, v in groups.items() if v}


def pil_to_qpixmap_high_quality(pil_image, scale_factor: float = 1.0):
    """高质量PIL图像转QPixmap - 优化版本"""
    try:
        # 确保RGBA模式
        if pil_image.mode != 'RGBA':
            pil_image = pil_image.convert('RGBA')
        
        # 如果需要缩放，使用最高质量算法
        if scale_factor != 1.0:
            new_width = int(pil_image.size[0] * scale_factor)
            new_height = int(pil_image.size[1] * scale_factor)
            
            # 对于放大使用LANCZOS，对于缩小使用不同算法以获得最佳效果
            if scale_factor > 1.0:
                # 放大 - 使用LANCZOS获得平滑结果
                pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                # 缩小 - 使用BICUBIC获得锐利结果
                pil_image = pil_image.resize((new_width, new_height), Image.Resampling.BICUBIC)
        
        # 转换为QPixmap
        data = pil_image.tobytes('raw', 'RGBA')
        width, height = pil_image.size
        
        # 创建QImage时使用最佳格式
        qimage = QImage(data, width, height, QImage.Format.Format_RGBA8888)
        
        # 转换为QPixmap时启用最高质量变换
        pixmap = QPixmap.fromImage(qimage)
        
        return pixmap
        
    except Exception as e:
        print(f"高质量图像转换失败: {e}")
        return None


class SimpleAlignmentSystem:
    """简单的对齐系统占位类"""
    
    def __init__(self):
        self.layer_configs = {}
    
    def detect_layer_type(self, file_path, layer_name):
        """检测图层类型"""
        # 简单的类型检测逻辑
        if "眼" in layer_name or "eye" in layer_name.lower():
            return "eyes"
        elif "口" in layer_name or "mouth" in layer_name.lower():
            return "mouth"
        elif "眉" in layer_name or "brow" in layer_name.lower():
            return "eyebrows"
        else:
            return "other"
    
    def get_alignment_position(self, character_name, character_size, layer_type):
        """获取对齐位置"""
        # 返回默认位置 (x, y)
        return (0, 0)
    
    def get_layer_z_order(self, layer_type):
        """获取图层Z顺序"""
        return 0
    
    def get_layer_category(self, layer_type):
        """获取图层分类"""
        return "default"


def get_alignment_system(base_path):
    """获取对齐系统（占位实现）"""
    return SimpleAlignmentSystem()
