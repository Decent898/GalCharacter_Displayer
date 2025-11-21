#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据模型模块
包含角色实例和相关数据结构
"""

import uuid
from typing import Dict, List, Optional
from PyQt6.QtCore import QThread, pyqtSignal
from .custom_component import CharacterCustomComponents

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class CharacterInstance:
    """角色实例类 - 管理单个角色的状态和属性"""
    
    def __init__(self, character_name: str, size: str):
        self.instance_id = str(uuid.uuid4())  # 唯一实例ID
        self.character_name = character_name
        self.size = size
        self.name = f"{character_name}_{size}_{self.instance_id[:8]}"
        
        # 图层相关
        self.layer_images: Dict[int, Image.Image] = {}
        self.composition_layers: Dict[int, dict] = {}
        self.layer_order: List[int] = []
        
        # 变换属性
        self.x_offset: float = 0.0
        self.y_offset: float = 0.0
        self.scale: float = 1.0
        
        # 显示属性
        self.visible: bool = True
        self.z_order: int = 0  # 角色层级，数值越大越在前面
        
        # 自定义部件管理器
        self.custom_components = CharacterCustomComponents()
    
    def to_dict(self) -> dict:
        """转换为字典格式（用于保存）"""
        # 转换composition_layers的键为字符串（JSON兼容）
        composition_layers_str = {}
        for k, v in self.composition_layers.items():
            composition_layers_str[str(k)] = v
        
        # 确保layer_order包含所有composition_layers中的图层
        all_layer_ids = list(self.composition_layers.keys())
        # 保持原有顺序，添加缺失的图层
        complete_layer_order = []
        for layer_id in self.layer_order:
            if layer_id in all_layer_ids:
                complete_layer_order.append(layer_id)
        # 添加不在layer_order中的图层
        for layer_id in all_layer_ids:
            if layer_id not in complete_layer_order:
                complete_layer_order.append(layer_id)
        
        return {
            'instance_id': self.instance_id,
            'character_name': self.character_name,
            'size': self.size,
            'name': self.name,
            'x_offset': self.x_offset,
            'y_offset': self.y_offset,
            'scale': self.scale,
            'visible': self.visible,
            'z_order': self.z_order,
            'layer_order': complete_layer_order,  # 保存完整的图层顺序
            'composition_layers': composition_layers_str,  # 保存完整的图层信息
            'custom_components': self.custom_components.to_dict()
        }
    
    def from_dict(self, data: dict):
        """从字典格式加载（用于加载）"""
        self.instance_id = data.get('instance_id', self.instance_id)
        self.character_name = data.get('character_name', self.character_name)
        self.size = data.get('size', self.size)
        self.name = data.get('name', self.name)
        self.x_offset = data.get('x_offset', 0.0)
        self.y_offset = data.get('y_offset', 0.0)
        self.scale = data.get('scale', 1.0)
        self.visible = data.get('visible', True)
        self.z_order = data.get('z_order', 0)
        
        # 加载图层顺序，确保转换为整数
        raw_layer_order = data.get('layer_order', [])
        self.layer_order = []
        for layer_id in raw_layer_order:
            try:
                int_id = int(layer_id)
                self.layer_order.append(int_id)
            except (ValueError, TypeError):
                # 如果转换失败，跳过这个图层ID
                continue
        
        # 加载图层信息，转换字符串键回整数
        if 'composition_layers' in data:
            self.composition_layers = {}
            for k, v in data['composition_layers'].items():
                try:
                    # 尝试转换为整数
                    int_key = int(k)
                    self.composition_layers[int_key] = v
                except ValueError:
                    # 如果转换失败，保持为字符串（向后兼容）
                    self.composition_layers[k] = v
        
        # 加载自定义部件
        if 'custom_components' in data:
            self.custom_components.from_dict(data['custom_components'])
        
        # 确保layer_order包含所有composition_layers中的图层
        if self.composition_layers:
            all_layer_ids = list(self.composition_layers.keys())
            # 添加不在layer_order中的图层到末尾
            for layer_id in all_layer_ids:
                if layer_id not in self.layer_order:
                    self.layer_order.append(layer_id)


class ImageLoader(QThread):
    """异步图像加载器"""
    imageLoaded = pyqtSignal(int, object)  # layer_id, PIL.Image
    loadProgress = pyqtSignal(int, int)    # current, total
    
    def __init__(self):
        super().__init__()
        self.tasks = []
        
    def addTask(self, layer_id: int, image_path: str):
        """添加加载任务"""
        self.tasks.append((layer_id, image_path))
    
    def run(self):
        """执行加载任务"""
        total = len(self.tasks)
        for i, (layer_id, image_path) in enumerate(self.tasks):
            try:
                if PIL_AVAILABLE:
                    image = Image.open(image_path)
                    if image.mode != 'RGBA':
                        image = image.convert('RGBA')
                    self.imageLoaded.emit(layer_id, image)
                
                self.loadProgress.emit(i + 1, total)
                
            except Exception as e:
                print(f"加载图像失败 {image_path}: {e}")
        
        self.tasks.clear()
