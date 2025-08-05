#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强的图层复选框
支持右键菜单和自定义组件编辑
"""

from PyQt6.QtWidgets import QMenu, QWidget
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction

from . import PreviewableCheckBox


class LayerCheckBox(PreviewableCheckBox):
    """支持右键菜单的图层复选框"""
    
    cloneRequested = pyqtSignal(dict)  # 克隆请求信号
    
    def __init__(self, text, layer_data):
        super().__init__(text, layer_data)
        self.layer_data = layer_data
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu(self)
        
        # 克隆后修改动作
        clone_action = QAction("克隆后修改", self)
        clone_action.setToolTip("创建此组件的副本并打开编辑器进行自定义修改")
        clone_action.triggered.connect(lambda: self.cloneRequested.emit(self.layer_data))
        menu.addAction(clone_action)
        
        # 显示菜单
        global_pos = self.mapToGlobal(position)
        menu.exec(global_pos)
