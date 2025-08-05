#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口模块
包含主窗口类和相关业务逻辑
"""

import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
    QTabWidget, QProgressBar, QMessageBox, QFileDialog, 
    QListWidget, QListWidgetItem, QApplication, QLabel,
    QStatusBar, QFrame, QGroupBox, QPushButton, QButtonGroup, QRadioButton, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPainter, QPixmap

from ..models import CharacterInstance, ImageLoader
from ..widgets import LayerPreviewWindow, PreviewableCheckBox, PreviewableBackgroundItem
from ..widgets.canvas import Canvas
from ..utils import get_modern_style, organize_layers_by_type, pil_to_qpixmap_high_quality, get_alignment_system
from .tabs import SceneTab, CharacterTab, LayerTab

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class ModernCharacterComposer(QMainWindow):
    """现代化的角色立绘搭配软件主窗口"""
    
    def __init__(self):
        super().__init__()
        self.character_data = {}
        self.character_instances = {}
        self.current_instance = None
        self.next_z_order = 0  # 用于分配新角色的层级
        self.image_loader = ImageLoader()
        self._updating_controls = False  # 防止控件更新时触发变换事件
        
        # 创建预览窗口
        self.preview_window = LayerPreviewWindow()
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self.hidePreview)
        self.preview_timer.setSingleShot(True)
        
        self.setupUI()
        self.setupConnections()
        self.loadCharacterData()
        self.loadBackgroundList()
        self.setStyleSheet(get_modern_style())
        
    def setupUI(self):
        """设置用户界面"""
        self.setWindowTitle("GINKA 立绘搭配软件 - 现代版")
        self.setGeometry(100, 100, 1600, 1000)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧控制面板
        self.setupLeftPanel(splitter)
        
        # 右侧画布区域
        self.setupCanvasArea(splitter)
        
        # 设置分割器比例 - 左侧控制面板更窄，右侧画布更大
        splitter.setSizes([350, 1250])
        
        # 创建状态栏
        self.setupStatusBar()
    
    def setupLeftPanel(self, parent):
        """设置左侧控制面板"""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # 创建标签页
        tab_widget = QTabWidget()
        left_layout.addWidget(tab_widget)
        
        # 场景标签页
        self.scene_tab = SceneTab()
        tab_widget.addTab(self.scene_tab, "🎬 场景")
        
        # 角色标签页
        self.character_tab = CharacterTab()
        tab_widget.addTab(self.character_tab, "👥 角色")
        
        # 图层标签页
        self.layer_tab = LayerTab()
        tab_widget.addTab(self.layer_tab, "🎨 图层")
        
        parent.addWidget(left_widget)
    
    def setupCanvasArea(self, parent):
        """设置画布区域"""
        canvas_widget = QWidget()
        canvas_layout = QVBoxLayout(canvas_widget)
        canvas_layout.setContentsMargins(5, 5, 5, 5)  # 减少边距
        
        # 顶部工具栏
        toolbar_layout = QHBoxLayout()
        
        # 画布标题和缩放信息
        title_label = QLabel("预览画布")
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        toolbar_layout.addWidget(title_label)
        
        # 缩放显示
        self.zoom_label = QLabel("缩放: 100%")
        toolbar_layout.addWidget(self.zoom_label)
        
        toolbar_layout.addStretch()
        
        # 画布控制按钮组
        
        # 交互模式
        mode_label = QLabel("模式:")
        toolbar_layout.addWidget(mode_label)
        
        self.canvas_mode_group = QButtonGroup()
        self.canvas_mode_radio = QRadioButton("拖拽画布")
        self.character_mode_radio = QRadioButton("移动角色")
        self.canvas_mode_radio.setChecked(True)
        
        self.canvas_mode_group.addButton(self.canvas_mode_radio)
        self.canvas_mode_group.addButton(self.character_mode_radio)
        
        toolbar_layout.addWidget(self.canvas_mode_radio)
        toolbar_layout.addWidget(self.character_mode_radio)
        
        # 分隔线
        separator = QFrame()
        separator.setFrameStyle(QFrame.Shape.VLine | QFrame.Shadow.Sunken)
        toolbar_layout.addWidget(separator)
        
        # 画布操作按钮
        self.fit_canvas_btn = QPushButton("适应画布")
        self.reset_view_btn = QPushButton("重置视图")
        self.fit_canvas_btn.setMaximumWidth(80)
        self.reset_view_btn.setMaximumWidth(80)
        toolbar_layout.addWidget(self.fit_canvas_btn)
        toolbar_layout.addWidget(self.reset_view_btn)
        
        # 分隔线
        separator2 = QFrame()
        separator2.setFrameStyle(QFrame.Shape.VLine | QFrame.Shadow.Sunken)
        toolbar_layout.addWidget(separator2)
        
        # 进度条（用于显示加载进度）
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        toolbar_layout.addWidget(self.progress_bar)
        
        canvas_layout.addLayout(toolbar_layout)
        
        # 画布 - 占据剩余全部空间
        self.canvas = Canvas()
        self.canvas.setMinimumSize(600, 400)  # 设置最小尺寸
        canvas_layout.addWidget(self.canvas, 1)  # stretch=1 让画布占据全部剩余空间
        
        parent.addWidget(canvas_widget)
    
    def setupStatusBar(self):
        """设置状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
    
    def setupConnections(self):
        """设置信号连接"""
        # 画布工具栏连接
        self.canvas_mode_radio.toggled.connect(lambda checked: self.canvas.setDragMode('canvas' if checked else 'character'))
        self.fit_canvas_btn.clicked.connect(self.fitCanvas)
        self.reset_view_btn.clicked.connect(self.resetView)
        
        # 场景标签页连接
        self.scene_tab.backgroundComboChanged.connect(self.onBackgroundChanged)
        self.scene_tab.loadBackgroundRequested.connect(self.loadBackground)
        self.scene_tab.clearBackgroundRequested.connect(self.clearBackground)
        # 注释掉原来的画布控制连接，因为已经移到工具栏
        # self.scene_tab.canvasModeChanged.connect(self.canvas.setDragMode)
        # self.scene_tab.fitCanvasRequested.connect(self.fitCanvas)
        # self.scene_tab.resetViewRequested.connect(self.resetView)
        self.scene_tab.exportImageRequested.connect(self.exportImage)
        self.scene_tab.exportImageHDRequested.connect(self.exportImageHD)
        self.scene_tab.saveSceneRequested.connect(self.saveScene)
        self.scene_tab.loadSceneRequested.connect(self.loadScene)
        
        # 角色标签页连接
        self.character_tab.addCharacterRequested.connect(self.addCharacterInstance)
        self.character_tab.duplicateCharacterRequested.connect(self.duplicateCharacterInstance)
        self.character_tab.removeCharacterRequested.connect(self.removeCharacterInstance)
        self.character_tab.clearAllCharactersRequested.connect(self.clearAllCharacters)
        self.character_tab.instanceSelected.connect(self.onInstanceSelected)
        self.character_tab.transformChanged.connect(self.onTransformChanged)
        self.character_tab.resetTransformRequested.connect(self.resetTransform)
        self.character_tab.moveCharacterForwardRequested.connect(self.moveCharacterForward)
        self.character_tab.moveCharacterBackwardRequested.connect(self.moveCharacterBackward)
        self.character_tab.moveCharacterToFrontRequested.connect(self.moveCharacterToFront)
        self.character_tab.moveCharacterToBackRequested.connect(self.moveCharacterToBack)
        # 注释掉不存在的信号连接
        # self.character_tab.importCustomLayerRequested.connect(self.onImportCustomLayerRequested)
        
        # 图层标签页连接
        self.layer_tab.layerToggled.connect(self.toggleLayer)
        self.layer_tab.moveLayerUpRequested.connect(self.moveLayerUp)
        self.layer_tab.moveLayerDownRequested.connect(self.moveLayerDown)
        self.layer_tab.moveLayerToTopRequested.connect(self.moveLayerToTop)
        self.layer_tab.moveLayerToBottomRequested.connect(self.moveLayerToBottom)
        
        # 画布连接
        self.canvas.characterSelected.connect(self.onCanvasCharacterSelected)
        self.canvas.characterTransformChanged.connect(self.onCanvasCharacterTransformChanged)
        
        # 图像加载连接
        self.image_loader.imageLoaded.connect(self.onImageLoaded)
        self.image_loader.loadProgress.connect(self.onLoadProgress)
        
        # 缩放同步连接
        self.character_tab.scale_slider.valueChanged.connect(
            lambda v: self.character_tab.scale_spinbox.setValue(v/100) if not self._updating_controls else None
        )
        self.character_tab.scale_spinbox.valueChanged.connect(
            lambda v: self.character_tab.scale_slider.setValue(int(v*100)) if not self._updating_controls else None
        )
    
    def loadCharacterData(self):
        """加载角色数据"""
        try:
            with open('character_analysis.json', 'r', encoding='utf-8') as f:
                self.character_data = json.load(f)
            
            character_names = list(self.character_data.keys())
            self.character_tab.new_character_combo.addItems(character_names)
            
            self.status_bar.showMessage(f"加载了 {len(character_names)} 个角色")
            
        except FileNotFoundError:
            QMessageBox.critical(self, "错误", "未找到角色数据文件 character_analysis.json")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载角色数据时出错: {e}")
    
    def loadBackgroundList(self):
        """加载背景图片列表"""
        bg_files = []
        bg_path = Path("bgimage")
        
        if bg_path.exists():
            for ext in ['*.png', '*.jpg', '*.jpeg']:
                bg_files.extend([f.name for f in bg_path.glob(ext)])
        
        # 填充下拉框
        self.scene_tab.background_combo.addItems(sorted(bg_files))
        
        # 填充预览区域
        self.updateBackgroundPreviewArea(sorted(bg_files))
    
    def updateBackgroundPreviewArea(self, bg_files):
        """更新背景预览区域"""
        # 清空现有控件
        for i in reversed(range(self.scene_tab.bg_scroll_layout.count())):
            item = self.scene_tab.bg_scroll_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None)
        
        # 添加背景项目
        for bg_file in bg_files:
            bg_path = Path("bgimage") / bg_file
            if bg_path.exists():
                bg_item = PreviewableBackgroundItem(bg_file, str(bg_path))
                bg_item.backgroundSelected.connect(self.onBackgroundSelectedFromPreview)
                bg_item.previewRequested.connect(self.showBackgroundPreview)
                self.scene_tab.bg_scroll_layout.addWidget(bg_item)
        
        self.scene_tab.bg_scroll_layout.addStretch()
    
    def onBackgroundChanged(self):
        """背景改变处理"""
        self.loadBackground()
    
    def loadBackground(self):
        """加载背景"""
        bg_file = self.scene_tab.background_combo.currentText()
        if not bg_file:
            return
        
        bg_path = Path("bgimage") / bg_file
        if bg_path.exists():
            self.canvas.setBackgroundImage(str(bg_path))
            self.status_bar.showMessage(f"加载背景: {bg_file}")
        else:
            QMessageBox.warning(self, "警告", f"背景文件不存在: {bg_path}")
    
    def clearBackground(self):
        """清除背景"""
        self.canvas.clearBackground()
        self.scene_tab.background_combo.setCurrentIndex(-1)
        self.status_bar.showMessage("背景已清除")
    
    def showBackgroundPreview(self, bg_filename, global_pos):
        """显示背景预览"""
        # 构建背景图像文件路径
        bg_path = Path("bgimage") / bg_filename
        
        # 显示预览
        self.preview_window.showPreview(f"背景: {bg_filename}", str(bg_path))
        self.preview_window.showAtPosition(global_pos)
        
        # 设置定时器隐藏预览（如果鼠标离开）
        self.preview_timer.start(3000)  # 3秒后自动隐藏
    
    def onBackgroundSelectedFromPreview(self, bg_filename):
        """从预览区域选择背景"""
        # 更新下拉框选择
        index = self.scene_tab.background_combo.findText(bg_filename)
        if index >= 0:
            self.scene_tab.background_combo.setCurrentIndex(index)
        
        # 加载背景
        self.loadBackground()
    
    def hidePreview(self):
        """隐藏预览窗口"""
        if self.preview_window:
            self.preview_window.hide()
    
    def addCharacterInstance(self, character_name: str, size: str):
        """添加角色实例"""
        if not character_name:
            QMessageBox.warning(self, "警告", "请选择角色")
            return
        
        instance = CharacterInstance(character_name, size)
        instance.z_order = self.next_z_order
        self.next_z_order += 1
        
        self.character_instances[instance.instance_id] = instance
        
        # 添加到画布
        self.canvas.addCharacterInstance(instance.instance_id, instance)
        
        # 更新列表
        self.updateInstanceList()
        
        # 选中新实例
        self.character_tab.instance_list.setCurrentRow(len(self.character_instances) - 1)
        
        self.status_bar.showMessage(f"添加角色: {instance.name}")
    
    def updateInstanceList(self):
        """更新角色实例列表"""
        self.character_tab.instance_list.clear()
        
        # 按照z_order排序显示
        sorted_instances = sorted(self.character_instances.values(), key=lambda x: x.z_order, reverse=True)
        
        for instance in sorted_instances:
            visibility = '显示' if instance.visible else '隐藏'
            item_text = f"[层级{instance.z_order}] {instance.name} ({visibility})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, instance.instance_id)
            self.character_tab.instance_list.addItem(item)
    
    def onInstanceSelected(self, row):
        """角色实例选择处理"""
        if row >= 0:
            item = self.character_tab.instance_list.item(row)
            if item:
                instance_id = item.data(Qt.ItemDataRole.UserRole)
                old_instance = self.current_instance
                self.current_instance = self.character_instances.get(instance_id)
                
                # 只有当实例真正改变时才更新控件
                if old_instance != self.current_instance:
                    self.updateTransformControls()
                    self.updateLayerUI()
                    self.updateLayerOrderDisplay()
        else:
            self.current_instance = None
            self.updateLayerUI()
    
    def updateTransformControls(self):
        """更新变换控件"""
        if self.current_instance:
            # 设置更新标志，防止触发变换事件
            self._updating_controls = True
            
            try:
                # 更新数值输入框
                self.character_tab.x_spinbox.setValue(int(self.current_instance.x_offset))
                self.character_tab.y_spinbox.setValue(int(self.current_instance.y_offset))
                self.character_tab.scale_spinbox.setValue(self.current_instance.scale)
                
                # 更新滑块
                self.character_tab.x_slider.setValue(int(self.current_instance.x_offset))
                self.character_tab.y_slider.setValue(int(self.current_instance.y_offset))
                self.character_tab.scale_slider.setValue(int(self.current_instance.scale * 100))
                
                # 更新层级显示
                self.character_tab.zorder_label.setText(str(self.current_instance.z_order))
                
            finally:
                # 清除更新标志
                self._updating_controls = False
    
    def onTransformChanged(self):
        """变换控件改变处理"""
        # 如果正在更新控件，则忽略变换事件
        if self._updating_controls:
            return
            
        if self.current_instance:
            self.current_instance.x_offset = float(self.character_tab.x_spinbox.value())
            self.current_instance.y_offset = float(self.character_tab.y_spinbox.value())
            self.current_instance.scale = self.character_tab.scale_spinbox.value()
            
            self.canvas.updateCharacterInstance(self.current_instance.instance_id)
    
    def resetTransform(self):
        """重置变换"""
        if self.current_instance:
            self.current_instance.x_offset = 0.0
            self.current_instance.y_offset = 0.0
            self.current_instance.scale = 1.0
            self.updateTransformControls()
            self.canvas.updateCharacterInstance(self.current_instance.instance_id)
    
    def updateLayerUI(self):
        """更新图层UI"""
        # 清空现有控件
        for i in reversed(range(self.layer_tab.layer_scroll_layout.count())):
            item = self.layer_tab.layer_scroll_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None)
        
        if not self.current_instance:
            return
        
        character_name = self.current_instance.character_name
        size = self.current_instance.size
        
        if character_name not in self.character_data:
            return
        
        char_data = self.character_data[character_name]
        size_data = char_data['layer_mapping'].get(size, {})
        
        # 根据图层名称智能分组
        layer_groups = organize_layers_by_type(size_data.get('未分组', []))
        
        for group_name, layers in layer_groups.items():
            # 分组标题
            group_label = QLabel(f"=== {group_name} ===")
            group_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            group_label.setStyleSheet("color: #2c3e50; margin: 10px 0 5px 0;")
            self.layer_tab.layer_scroll_layout.addWidget(group_label)
            
            # 图层选项
            for layer in layers:
                layer_frame = QFrame()
                layer_layout = QHBoxLayout(layer_frame)
                layer_layout.setContentsMargins(20, 2, 5, 2)
                
                # 检查是否已选中
                layer_id = layer['layer_id']
                is_selected = layer_id in self.current_instance.composition_layers
                
                # 使用支持预览的复选框
                checkbox = PreviewableCheckBox(f"{layer['name']} (ID:{layer_id})", layer)
                checkbox.setChecked(is_selected)
                checkbox.toggled.connect(lambda checked, l=layer: self.toggleLayer(l, checked))
                checkbox.previewRequested.connect(self.showLayerPreview)
                layer_layout.addWidget(checkbox)
                
                # 显示图层信息
                info_text = f"{layer['size'][0]}×{layer['size'][1]}"
                if layer['has_image']:
                    info_text += " ✓"
                    info_color = "#27ae60"
                else:
                    info_text += " ✗"
                    info_color = "#e74c3c"
                
                info_label = QLabel(info_text)
                info_label.setStyleSheet(f"color: {info_color}; font-weight: bold;")
                layer_layout.addWidget(info_label)
                
                layer_layout.addStretch()
                self.layer_tab.layer_scroll_layout.addWidget(layer_frame)
        
        # 添加自定义图层分组
        custom_layers = [layer for layer_id, layer in self.current_instance.composition_layers.items() 
                        if layer_id < 0 and layer.get('custom', False)]
        
        if custom_layers:
            # 自定义图层分组标题
            custom_group_label = QLabel("=== 自定义图层 ===")
            custom_group_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            custom_group_label.setStyleSheet("color: #8e44ad; margin: 10px 0 5px 0;")
            self.layer_tab.layer_scroll_layout.addWidget(custom_group_label)
            
            for layer in custom_layers:
                layer_frame = QFrame()
                layer_layout = QHBoxLayout(layer_frame)
                layer_layout.setContentsMargins(20, 2, 5, 2)
                
                # 检查是否已选中（自定义图层默认选中）
                layer_id = layer['layer_id']
                
                # 使用普通复选框（自定义图层）
                checkbox = QCheckBox(f"{layer['name']} (自定义)")
                checkbox.setChecked(True)  # 自定义图层一旦添加就选中
                checkbox.setStyleSheet("color: #8e44ad; font-weight: bold;")
                checkbox.toggled.connect(lambda checked, l=layer: self.toggleCustomLayer(l, checked))
                layer_layout.addWidget(checkbox)
                
                # 显示图层信息
                info_text = f"{layer['size'][0]}×{layer['size'][1]} ✓"
                info_label = QLabel(info_text)
                info_label.setStyleSheet("color: #8e44ad; font-weight: bold;")
                layer_layout.addWidget(info_label)
                
                # 删除按钮
                delete_btn = QPushButton("删除")
                delete_btn.setMaximumWidth(50)
                delete_btn.setStyleSheet("QPushButton { background-color: #e74c3c; color: white; } QPushButton:hover { background-color: #c0392b; }")
                delete_btn.clicked.connect(lambda _, l=layer: self.removeCustomLayer(l))
                layer_layout.addWidget(delete_btn)
                
                layer_layout.addStretch()
                self.layer_tab.layer_scroll_layout.addWidget(layer_frame)
        
        self.layer_tab.layer_scroll_layout.addStretch()
    
    def showLayerPreview(self, layer, global_pos):
        """显示图层预览"""
        if not self.current_instance:
            return
        
        character_name = self.current_instance.character_name
        size = self.current_instance.size
        layer_id = layer['layer_id']
        
        # 构建图像文件路径
        png_file = f"cr_data_png/{character_name}_{size}_{layer_id}.png"
        
        # 显示预览
        self.preview_window.showPreview(layer['name'], png_file, layer)
        self.preview_window.showAtPosition(global_pos)
        
        # 设置定时器隐藏预览（如果鼠标离开）
        self.preview_timer.start(3000)  # 3秒后自动隐藏
    
    def toggleLayer(self, layer, is_selected):
        """切换图层显示"""
        if not self.current_instance:
            return
        
        layer_id = layer['layer_id']
        
        if is_selected:
            self.addLayerToInstance(layer)
        else:
            self.removeLayerFromInstance(layer_id)
    
    def addLayerToInstance(self, layer):
        """添加图层到角色实例"""
        if not self.current_instance:
            return
        
        layer_id = layer['layer_id']
        character_name = self.current_instance.character_name
        size = self.current_instance.size
        
        png_file = f"cr_data_png/{character_name}_{size}_{layer_id}.png"
        
        if not os.path.exists(png_file):
            QMessageBox.warning(self, "警告", f"图像文件不存在:\n{png_file}")
            return
        
        # 异步加载图像
        self.image_loader.addTask(layer_id, png_file)
        
        # 先添加图层信息
        self.current_instance.composition_layers[layer_id] = layer
        if layer_id not in self.current_instance.layer_order:
            self.current_instance.layer_order.append(layer_id)
        
        self.updateLayerOrderDisplay()
        
        # 启动加载
        if not self.image_loader.isRunning():
            self.progress_bar.setVisible(True)
            self.image_loader.start()
    
    def importCustomLayer(self, file_path, layer_name):
        """导入自定义图层并智能对齐"""
        if not self.current_instance:
            QMessageBox.warning(self, "警告", "请先选择一个角色实例")
            return
        
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "警告", f"文件不存在: {file_path}")
            return
        
        try:
            # 简化版本：跳过复杂的对齐系统
            # 直接使用基本的图层信息
            
            # 生成唯一的图层ID（使用负数避免与原始图层冲突）
            custom_layer_id = -(len([lid for lid in self.current_instance.composition_layers.keys() if lid < 0]) + 1)
            
            # 加载图像并转换为PNG格式
            if PIL_AVAILABLE:
                from PIL import Image
                img = Image.open(file_path)
                # 确保图像有透明通道
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # 根据对齐点计算实际位置
                actual_x = alignment_point.x - (img.width * alignment_point.anchor_x)
                actual_y = alignment_point.y - (img.height * alignment_point.anchor_y)
                
                # 创建自定义图层信息
                custom_layer = {
                    'name': layer_name,
                    'layer_id': custom_layer_id,
                    'position': [actual_x, actual_y],
                    'size': [img.width, img.height],
                    'has_image': True,
                    'custom': True,  # 标记为自定义图层
                    'file_path': file_path,
                    'layer_type': layer_type,  # 保存检测到的类型
                    'z_order': z_order,  # 保存Z序
                    'alignment_point': {  # 保存对齐信息
                        'x': alignment_point.x,
                        'y': alignment_point.y,
                        'scale': alignment_point.scale,
                        'anchor_x': alignment_point.anchor_x,
                        'anchor_y': alignment_point.anchor_y
                    }
                }
                
                # 添加到当前角色实例
                self.current_instance.composition_layers[custom_layer_id] = custom_layer
                self.current_instance.layer_images[custom_layer_id] = img
                
                # 按Z序插入到正确位置
                self._insert_layer_by_z_order(custom_layer_id, z_order)
                
                # 更新显示
                self.updateLayerUI()
                self.updateLayerOrderDisplay()
                self.canvas.updateCharacterInstance(self.current_instance.instance_id)
                
                # 显示对齐信息
                category = alignment_system.get_layer_category(layer_type)
                layer_type_name = alignment_system.layer_configs[layer_type].name
                self.status_bar.showMessage(
                    f"成功导入并对齐: {layer_name} (类型: {layer_type_name}, 类别: {category}, 位置: {actual_x:.0f}, {actual_y:.0f})"
                )
                
            else:
                QMessageBox.warning(self, "警告", "PIL库不可用，无法导入图像")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导入自定义图层失败: {e}")
            import traceback
            traceback.print_exc()
    
    def onImportCustomLayerRequested(self, file_path, layer_info):
        """处理导入自定义图层请求（简化版本）"""
        QMessageBox.information(self, "提示", "自定义图层导入功能暂未实现")
    
    def importCustomLayerWithType(self, file_path, layer_name, layer_type):
        """使用指定类型导入自定义图层（简化版本）"""
        QMessageBox.information(self, "提示", "自定义图层导入功能暂未实现")
    
    def _insert_layer_by_z_order(self, layer_id, z_order):
        """按Z序插入图层到正确位置"""
        if not self.current_instance or not hasattr(self.current_instance, 'layer_order'):
            return
            
        # 如果已经在列表中，先移除
        if layer_id in self.current_instance.layer_order:
            self.current_instance.layer_order.remove(layer_id)
        
        # 找到合适的插入位置（按Z序排序，从小到大）
        insert_pos = len(self.current_instance.layer_order)
        for i, existing_id in enumerate(self.current_instance.layer_order):
            existing_layer = self.current_instance.composition_layers.get(existing_id)
            if existing_layer:
                existing_z = existing_layer.get('z_order', 0)
                if z_order < existing_z:
                    insert_pos = i
                    break
        
        # 插入到正确位置
        self.current_instance.layer_order.insert(insert_pos, layer_id)
    
    def toggleCustomLayer(self, layer, is_selected):
        """切换自定义图层显示"""
        if not self.current_instance:
            return
        
        layer_id = layer['layer_id']
        
        if is_selected:
            # 自定义图层已经在导入时添加，这里只需要确保在layer_order中
            if layer_id not in self.current_instance.layer_order:
                self.current_instance.layer_order.append(layer_id)
        else:
            # 从layer_order中移除，但保持在composition_layers中
            if layer_id in self.current_instance.layer_order:
                self.current_instance.layer_order.remove(layer_id)
        
        self.updateLayerOrderDisplay()
        self.canvas.updateCharacterInstance(self.current_instance.instance_id)
    
    def removeCustomLayer(self, layer):
        """删除自定义图层"""
        if not self.current_instance:
            return
        
        layer_id = layer['layer_id']
        
        # 确认删除
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除自定义图层 '{layer['name']}' 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 从各个地方移除图层
            if layer_id in self.current_instance.layer_images:
                del self.current_instance.layer_images[layer_id]
            if layer_id in self.current_instance.composition_layers:
                del self.current_instance.composition_layers[layer_id]
            if layer_id in self.current_instance.layer_order:
                self.current_instance.layer_order.remove(layer_id)
            
            # 更新显示
            self.updateLayerUI()
            self.updateLayerOrderDisplay()
            self.canvas.updateCharacterInstance(self.current_instance.instance_id)
            
            self.status_bar.showMessage(f"已删除自定义图层: {layer['name']}")
    
    def removeLayerFromInstance(self, layer_id):
        """从角色实例移除图层"""
        if not self.current_instance:
            return
        
        if layer_id in self.current_instance.layer_images:
            del self.current_instance.layer_images[layer_id]
        if layer_id in self.current_instance.composition_layers:
            del self.current_instance.composition_layers[layer_id]
        if layer_id in self.current_instance.layer_order:
            self.current_instance.layer_order.remove(layer_id)
        
        self.updateLayerOrderDisplay()
        self.canvas.updateCharacterInstance(self.current_instance.instance_id)
    
    def onImageLoaded(self, layer_id, image):
        """图像加载完成"""
        # 找到所有包含此图层的角色实例
        for instance in self.character_instances.values():
            if layer_id in instance.composition_layers:
                instance.layer_images[layer_id] = image
                self.canvas.updateCharacterInstance(instance.instance_id)
                
        # 如果当前选中的实例包含此图层，更新UI
        if (self.current_instance and 
            layer_id in self.current_instance.composition_layers):
            self.updateLayerOrderDisplay()
    
    def onLoadProgress(self, current, total):
        """加载进度更新"""
        if total > 0:
            self.progress_bar.setValue(int(current * 100 / total))
            if current >= total:
                self.progress_bar.setVisible(False)
    
    def updateLayerOrderDisplay(self):
        """更新图层顺序显示"""
        self.layer_tab.layer_order_list.clear()
        
        if not self.current_instance:
            return
        
        for i, layer_id in enumerate(self.current_instance.layer_order):
            if layer_id in self.current_instance.composition_layers:
                layer = self.current_instance.composition_layers[layer_id]
                display_text = f"{i+1}. {layer['name']} (ID:{layer_id})"
                item = QListWidgetItem(display_text)
                item.setData(Qt.ItemDataRole.UserRole, layer_id)
                self.layer_tab.layer_order_list.addItem(item)
    
    # 图层顺序控制方法
    def moveLayerUp(self):
        """向上移动图层"""
        if not self.current_instance:
            return
        
        current_row = self.layer_tab.layer_order_list.currentRow()
        if current_row >= 0 and current_row < len(self.current_instance.layer_order) - 1:
            layer_order = self.current_instance.layer_order
            layer_order[current_row], layer_order[current_row + 1] = \
                layer_order[current_row + 1], layer_order[current_row]
            
            self.updateLayerOrderDisplay()
            self.layer_tab.layer_order_list.setCurrentRow(current_row + 1)
            self.canvas.updateCharacterInstance(self.current_instance.instance_id)
    
    def moveLayerDown(self):
        """向下移动图层"""
        if not self.current_instance:
            return
        
        current_row = self.layer_tab.layer_order_list.currentRow()
        if current_row > 0:
            layer_order = self.current_instance.layer_order
            layer_order[current_row], layer_order[current_row - 1] = \
                layer_order[current_row - 1], layer_order[current_row]
            
            self.updateLayerOrderDisplay()
            self.layer_tab.layer_order_list.setCurrentRow(current_row - 1)
            self.canvas.updateCharacterInstance(self.current_instance.instance_id)
    
    def moveLayerToTop(self):
        """移动图层到顶层"""
        if not self.current_instance:
            return
        
        current_row = self.layer_tab.layer_order_list.currentRow()
        if current_row >= 0:
            layer_order = self.current_instance.layer_order
            layer_id = layer_order.pop(current_row)
            layer_order.append(layer_id)
            
            self.updateLayerOrderDisplay()
            self.layer_tab.layer_order_list.setCurrentRow(len(layer_order) - 1)
            self.canvas.updateCharacterInstance(self.current_instance.instance_id)
    
    def moveLayerToBottom(self):
        """移动图层到底层"""
        if not self.current_instance:
            return
        
        current_row = self.layer_tab.layer_order_list.currentRow()
        if current_row >= 0:
            layer_order = self.current_instance.layer_order
            layer_id = layer_order.pop(current_row)
            layer_order.insert(0, layer_id)
            
            self.updateLayerOrderDisplay()
            self.layer_tab.layer_order_list.setCurrentRow(0)
            self.canvas.updateCharacterInstance(self.current_instance.instance_id)
    
    def duplicateCharacterInstance(self):
        """复制角色实例"""
        if not self.current_instance:
            QMessageBox.warning(self, "警告", "请选择要复制的角色实例")
            return
        
        original = self.current_instance
        new_instance = CharacterInstance(original.character_name, original.size)
        
        # 复制所有属性
        new_instance.layer_images = original.layer_images.copy()
        new_instance.composition_layers = original.composition_layers.copy()
        new_instance.layer_order = original.layer_order.copy()
        new_instance.x_offset = original.x_offset + 100
        new_instance.y_offset = original.y_offset + 100
        new_instance.scale = original.scale
        new_instance.z_order = self.next_z_order  # 新的层级
        self.next_z_order += 1
        
        self.character_instances[new_instance.instance_id] = new_instance
        self.canvas.addCharacterInstance(new_instance.instance_id, new_instance)
        self.updateInstanceList()
        
        self.status_bar.showMessage(f"复制角色: {new_instance.name}")
    
    def removeCharacterInstance(self):
        """删除角色实例"""
        if not self.current_instance:
            QMessageBox.warning(self, "警告", "请选择要删除的角色实例")
            return
        
        instance_id = self.current_instance.instance_id
        del self.character_instances[instance_id]
        
        self.canvas.removeCharacterInstance(instance_id)
        self.current_instance = None
        self.updateInstanceList()
        self.updateLayerUI()
        
        self.status_bar.showMessage("角色实例已删除")
    
    def clearAllCharacters(self):
        """清空所有角色"""
        self.character_instances.clear()
        self.current_instance = None
        
        for instance_id in list(self.canvas.character_instances.keys()):
            self.canvas.removeCharacterInstance(instance_id)
        
        self.updateInstanceList()
        self.updateLayerUI()
        self.status_bar.showMessage("所有角色已清空")
    
    def onCanvasCharacterSelected(self, instance_id):
        """画布角色选择处理"""
        if instance_id in self.character_instances:
            old_instance = self.current_instance
            self.current_instance = self.character_instances[instance_id]
            
            # 更新列表选择
            for i in range(self.character_tab.instance_list.count()):
                item = self.character_tab.instance_list.item(i)
                if item and item.data(Qt.ItemDataRole.UserRole) == instance_id:
                    # 临时断开列表选择信号，避免循环调用
                    self.character_tab.instance_list.currentRowChanged.disconnect()
                    try:
                        self.character_tab.instance_list.setCurrentRow(i)
                    finally:
                        self.character_tab.instance_list.currentRowChanged.connect(self.onInstanceSelected)
                    break
            
            # 只有当实例真正改变时才更新控件
            if old_instance != self.current_instance:
                self.updateTransformControls()
    
    def onCanvasCharacterTransformChanged(self, instance_id):
        """画布角色变换改变处理"""
        if instance_id in self.character_instances:
            instance = self.character_instances[instance_id]
            # 如果改变的是当前选中的角色，更新控制面板
            if self.current_instance and self.current_instance.instance_id == instance_id:
                self.updateTransformControls()
    
    def fitCanvas(self):
        """适应画布大小"""
        if self.canvas.background_pixmap:
            # 计算合适的缩放比例
            canvas_width = self.canvas.width()
            canvas_height = self.canvas.height()
            bg_width = self.canvas.background_pixmap.width()
            bg_height = self.canvas.background_pixmap.height()
            
            scale_x = canvas_width / bg_width * 0.9  # 留10%边距
            scale_y = canvas_height / bg_height * 0.9
            
            self.canvas.scale_factor = min(scale_x, scale_y, 1.0)  # 不超过100%
            self.canvas.offset_x = 0
            self.canvas.offset_y = 0
            self.updateZoomLabel()
            self.canvas.update()
    
    def resetView(self):
        """重置视图"""
        self.canvas.scale_factor = 1.0
        self.canvas.offset_x = 0
        self.canvas.offset_y = 0
        self.updateZoomLabel()
        self.canvas.update()
    
    def updateZoomLabel(self):
        """更新缩放标签"""
        zoom_percent = int(self.canvas.scale_factor * 100)
        self.zoom_label.setText(f"缩放: {zoom_percent}%")
    
    def moveCharacterForward(self):
        """角色前移一层"""
        if not self.current_instance:
            QMessageBox.warning(self, "警告", "请选择要调整的角色")
            return
        
        # 找到比当前角色层级大1的最小层级
        current_z = self.current_instance.z_order
        target_z = None
        
        for instance in self.character_instances.values():
            if instance.z_order > current_z:
                if target_z is None or instance.z_order < target_z:
                    target_z = instance.z_order
        
        if target_z is not None:
            # 交换层级
            for instance in self.character_instances.values():
                if instance.z_order == target_z:
                    instance.z_order = current_z
                    break
            self.current_instance.z_order = target_z
            
            self.updateInstanceList()
            self.updateTransformControls()
            self.canvas.update()
    
    def moveCharacterBackward(self):
        """角色后移一层"""
        if not self.current_instance:
            QMessageBox.warning(self, "警告", "请选择要调整的角色")
            return
        
        # 找到比当前角色层级小1的最大层级
        current_z = self.current_instance.z_order
        target_z = None
        
        for instance in self.character_instances.values():
            if instance.z_order < current_z:
                if target_z is None or instance.z_order > target_z:
                    target_z = instance.z_order
        
        if target_z is not None:
            # 交换层级
            for instance in self.character_instances.values():
                if instance.z_order == target_z:
                    instance.z_order = current_z
                    break
            self.current_instance.z_order = target_z
            
            self.updateInstanceList()
            self.updateTransformControls()
            self.canvas.update()
    
    def moveCharacterToFront(self):
        """角色移到最前"""
        if not self.current_instance:
            QMessageBox.warning(self, "警告", "请选择要调整的角色")
            return
        
        # 找到最大层级
        max_z = max((instance.z_order for instance in self.character_instances.values()), default=0)
        
        if self.current_instance.z_order < max_z:
            self.current_instance.z_order = max_z + 1
            self.updateInstanceList()
            self.updateTransformControls()
            self.canvas.update()
    
    def moveCharacterToBack(self):
        """角色移到最后"""
        if not self.current_instance:
            QMessageBox.warning(self, "警告", "请选择要调整的角色")
            return
        
        # 找到最小层级
        min_z = min((instance.z_order for instance in self.character_instances.values()), default=0)
        
        if self.current_instance.z_order > min_z:
            self.current_instance.z_order = min_z - 1
            self.updateInstanceList()
            self.updateTransformControls()
            self.canvas.update()
    
    def exportImage(self):
        """导出图像 - 高清无损渲染"""
        if not self.character_instances and not self.canvas.background_pixmap:
            QMessageBox.warning(self, "警告", "没有内容可以导出")
            return
        
        # 首先让用户选择导出分辨率
        resolution_dialog = QMessageBox()
        resolution_dialog.setWindowTitle("选择导出分辨率")
        resolution_dialog.setText("请选择导出图像的分辨率倍数：")
        
        # 添加自定义按钮
        btn_1x = resolution_dialog.addButton("1倍 (原始)", QMessageBox.ButtonRole.ActionRole)
        btn_2x = resolution_dialog.addButton("2倍 (高清)", QMessageBox.ButtonRole.ActionRole)
        btn_3x = resolution_dialog.addButton("3倍 (超清)", QMessageBox.ButtonRole.ActionRole)
        btn_4x = resolution_dialog.addButton("4倍 (4K)", QMessageBox.ButtonRole.ActionRole)
        btn_cancel = resolution_dialog.addButton("取消", QMessageBox.ButtonRole.RejectRole)
        
        resolution_dialog.exec()
        clicked_button = resolution_dialog.clickedButton()
        
        if clicked_button == btn_cancel:
            return
        elif clicked_button == btn_1x:
            scale_multiplier = 1.0
        elif clicked_button == btn_2x:
            scale_multiplier = 2.0
        elif clicked_button == btn_3x:
            scale_multiplier = 3.0
        elif clicked_button == btn_4x:
            scale_multiplier = 4.0
        else:
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出图像", "", "PNG files (*.png);;JPEG files (*.jpg)"
        )
        
        if filename:
            try:
                # 确定基础导出尺寸
                if self.canvas.background_pixmap:
                    base_width = self.canvas.background_pixmap.width()
                    base_height = self.canvas.background_pixmap.height()
                else:
                    base_width = 1920
                    base_height = 1080
                
                # 应用分辨率倍数
                export_width = int(base_width * scale_multiplier)
                export_height = int(base_height * scale_multiplier)
                
                # 显示导出进度
                self.status_bar.showMessage(f"正在导出 {export_width}×{export_height} 高清图像...")
                QApplication.processEvents()  # 更新UI
                
                # 创建高质量画布
                export_pixmap = QPixmap(export_width, export_height)
                export_pixmap.fill(Qt.GlobalColor.transparent)
                
                painter = QPainter(export_pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
                painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
                
                # 绘制背景（高分辨率缩放）
                if self.canvas.background_pixmap:
                    # 高质量缩放背景图
                    scaled_bg = self.canvas.background_pixmap.scaled(
                        export_width, export_height, 
                        Qt.AspectRatioMode.IgnoreAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    painter.drawPixmap(0, 0, scaled_bg)
                
                # 使用专门的高分辨率导出渲染方法绘制角色
                self.renderCharactersForExport(painter, export_width, export_height, scale_multiplier)
                
                painter.end()
                
                # 保存文件（最高质量）
                success = export_pixmap.save(filename, None, 100)  # 100%质量
                
                if success:
                    file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
                    QMessageBox.information(self, "导出成功", 
                        f"高清图像已导出到:\n{filename}\n"
                        f"分辨率: {export_width}×{export_height} ({scale_multiplier}倍)\n"
                        f"文件大小: {file_size:.2f} MB")
                else:
                    QMessageBox.warning(self, "警告", "保存文件失败")
                
                self.status_bar.showMessage("导出完成")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出图像失败: {e}")
                self.status_bar.showMessage("导出失败")
    
    def exportImageHD(self):
        """快速高清导出 - 默认2倍分辨率"""
        if not self.character_instances and not self.canvas.background_pixmap:
            QMessageBox.warning(self, "警告", "没有内容可以导出")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "高清导出图像", "", "PNG files (*.png);;JPEG files (*.jpg)"
        )
        
        if filename:
            try:
                scale_multiplier = 2.0  # 固定2倍分辨率
                
                # 确定基础导出尺寸
                if self.canvas.background_pixmap:
                    base_width = self.canvas.background_pixmap.width()
                    base_height = self.canvas.background_pixmap.height()
                else:
                    base_width = 1920
                    base_height = 1080
                
                # 应用分辨率倍数
                export_width = int(base_width * scale_multiplier)
                export_height = int(base_height * scale_multiplier)
                
                # 显示导出进度
                self.status_bar.showMessage(f"正在高清导出 {export_width}×{export_height} 图像...")
                QApplication.processEvents()  # 更新UI
                
                # 创建高质量画布
                export_pixmap = QPixmap(export_width, export_height)
                export_pixmap.fill(Qt.GlobalColor.transparent)
                
                painter = QPainter(export_pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
                painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
                
                # 绘制背景（高分辨率缩放）
                if self.canvas.background_pixmap:
                    # 高质量缩放背景图
                    scaled_bg = self.canvas.background_pixmap.scaled(
                        export_width, export_height, 
                        Qt.AspectRatioMode.IgnoreAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    painter.drawPixmap(0, 0, scaled_bg)
                
                # 使用专门的高分辨率导出渲染方法绘制角色
                self.renderCharactersForExport(painter, export_width, export_height, scale_multiplier)
                
                painter.end()
                
                # 保存文件（最高质量）
                success = export_pixmap.save(filename, None, 100)  # 100%质量
                
                if success:
                    file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
                    QMessageBox.information(self, "高清导出成功", 
                        f"高清图像已导出到:\n{filename}\n"
                        f"分辨率: {export_width}×{export_height} (2倍高清)\n"
                        f"文件大小: {file_size:.2f} MB")
                else:
                    QMessageBox.warning(self, "警告", "保存文件失败")
                
                self.status_bar.showMessage("高清导出完成")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"高清导出失败: {e}")
                self.status_bar.showMessage("高清导出失败")
    
    def renderCharactersForExport(self, painter: QPainter, canvas_width: int, canvas_height: int, scale_multiplier: float = 1.0):
        """专用于导出的角色渲染方法 - 支持高分辨率"""
        # 计算画布中心（考虑分辨率倍数）
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        # 按照正确的图层顺序渲染所有角色
        all_render_items = []
        
        # 按z_order从小到大排序角色（小的在后面，大的在前面）
        sorted_instances = sorted(self.character_instances.values(), key=lambda x: x.z_order)
        
        # 收集所有要渲染的图层，按角色层级和图层顺序排序
        for instance in sorted_instances:
            if not instance.visible:
                continue
                
            for layer_id in instance.layer_order:
                if layer_id in instance.composition_layers and layer_id in instance.layer_images:
                    layer = instance.composition_layers[layer_id]
                    image = instance.layer_images[layer_id]
                    
                    # 计算最终位置（考虑角色变换、居中和分辨率倍数）
                    layer_x, layer_y = layer['position']
                    
                    # 应用角色变换和分辨率倍数
                    final_x = (layer_x * instance.scale + instance.x_offset) * scale_multiplier
                    final_y = (layer_y * instance.scale + instance.y_offset) * scale_multiplier
                    
                    # 应用画布居中偏移
                    final_x += center_x
                    final_y += center_y
                    
                    # 计算最终缩放比例（实例缩放 × 分辨率倍数）
                    final_scale = instance.scale * scale_multiplier
                    
                    all_render_items.append({
                        'image': image,
                        'x': final_x,
                        'y': final_y,
                        'scale': final_scale,
                        'layer_id': layer_id,
                        'instance_id': instance.instance_id
                    })
        
        # 渲染所有图层
        for item in all_render_items:
            # 转换PIL图像为高分辨率QPixmap
            pixmap = pil_to_qpixmap_high_quality(item['image'], item['scale'])
            if pixmap:
                painter.drawPixmap(int(item['x']), int(item['y']), pixmap)
    
    def saveScene(self):
        """保存场景"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "保存场景", "", "JSON files (*.json)"
        )
        
        if filename:
            try:
                scene_data = {
                    'background': self.scene_tab.background_combo.currentText(),
                    'characters': []
                }
                
                for instance in self.character_instances.values():
                    char_data = {
                        'character_name': instance.character_name,
                        'size': instance.size,
                        'x_offset': instance.x_offset,
                        'y_offset': instance.y_offset,
                        'scale': instance.scale,
                        'visible': instance.visible,
                        'z_order': instance.z_order,
                        'layers': list(instance.composition_layers.keys()),
                        'layer_order': instance.layer_order
                    }
                    scene_data['characters'].append(char_data)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(scene_data, f, ensure_ascii=False, indent=2)
                
                QMessageBox.information(self, "成功", "场景已保存")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存场景失败: {e}")
    
    def loadScene(self):
        """加载场景"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "加载场景", "", "JSON files (*.json)"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    scene_data = json.load(f)
                
                # 清空当前场景
                self.clearAllCharacters()
                
                # 加载背景
                if scene_data.get('background'):
                    index = self.scene_tab.background_combo.findText(scene_data['background'])
                    if index >= 0:
                        self.scene_tab.background_combo.setCurrentIndex(index)
                
                # 重建角色实例
                loaded_count = 0
                for char_data in scene_data.get('characters', []):
                    instance = CharacterInstance(char_data['character_name'], char_data['size'])
                    instance.x_offset = char_data.get('x_offset', 0.0)
                    instance.y_offset = char_data.get('y_offset', 0.0)
                    instance.scale = char_data.get('scale', 1.0)
                    instance.visible = char_data.get('visible', True)
                    instance.z_order = char_data.get('z_order', loaded_count)
                    
                    # 重建图层信息
                    if char_data['character_name'] in self.character_data:
                        char_info = self.character_data[char_data['character_name']]
                        size_data = char_info['layer_mapping'].get(char_data['size'], {})
                        
                        # 收集所有分组中的图层
                        all_layers = []
                        for group_name, group_layers in size_data.items():
                            all_layers.extend(group_layers)
                        
                        for layer_id in char_data.get('layers', []):
                            for layer in all_layers:
                                if layer['layer_id'] == layer_id:
                                    instance.composition_layers[layer_id] = layer
                                    
                                    # 加载对应的图像文件
                                    png_file = f"cr_data_png/{char_data['character_name']}_{char_data['size']}_{layer_id}.png"
                                    if os.path.exists(png_file):
                                        self.image_loader.addTask(layer_id, png_file)
                                    break
                        
                        instance.layer_order = char_data.get('layer_order', list(instance.composition_layers.keys()))
                    
                    self.character_instances[instance.instance_id] = instance
                    self.canvas.addCharacterInstance(instance.instance_id, instance)
                    loaded_count += 1
                
                # 更新next_z_order
                if self.character_instances:
                    self.next_z_order = max(instance.z_order for instance in self.character_instances.values()) + 1
                
                # 启动图像加载器
                if self.image_loader.tasks and not self.image_loader.isRunning():
                    self.progress_bar.setVisible(True)
                    self.image_loader.start()
                
                self.updateInstanceList()
                
                # 强制更新画布
                self.canvas.update()
                
                QMessageBox.information(self, "成功", f"场景已加载，共 {loaded_count} 个角色")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载场景失败: {e}")
