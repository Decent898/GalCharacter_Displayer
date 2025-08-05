#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标签页组件
包含场景、角色、图层三个标签页的实现
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QComboBox,
    QPushButton, QScrollArea, QButtonGroup, QRadioButton, QListWidget,
    QSpinBox, QDoubleSpinBox, QSlider, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class SceneTab(QWidget):
    """场景标签页"""
    
    # 信号定义
    backgroundComboChanged = pyqtSignal(str)
    loadBackgroundRequested = pyqtSignal()
    clearBackgroundRequested = pyqtSignal()
    canvasModeChanged = pyqtSignal(str)
    fitCanvasRequested = pyqtSignal()
    resetViewRequested = pyqtSignal()
    exportImageRequested = pyqtSignal()
    exportImageHDRequested = pyqtSignal()
    saveSceneRequested = pyqtSignal()
    loadSceneRequested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setupConnections()
    
    def setupUI(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 背景设置组
        bg_group = QGroupBox("背景设置")
        bg_layout = QVBoxLayout(bg_group)
        
        # 快速选择区域
        quick_layout = QHBoxLayout()
        quick_layout.addWidget(QLabel("快速选择:"))
        self.background_combo = QComboBox()
        self.background_combo.setMinimumHeight(30)
        quick_layout.addWidget(self.background_combo)
        bg_layout.addLayout(quick_layout)
        
        bg_btn_layout = QHBoxLayout()
        self.load_bg_btn = QPushButton("加载背景")
        self.clear_bg_btn = QPushButton("清除背景")
        bg_btn_layout.addWidget(self.load_bg_btn)
        bg_btn_layout.addWidget(self.clear_bg_btn)
        bg_layout.addLayout(bg_btn_layout)
        
        # 背景预览选择区域
        bg_preview_label = QLabel("背景预览选择:")
        bg_preview_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        bg_layout.addWidget(bg_preview_label)
        
        # 创建背景滚动区域
        bg_scroll_area = QScrollArea()
        bg_scroll_area.setWidgetResizable(True)
        bg_scroll_area.setMinimumHeight(200)
        bg_scroll_area.setMaximumHeight(300)
        
        self.bg_scroll_widget = QWidget()
        self.bg_scroll_layout = QVBoxLayout(self.bg_scroll_widget)
        bg_scroll_area.setWidget(self.bg_scroll_widget)
        
        bg_layout.addWidget(bg_scroll_area)
        layout.addWidget(bg_group)
        
        # 画布控制组
        canvas_group = QGroupBox("画布控制")
        canvas_layout = QVBoxLayout(canvas_group)
        
        # 交互模式
        mode_layout = QHBoxLayout()
        self.mode_group = QButtonGroup()
        self.canvas_mode_radio = QRadioButton("拖拽画布")
        self.character_mode_radio = QRadioButton("移动角色")
        self.canvas_mode_radio.setChecked(True)
        
        self.mode_group.addButton(self.canvas_mode_radio)
        self.mode_group.addButton(self.character_mode_radio)
        
        mode_layout.addWidget(self.canvas_mode_radio)
        mode_layout.addWidget(self.character_mode_radio)
        canvas_layout.addLayout(mode_layout)
        
        # 画布操作按钮
        canvas_btn_layout = QHBoxLayout()
        self.fit_canvas_btn = QPushButton("适应画布")
        self.reset_view_btn = QPushButton("重置视图")
        canvas_btn_layout.addWidget(self.fit_canvas_btn)
        canvas_btn_layout.addWidget(self.reset_view_btn)
        canvas_layout.addLayout(canvas_btn_layout)
        
        layout.addWidget(canvas_group)
        
        # 文件操作组
        file_group = QGroupBox("文件操作")
        file_layout = QVBoxLayout(file_group)
        
        self.export_btn = QPushButton("导出图片")
        self.export_hd_btn = QPushButton("高清导出")
        self.export_hd_btn.setStyleSheet("QPushButton { background-color: #28a745; } QPushButton:hover { background-color: #218838; }")
        self.save_scene_btn = QPushButton("保存场景")
        self.load_scene_btn = QPushButton("加载场景")
        
        file_layout.addWidget(self.export_btn)
        file_layout.addWidget(self.export_hd_btn)
        file_layout.addWidget(self.save_scene_btn)
        file_layout.addWidget(self.load_scene_btn)
        
        layout.addWidget(file_group)
        layout.addStretch()
    
    def setupConnections(self):
        """设置信号连接"""
        self.background_combo.currentTextChanged.connect(self.backgroundComboChanged.emit)
        self.load_bg_btn.clicked.connect(self.loadBackgroundRequested.emit)
        self.clear_bg_btn.clicked.connect(self.clearBackgroundRequested.emit)
        
        self.canvas_mode_radio.toggled.connect(lambda: self.canvasModeChanged.emit("canvas"))
        self.character_mode_radio.toggled.connect(lambda: self.canvasModeChanged.emit("character"))
        
        self.fit_canvas_btn.clicked.connect(self.fitCanvasRequested.emit)
        self.reset_view_btn.clicked.connect(self.resetViewRequested.emit)
        
        self.export_btn.clicked.connect(self.exportImageRequested.emit)
        self.export_hd_btn.clicked.connect(self.exportImageHDRequested.emit)
        self.save_scene_btn.clicked.connect(self.saveSceneRequested.emit)
        self.load_scene_btn.clicked.connect(self.loadSceneRequested.emit)


class CharacterTab(QWidget):
    """角色标签页"""
    
    # 信号定义
    addCharacterRequested = pyqtSignal(str, str)  # character_name, size
    duplicateCharacterRequested = pyqtSignal()
    removeCharacterRequested = pyqtSignal()
    clearAllCharactersRequested = pyqtSignal()
    instanceSelected = pyqtSignal(int)  # row
    transformChanged = pyqtSignal()
    resetTransformRequested = pyqtSignal()
    moveCharacterForwardRequested = pyqtSignal()
    moveCharacterBackwardRequested = pyqtSignal()
    moveCharacterToFrontRequested = pyqtSignal()
    moveCharacterToBackRequested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setupConnections()
    
    def setupUI(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 添加角色组
        add_group = QGroupBox("添加角色")
        add_layout = QVBoxLayout(add_group)
        
        char_select_layout = QHBoxLayout()
        char_select_layout.addWidget(QLabel("角色:"))
        self.new_character_combo = QComboBox()
        char_select_layout.addWidget(self.new_character_combo)
        add_layout.addLayout(char_select_layout)
        
        size_select_layout = QHBoxLayout()
        size_select_layout.addWidget(QLabel("尺寸:"))
        self.new_size_combo = QComboBox()
        self.new_size_combo.addItems(['s', 'm', 'l', 'll'])
        self.new_size_combo.setCurrentText('l')
        size_select_layout.addWidget(self.new_size_combo)
        add_layout.addLayout(size_select_layout)
        
        self.add_character_btn = QPushButton("添加角色")
        self.add_character_btn.setMinimumHeight(35)
        add_layout.addWidget(self.add_character_btn)
        
        layout.addWidget(add_group)
        
        # 角色列表组
        list_group = QGroupBox("角色列表")
        list_layout = QVBoxLayout(list_group)
        
        self.instance_list = QListWidget()
        self.instance_list.setMinimumHeight(150)
        list_layout.addWidget(self.instance_list)
        
        list_btn_layout = QHBoxLayout()
        self.duplicate_btn = QPushButton("复制")
        self.remove_btn = QPushButton("删除")
        self.clear_all_btn = QPushButton("清空")
        list_btn_layout.addWidget(self.duplicate_btn)
        list_btn_layout.addWidget(self.remove_btn)
        list_btn_layout.addWidget(self.clear_all_btn)
        list_layout.addLayout(list_btn_layout)
        
        layout.addWidget(list_group)
        
        # 变换控制组
        transform_group = QGroupBox("位置和缩放")
        transform_layout = QVBoxLayout(transform_group)
        
        # X偏移
        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel("X:"))
        self.x_slider = QSlider(Qt.Orientation.Horizontal)
        self.x_slider.setRange(-1000, 1000)
        self.x_spinbox = QSpinBox()
        self.x_spinbox.setRange(-1000, 1000)
        x_layout.addWidget(self.x_slider)
        x_layout.addWidget(self.x_spinbox)
        transform_layout.addLayout(x_layout)
        
        # Y偏移
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Y:"))
        self.y_slider = QSlider(Qt.Orientation.Horizontal)
        self.y_slider.setRange(-1000, 1000)
        self.y_spinbox = QSpinBox()
        self.y_spinbox.setRange(-1000, 1000)
        y_layout.addWidget(self.y_slider)
        y_layout.addWidget(self.y_spinbox)
        transform_layout.addLayout(y_layout)
        
        # 缩放
        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("缩放:"))
        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setRange(10, 200)  # 0.1 to 2.0
        self.scale_slider.setValue(100)
        self.scale_spinbox = QDoubleSpinBox()
        self.scale_spinbox.setRange(0.1, 2.0)
        self.scale_spinbox.setValue(1.0)
        self.scale_spinbox.setSingleStep(0.1)
        scale_layout.addWidget(self.scale_slider)
        scale_layout.addWidget(self.scale_spinbox)
        transform_layout.addLayout(scale_layout)
        
        self.reset_transform_btn = QPushButton("重置变换")
        transform_layout.addWidget(self.reset_transform_btn)
        
        layout.addWidget(transform_group)
        
        # 角色层级控制组
        zorder_group = QGroupBox("角色层级")
        zorder_layout = QVBoxLayout(zorder_group)
        
        # 层级显示和调整
        zorder_info_layout = QHBoxLayout()
        zorder_info_layout.addWidget(QLabel("当前层级:"))
        self.zorder_label = QLabel("0")
        self.zorder_label.setStyleSheet("color: #007bff; font-weight: bold;")
        zorder_info_layout.addWidget(self.zorder_label)
        zorder_info_layout.addStretch()
        zorder_layout.addLayout(zorder_info_layout)
        
        # 层级调整按钮
        zorder_btn_layout = QHBoxLayout()
        self.move_forward_btn = QPushButton("前移一层")
        self.move_backward_btn = QPushButton("后移一层")
        self.move_front_btn = QPushButton("移到最前")
        self.move_back_btn = QPushButton("移到最后")
        
        zorder_btn_layout.addWidget(self.move_backward_btn)
        zorder_btn_layout.addWidget(self.move_forward_btn)
        zorder_layout.addLayout(zorder_btn_layout)
        
        zorder_btn_layout2 = QHBoxLayout()
        zorder_btn_layout2.addWidget(self.move_back_btn)
        zorder_btn_layout2.addWidget(self.move_front_btn)
        zorder_layout.addLayout(zorder_btn_layout2)
        
        layout.addWidget(zorder_group)
        layout.addStretch()
    
    def setupConnections(self):
        """设置信号连接"""
        self.add_character_btn.clicked.connect(
            lambda: self.addCharacterRequested.emit(
                self.new_character_combo.currentText(),
                self.new_size_combo.currentText()
            )
        )
        
        self.duplicate_btn.clicked.connect(self.duplicateCharacterRequested.emit)
        self.remove_btn.clicked.connect(self.removeCharacterRequested.emit)
        self.clear_all_btn.clicked.connect(self.clearAllCharactersRequested.emit)
        self.instance_list.currentRowChanged.connect(self.instanceSelected.emit)
        
        # 变换控制连接
        self.x_slider.valueChanged.connect(self.x_spinbox.setValue)
        self.x_spinbox.valueChanged.connect(self.x_slider.setValue)
        self.y_slider.valueChanged.connect(self.y_spinbox.setValue)
        self.y_spinbox.valueChanged.connect(self.y_slider.setValue)
        
        self.x_spinbox.valueChanged.connect(self.transformChanged.emit)
        self.y_spinbox.valueChanged.connect(self.transformChanged.emit)
        self.scale_spinbox.valueChanged.connect(self.transformChanged.emit)
        
        self.reset_transform_btn.clicked.connect(self.resetTransformRequested.emit)
        
        # 角色层级控制
        self.move_forward_btn.clicked.connect(self.moveCharacterForwardRequested.emit)
        self.move_backward_btn.clicked.connect(self.moveCharacterBackwardRequested.emit)
        self.move_front_btn.clicked.connect(self.moveCharacterToFrontRequested.emit)
        self.move_back_btn.clicked.connect(self.moveCharacterToBackRequested.emit)


class LayerTab(QWidget):
    """图层标签页"""
    
    # 信号定义
    layerToggled = pyqtSignal(object, bool)  # layer, is_selected
    moveLayerUpRequested = pyqtSignal()
    moveLayerDownRequested = pyqtSignal()
    moveLayerToTopRequested = pyqtSignal()
    moveLayerToBottomRequested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setupConnections()
    
    def setupUI(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 图层选择组
        layer_group = QGroupBox("图层选择")
        layer_layout = QVBoxLayout(layer_group)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(300)
        
        self.layer_scroll_widget = QWidget()
        self.layer_scroll_layout = QVBoxLayout(self.layer_scroll_widget)
        scroll_area.setWidget(self.layer_scroll_widget)
        
        layer_layout.addWidget(scroll_area)
        layout.addWidget(layer_group)
        
        # 图层顺序组
        order_group = QGroupBox("图层顺序")
        order_layout = QVBoxLayout(order_group)
        
        self.layer_order_list = QListWidget()
        self.layer_order_list.setMinimumHeight(120)
        order_layout.addWidget(self.layer_order_list)
        
        order_btn_layout = QHBoxLayout()
        self.move_up_btn = QPushButton("↑")
        self.move_down_btn = QPushButton("↓")
        self.move_top_btn = QPushButton("置顶")
        self.move_bottom_btn = QPushButton("置底")
        
        order_btn_layout.addWidget(self.move_up_btn)
        order_btn_layout.addWidget(self.move_down_btn)
        order_btn_layout.addWidget(self.move_top_btn)
        order_btn_layout.addWidget(self.move_bottom_btn)
        order_layout.addLayout(order_btn_layout)
        
        layout.addWidget(order_group)
        layout.addStretch()
    
    def setupConnections(self):
        """设置信号连接"""
        self.move_up_btn.clicked.connect(self.moveLayerUpRequested.emit)
        self.move_down_btn.clicked.connect(self.moveLayerDownRequested.emit)
        self.move_top_btn.clicked.connect(self.moveLayerToTopRequested.emit)
        self.move_bottom_btn.clicked.connect(self.moveLayerToBottomRequested.emit)
