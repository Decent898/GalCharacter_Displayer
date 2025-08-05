#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据模型模块
包含角色实例和相关数据结构
"""

import uuid
from typing import Dict, List, Optional
from PyQt6.QtCore import QThread, pyqtSignal

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
