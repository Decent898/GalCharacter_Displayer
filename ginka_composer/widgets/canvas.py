#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画布模块
包含高性能的画布组件，用于显示和操作角色
"""

import os
from typing import Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import (
    QPixmap, QPainter, QColor, QPen, QMouseEvent, 
    QWheelEvent, QImage
)

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class Canvas(QWidget):
    """高性能画布组件"""
    characterSelected = pyqtSignal(str)  # instance_id
    characterTransformChanged = pyqtSignal(str)  # instance_id - 当角色变换改变时发出
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.background_pixmap = None
        self.character_instances = {}
        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.drag_start = None
        self.drag_mode = "canvas"  # "canvas" or "character"
        self.selected_instance = None
        
        # 启用鼠标跟踪
        self.setMouseTracking(True)
        
    def setBackgroundImage(self, image_path: str):
        """设置背景图片"""
        if os.path.exists(image_path):
            self.background_pixmap = QPixmap(image_path)
            self.update()
    
    def clearBackground(self):
        """清除背景"""
        self.background_pixmap = None
        self.update()
    
    def addCharacterInstance(self, instance_id: str, instance):
        """添加角色实例"""
        self.character_instances[instance_id] = instance
        self.update()
    
    def removeCharacterInstance(self, instance_id: str):
        """删除角色实例"""
        if instance_id in self.character_instances:
            del self.character_instances[instance_id]
            self.update()
    
    def updateCharacterInstance(self, instance_id: str):
        """更新指定角色实例"""
        self.update()
    
    def setDragMode(self, mode: str):
        """设置拖拽模式"""
        self.drag_mode = mode
    
    def paintEvent(self, event):
        """重绘事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # 填充画布背景为深灰色，便于查看
        painter.fillRect(self.rect(), QColor(60, 60, 60))
        
        # 计算居中偏移
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        # 应用变换
        painter.save()
        painter.translate(center_x + self.offset_x, center_y + self.offset_y)
        painter.scale(self.scale_factor, self.scale_factor)
        
        # 绘制背景图片（居中）
        if self.background_pixmap:
            bg_x = -self.background_pixmap.width() // 2
            bg_y = -self.background_pixmap.height() // 2
            painter.drawPixmap(bg_x, bg_y, self.background_pixmap)
        
        # 绘制所有角色实例，按z_order从小到大排序
        sorted_instances = sorted(self.character_instances.values(), key=lambda x: x.z_order)
        for instance in sorted_instances:
            if instance.visible:
                self.drawCharacterInstance(painter, instance)
        
        painter.restore()
        
        # 绘制网格线辅助对齐
        self.drawGrid(painter)
    
    def drawGrid(self, painter: QPainter):
        """绘制网格线"""
        painter.save()
        painter.setPen(QPen(QColor(100, 100, 100), 1, Qt.PenStyle.DashLine))
        
        # 绘制中心十字线
        center_x = int(self.width() // 2 + self.offset_x)
        center_y = int(self.height() // 2 + self.offset_y)
        
        painter.drawLine(0, center_y, self.width(), center_y)  # 水平中心线
        painter.drawLine(center_x, 0, center_x, self.height())  # 垂直中心线
        
        painter.restore()
    
    def drawCharacterInstance(self, painter: QPainter, instance):
        """绘制角色实例"""
        painter.save()
        
        # 应用实例变换
        painter.translate(instance.x_offset, instance.y_offset)
        painter.scale(instance.scale, instance.scale)
        
        # 按顺序绘制图层
        for layer_id in instance.layer_order:
            if layer_id in instance.composition_layers and layer_id in instance.layer_images:
                layer = instance.composition_layers[layer_id]
                image = instance.layer_images[layer_id]
                
                # 转换PIL图像为QPixmap
                pixmap = self.pilToQPixmap(image)
                if pixmap:
                    x, y = layer['position']
                    painter.drawPixmap(x, y, pixmap)
        
        painter.restore()
    
    def pilToQPixmap(self, pil_image):
        """将PIL图像转换为QPixmap"""
        try:
            # 转换为RGBA模式
            if pil_image.mode != 'RGBA':
                pil_image = pil_image.convert('RGBA')
            
            # 获取图像数据
            data = pil_image.tobytes('raw', 'RGBA')
            width, height = pil_image.size
            
            # 创建QImage，然后转换为QPixmap
            qimage = QImage(data, width, height, QImage.Format.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimage)
            return pixmap
            
        except Exception as e:
            print(f"图像转换失败: {e}")
            return None
    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start = event.position().toPoint()
            
            if self.drag_mode == "character":
                # 查找点击的角色
                canvas_pos = self.screenToCanvas(event.position().toPoint())
                self.selected_instance = self.findCharacterAt(canvas_pos)
                if self.selected_instance:
                    self.characterSelected.emit(self.selected_instance)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件"""
        if self.drag_start is not None and event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.position().toPoint() - self.drag_start
            
            if self.drag_mode == "canvas":
                # 拖拽画布
                self.offset_x += delta.x()
                self.offset_y += delta.y()
                self.update()
            elif self.drag_mode == "character" and self.selected_instance:
                # 移动角色
                instance = self.character_instances.get(self.selected_instance)
                if instance:
                    instance.x_offset += delta.x() / self.scale_factor
                    instance.y_offset += delta.y() / self.scale_factor
                    self.update()
                    # 发出角色变换改变信号
                    self.characterTransformChanged.emit(self.selected_instance)
            
            self.drag_start = event.position().toPoint()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        # 如果刚刚拖动了角色，发出最终的变换改变信号
        if self.drag_mode == "character" and self.selected_instance:
            self.characterTransformChanged.emit(self.selected_instance)
        
        self.drag_start = None
        self.selected_instance = None
    
    def wheelEvent(self, event: QWheelEvent):
        """鼠标滚轮事件"""
        # 缩放画布
        zoom_in = event.angleDelta().y() > 0
        zoom_factor = 1.1 if zoom_in else 0.9
        
        old_scale = self.scale_factor
        self.scale_factor = max(0.1, min(5.0, self.scale_factor * zoom_factor))
        
        # 保持鼠标位置为缩放中心
        mouse_pos = event.position().toPoint()
        scale_delta = self.scale_factor / old_scale
        
        self.offset_x = mouse_pos.x() - (mouse_pos.x() - self.offset_x) * scale_delta
        self.offset_y = mouse_pos.y() - (mouse_pos.y() - self.offset_y) * scale_delta
        
        self.update()
    
    def screenToCanvas(self, screen_pos: QPoint) -> QPoint:
        """屏幕坐标转画布坐标"""
        center_x = self.width() // 2
        center_y = self.height() // 2
        canvas_x = (screen_pos.x() - center_x - self.offset_x) / self.scale_factor
        canvas_y = (screen_pos.y() - center_y - self.offset_y) / self.scale_factor
        return QPoint(int(canvas_x), int(canvas_y))
    
    def findCharacterAt(self, pos: QPoint) -> Optional[str]:
        """查找指定位置的角色"""
        # 从上到下查找（逆序）
        for instance in reversed(list(self.character_instances.values())):
            if instance.visible and self.pointInInstance(pos, instance):
                return instance.instance_id
        return None
    
    def pointInInstance(self, pos: QPoint, instance) -> bool:
        """检查点是否在角色实例范围内"""
        bounds = self.calculateInstanceBounds(instance)
        return bounds[0] <= pos.x() <= bounds[2] and bounds[1] <= pos.y() <= bounds[3]
    
    def calculateInstanceBounds(self, instance) -> tuple:
        """计算角色实例的边界"""
        if not instance.composition_layers:
            return (0, 0, 0, 0)
        
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')
        
        # 考虑居中偏移
        center_offset_x = 0  # 背景图片已经在绘制时居中
        center_offset_y = 0
        
        for layer_id, layer in instance.composition_layers.items():
            x, y = layer['position']
            width, height = layer['size']
            
            final_x = (x + center_offset_x) * instance.scale + instance.x_offset
            final_y = (y + center_offset_y) * instance.scale + instance.y_offset
            scaled_width = width * instance.scale
            scaled_height = height * instance.scale
            
            min_x = min(min_x, final_x)
            min_y = min(min_y, final_y)
            max_x = max(max_x, final_x + scaled_width)
            max_y = max(max_y, final_y + scaled_height)
        
        return (min_x, min_y, max_x, max_y)
