#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标签页组件
包含场景、角色、图层三个标签页的实现
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QComboBox,
    QPushButton, QScrollArea, QButtonGroup, QRadioButton, QListWidget,
    QSpinBox, QDoubleSpinBox, QSlider, QFrame, QFileDialog, QMessageBox,
    QListWidgetItem, QTabWidget
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
    exportCharacterOnlyRequested = pyqtSignal()
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
        self.export_character_btn = QPushButton("导出立牌")
        self.export_character_btn.setStyleSheet("QPushButton { background-color: #17a2b8; color: white; } QPushButton:hover { background-color: #138496; }")
        self.save_scene_btn = QPushButton("保存场景")
        self.load_scene_btn = QPushButton("加载场景")
        
        file_layout.addWidget(self.export_btn)
        file_layout.addWidget(self.export_hd_btn)
        file_layout.addWidget(self.export_character_btn)
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
        self.export_character_btn.clicked.connect(self.exportCharacterOnlyRequested.emit)
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
    
    # 自定义部件信号
    addCustomComponentRequested = pyqtSignal(str)  # image_path
    removeCustomComponentRequested = pyqtSignal(str)  # component_name
    customComponentSelected = pyqtSignal(str)  # component_name
    customComponentTransformChanged = pyqtSignal(str, int, int, float)  # name, x, y, scale
    moveCustomComponentRequested = pyqtSignal(str, str)  # component_name, direction ('up', 'down', 'front', 'back')
    
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setupConnections()
    
    def setupUI(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 创建子标签页
        self.tab_widget = QTabWidget()
        
        # 角色管理标签页
        character_tab = QWidget()
        self.setupCharacterTab(character_tab)
        self.tab_widget.addTab(character_tab, "角色管理")
        
        # 自定义部件标签页
        component_tab = QWidget()
        self.setupCustomComponentTab(component_tab)
        self.tab_widget.addTab(component_tab, "自定义部件")
        
        layout.addWidget(self.tab_widget)
    
    def setupCharacterTab(self, parent):
        """设置角色管理标签页"""
        layout = QVBoxLayout(parent)
        
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
        self.x_spinbox.setRange(-2000, 2000)
        x_layout.addWidget(self.x_slider)
        x_layout.addWidget(self.x_spinbox)
        transform_layout.addLayout(x_layout)
        
        # Y偏移
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Y:"))
        self.y_slider = QSlider(Qt.Orientation.Horizontal)
        self.y_slider.setRange(-1000, 1000)
        self.y_spinbox = QSpinBox()
        self.y_spinbox.setRange(-2000, 2000)
        y_layout.addWidget(self.y_slider)
        y_layout.addWidget(self.y_spinbox)
        transform_layout.addLayout(y_layout)
        
        # 缩放
        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("缩放:"))
        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setRange(1, 1000)  # 0.01 to 10.0
        self.scale_slider.setValue(100)
        self.scale_spinbox = QDoubleSpinBox()
        self.scale_spinbox.setRange(0.01, 20.0)
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
    
    def setupCustomComponentTab(self, parent):
        """设置自定义部件标签页"""
        layout = QVBoxLayout(parent)
        
        # 提示信息组
        info_group = QGroupBox("使用说明")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel("""
<b>自定义部件功能：</b><br>
• 自定义部件与具体的角色实例绑定<br>
• 请先在"角色管理"标签页选择一个角色实例<br>
• 然后在此页面为该角色添加自定义图片部件<br>
• 可以调整部件的位置、缩放和层级
        """)
        info_text.setWordWrap(True)
        info_text.setStyleSheet("color: #555; font-size: 11px; padding: 10px;")
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_group)
        
        # 当前角色显示组
        current_group = QGroupBox("当前选中角色")
        current_layout = QVBoxLayout(current_group)
        
        self.current_character_label = QLabel("未选择角色")
        self.current_character_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
                color: #6c757d;
            }
        """)
        current_layout.addWidget(self.current_character_label)
        
        layout.addWidget(current_group)
        
        # 添加部件组
        add_comp_group = QGroupBox("添加自定义部件")
        add_comp_layout = QVBoxLayout(add_comp_group)
        
        # 说明文字
        info_label = QLabel("为当前角色添加自定义图片部件")
        info_label.setStyleSheet("color: #666; font-size: 11px;")
        add_comp_layout.addWidget(info_label)
        
        # 添加按钮
        self.add_component_btn = QPushButton("选择图片文件")
        self.add_component_btn.setMinimumHeight(35)
        self.add_component_btn.setEnabled(False)  # 默认禁用
        self.add_component_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #dee2e6;
            }
        """)
        add_comp_layout.addWidget(self.add_component_btn)
        
        layout.addWidget(add_comp_group)
        
        # 部件列表组
        comp_list_group = QGroupBox("角色的自定义部件")
        comp_list_layout = QVBoxLayout(comp_list_group)
        
        self.component_list = QListWidget()
        self.component_list.setMinimumHeight(150)
        self.component_list.setEnabled(False)  # 默认禁用
        comp_list_layout.addWidget(self.component_list)
        
        # 部件操作按钮
        comp_btn_layout = QHBoxLayout()
        self.remove_component_btn = QPushButton("删除部件")
        self.clear_components_btn = QPushButton("清空所有")
        self.remove_component_btn.setEnabled(False)
        self.clear_components_btn.setEnabled(False)
        comp_btn_layout.addWidget(self.remove_component_btn)
        comp_btn_layout.addWidget(self.clear_components_btn)
        comp_list_layout.addLayout(comp_btn_layout)
        
        layout.addWidget(comp_list_group)
        
        # 部件变换控制组
        comp_transform_group = QGroupBox("部件位置和缩放")
        comp_transform_layout = QVBoxLayout(comp_transform_group)
        
        # X偏移
        comp_x_layout = QHBoxLayout()
        comp_x_layout.addWidget(QLabel("X:"))
        self.comp_x_slider = QSlider(Qt.Orientation.Horizontal)
        self.comp_x_slider.setRange(-1000, 1000)
        self.comp_x_slider.setEnabled(False)
        self.comp_x_spinbox = QSpinBox()
        self.comp_x_spinbox.setRange(-2000, 2000)
        self.comp_x_spinbox.setEnabled(False)
        comp_x_layout.addWidget(self.comp_x_slider)
        comp_x_layout.addWidget(self.comp_x_spinbox)
        comp_transform_layout.addLayout(comp_x_layout)
        
        # Y偏移
        comp_y_layout = QHBoxLayout()
        comp_y_layout.addWidget(QLabel("Y:"))
        self.comp_y_slider = QSlider(Qt.Orientation.Horizontal)
        self.comp_y_slider.setRange(-1000, 1000)
        self.comp_y_slider.setEnabled(False)
        self.comp_y_spinbox = QSpinBox()
        self.comp_y_spinbox.setRange(-2000, 2000)
        self.comp_y_spinbox.setEnabled(False)
        comp_y_layout.addWidget(self.comp_y_slider)
        comp_y_layout.addWidget(self.comp_y_spinbox)
        comp_transform_layout.addLayout(comp_y_layout)
        
        # 缩放
        comp_scale_layout = QHBoxLayout()
        comp_scale_layout.addWidget(QLabel("缩放:"))
        self.comp_scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.comp_scale_slider.setRange(1, 1000)  # 0.01 to 10.0
        self.comp_scale_slider.setValue(100)
        self.comp_scale_slider.setEnabled(False)
        self.comp_scale_spinbox = QDoubleSpinBox()
        self.comp_scale_spinbox.setRange(0.01, 20.0)
        self.comp_scale_spinbox.setValue(1.0)
        self.comp_scale_spinbox.setSingleStep(0.01)
        self.comp_scale_spinbox.setEnabled(False)
        comp_scale_layout.addWidget(self.comp_scale_slider)
        comp_scale_layout.addWidget(self.comp_scale_spinbox)
        comp_transform_layout.addLayout(comp_scale_layout)
        
        layout.addWidget(comp_transform_group)
        
        # 部件层级控制组
        comp_zorder_group = QGroupBox("部件层级")
        comp_zorder_layout = QVBoxLayout(comp_zorder_group)
        
        # 层级调整按钮
        comp_zorder_btn_layout = QHBoxLayout()
        self.comp_move_up_btn = QPushButton("上移一层")
        self.comp_move_down_btn = QPushButton("下移一层")
        self.comp_move_up_btn.setEnabled(False)
        self.comp_move_down_btn.setEnabled(False)
        comp_zorder_btn_layout.addWidget(self.comp_move_down_btn)
        comp_zorder_btn_layout.addWidget(self.comp_move_up_btn)
        comp_zorder_layout.addLayout(comp_zorder_btn_layout)
        
        comp_zorder_btn_layout2 = QHBoxLayout()
        self.comp_move_front_btn = QPushButton("移到最前")
        self.comp_move_back_btn = QPushButton("移到最后")
        self.comp_move_front_btn.setEnabled(False)
        self.comp_move_back_btn.setEnabled(False)
        comp_zorder_btn_layout2.addWidget(self.comp_move_back_btn)
        comp_zorder_btn_layout2.addWidget(self.comp_move_front_btn)
        comp_zorder_layout.addLayout(comp_zorder_btn_layout2)
        
        layout.addWidget(comp_zorder_group)
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
        self.x_spinbox.valueChanged.connect(self.onXSpinboxChanged)
        self.y_slider.valueChanged.connect(self.y_spinbox.setValue)
        self.y_spinbox.valueChanged.connect(self.onYSpinboxChanged)
        
        # 缩放滑块和输入框的同步
        self.scale_slider.valueChanged.connect(self.onScaleSliderChanged)
        self.scale_spinbox.valueChanged.connect(self.onScaleSpinboxChanged)
        
        self.x_spinbox.valueChanged.connect(self.transformChanged.emit)
        self.y_spinbox.valueChanged.connect(self.transformChanged.emit)
        self.scale_spinbox.valueChanged.connect(self.transformChanged.emit)
        
        self.reset_transform_btn.clicked.connect(self.resetTransformRequested.emit)
        
        # 角色层级控制
        self.move_forward_btn.clicked.connect(self.moveCharacterForwardRequested.emit)
        self.move_backward_btn.clicked.connect(self.moveCharacterBackwardRequested.emit)
        self.move_front_btn.clicked.connect(self.moveCharacterToFrontRequested.emit)
        self.move_back_btn.clicked.connect(self.moveCharacterToBackRequested.emit)
        
        # 自定义部件信号连接
        self.add_component_btn.clicked.connect(self.onAddCustomComponent)
        self.remove_component_btn.clicked.connect(self.onRemoveCustomComponent)
        self.clear_components_btn.clicked.connect(self.onClearCustomComponents)
        self.component_list.currentRowChanged.connect(self.onCustomComponentSelected)
        
        # 自定义部件变换控制连接
        self.comp_x_slider.valueChanged.connect(self.comp_x_spinbox.setValue)
        self.comp_x_spinbox.valueChanged.connect(self.onCustomComponentXSpinboxChanged)
        self.comp_y_slider.valueChanged.connect(self.comp_y_spinbox.setValue)
        self.comp_y_spinbox.valueChanged.connect(self.onCustomComponentYSpinboxChanged)
        self.comp_scale_slider.valueChanged.connect(self.onCustomComponentScaleSliderChanged)
        self.comp_scale_spinbox.valueChanged.connect(self.onCustomComponentScaleSpinboxChanged)
        
        self.comp_x_spinbox.valueChanged.connect(self.onCustomComponentTransformChanged)
        self.comp_y_spinbox.valueChanged.connect(self.onCustomComponentTransformChanged)
        self.comp_scale_spinbox.valueChanged.connect(self.onCustomComponentTransformChanged)
        
        # 自定义部件层级控制
        self.comp_move_up_btn.clicked.connect(lambda: self.onMoveCustomComponent('up'))
        self.comp_move_down_btn.clicked.connect(lambda: self.onMoveCustomComponent('down'))
        self.comp_move_front_btn.clicked.connect(lambda: self.onMoveCustomComponent('front'))
        self.comp_move_back_btn.clicked.connect(lambda: self.onMoveCustomComponent('back'))
    
    def onAddCustomComponent(self):
        """添加自定义部件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片文件",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)"
        )
        
        if file_path:
            self.addCustomComponentRequested.emit(file_path)
    
    def onRemoveCustomComponent(self):
        """删除选中的自定义部件"""
        current_item = self.component_list.currentItem()
        if current_item:
            component_name = current_item.text()
            self.removeCustomComponentRequested.emit(component_name)
    
    def onClearCustomComponents(self):
        """清空所有自定义部件"""
        reply = QMessageBox.question(
            self, 
            "确认清空", 
            "确定要删除所有自定义部件吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            for i in range(self.component_list.count()):
                item = self.component_list.item(i)
                if item:
                    self.removeCustomComponentRequested.emit(item.text())
    
    def onCustomComponentSelected(self, row):
        """自定义部件选择事件"""
        if row >= 0:
            item = self.component_list.item(row)
            if item:
                self.customComponentSelected.emit(item.text())
                # 启用变换控件
                self.enableCustomComponentTransformControls(True)
        else:
            # 禁用变换控件
            self.enableCustomComponentTransformControls(False)
    
    def onScaleSliderChanged(self, value):
        """角色缩放滑块变化"""
        scale_value = value / 100.0  # 1-1000 映射到 0.01-10.0
        self.scale_spinbox.setValue(scale_value)
    
    def onScaleSpinboxChanged(self, value):
        """角色缩放输入框变化"""
        slider_value = int(value * 100)  # 0.01-10.0 映射到 1-1000
        # 如果超出滑块范围，只更新到边界值
        slider_value = max(1, min(1000, slider_value))
        self.scale_slider.setValue(slider_value)
    
    def onXSpinboxChanged(self, value):
        """X位置输入框变化"""
        # 如果在滑块范围内，同步滑块
        if -1000 <= value <= 1000:
            self.x_slider.setValue(value)
    
    def onYSpinboxChanged(self, value):
        """Y位置输入框变化"""
        # 如果在滑块范围内，同步滑块
        if -1000 <= value <= 1000:
            self.y_slider.setValue(value)
    
    def onCustomComponentScaleSliderChanged(self, value):
        """自定义部件缩放滑块变化"""
        scale_value = value / 100.0  # 1-1000 映射到 0.01-10.0
        self.comp_scale_spinbox.setValue(scale_value)
    
    def onCustomComponentScaleSpinboxChanged(self, value):
        """自定义部件缩放输入框变化"""
        slider_value = int(value * 100)  # 0.01-10.0 映射到 1-1000
        # 如果超出滑块范围，只更新到边界值
        slider_value = max(1, min(1000, slider_value))
        self.comp_scale_slider.setValue(slider_value)
    
    def onCustomComponentXSpinboxChanged(self, value):
        """自定义部件X位置输入框变化"""
        # 如果在滑块范围内，同步滑块
        if -1000 <= value <= 1000:
            self.comp_x_slider.setValue(value)
    
    def onCustomComponentYSpinboxChanged(self, value):
        """自定义部件Y位置输入框变化"""
        # 如果在滑块范围内，同步滑块
        if -1000 <= value <= 1000:
            self.comp_y_slider.setValue(value)
    
    def onCustomComponentTransformChanged(self):
        """自定义部件变换改变"""
        current_item = self.component_list.currentItem()
        if current_item:
            component_name = current_item.text()
            self.customComponentTransformChanged.emit(
                component_name,
                self.comp_x_spinbox.value(),
                self.comp_y_spinbox.value(),
                self.comp_scale_spinbox.value()
            )
    
    def onMoveCustomComponent(self, direction):
        """移动自定义部件层级"""
        current_item = self.component_list.currentItem()
        if current_item:
            component_name = current_item.text()
            self.moveCustomComponentRequested.emit(component_name, direction)
    
    def updateCustomComponentTransform(self, x, y, scale):
        """更新自定义部件变换控件"""
        self.comp_x_spinbox.setValue(x)
        self.comp_y_spinbox.setValue(y)
        self.comp_scale_spinbox.setValue(scale)
    
    def addCustomComponentToList(self, component_name):
        """添加自定义部件到列表"""
        self.component_list.addItem(component_name)
    
    def removeCustomComponentFromList(self, component_name):
        """从列表中移除自定义部件"""
        for i in range(self.component_list.count()):
            item = self.component_list.item(i)
            if item and item.text() == component_name:
                self.component_list.takeItem(i)
                break
    
    def setCurrentCharacterInstance(self, instance):
        """设置当前角色实例，更新自定义部件UI状态"""
        # 更新当前角色显示
        if instance:
            self.current_character_label.setText(f"角色: {instance.name}")
            self.current_character_label.setStyleSheet("""
                QLabel {
                    background-color: #d4edda;
                    border: 1px solid #c3e6cb;
                    border-radius: 4px;
                    padding: 8px;
                    font-weight: bold;
                    color: #155724;
                }
            """)
            
            # 启用所有自定义部件控件
            self.add_component_btn.setEnabled(True)
            self.component_list.setEnabled(True)
            self.remove_component_btn.setEnabled(True)
            self.clear_components_btn.setEnabled(True)
            
            # 更新部件列表
            self.component_list.clear()
            if hasattr(instance, 'custom_components'):
                for component in instance.custom_components.components:
                    self.addCustomComponentToList(component.name)
            
        else:
            self.current_character_label.setText("未选择角色")
            self.current_character_label.setStyleSheet("""
                QLabel {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 4px;
                    padding: 8px;
                    font-weight: bold;
                    color: #6c757d;
                }
            """)
            
            # 禁用所有自定义部件控件
            self.add_component_btn.setEnabled(False)
            self.component_list.setEnabled(False)
            self.remove_component_btn.setEnabled(False)
            self.clear_components_btn.setEnabled(False)
            self.enableCustomComponentTransformControls(False)
            
            # 清空部件列表
            self.component_list.clear()
    
    def enableCustomComponentTransformControls(self, enable: bool):
        """启用/禁用自定义部件变换控件"""
        self.comp_x_slider.setEnabled(enable)
        self.comp_x_spinbox.setEnabled(enable)
        self.comp_y_slider.setEnabled(enable)
        self.comp_y_spinbox.setEnabled(enable)
        self.comp_scale_slider.setEnabled(enable)
        self.comp_scale_spinbox.setEnabled(enable)
        self.comp_move_up_btn.setEnabled(enable)
        self.comp_move_down_btn.setEnabled(enable)
        self.comp_move_front_btn.setEnabled(enable)
        self.comp_move_back_btn.setEnabled(enable)


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
