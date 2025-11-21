#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义部件数据模型
"""

from dataclasses import dataclass
from typing import Optional, List
from PIL import Image


@dataclass
class CustomComponent:
    """自定义部件数据类"""
    name: str  # 部件名称
    image_path: str  # 图片路径
    x: int = 0  # X偏移
    y: int = 0  # Y偏移
    scale: float = 1.0  # 缩放
    z_index: int = 0  # 层级
    visible: bool = True  # 是否可见
    image: Optional[Image.Image] = None  # PIL图像对象
    
    def __post_init__(self):
        """初始化后处理"""
        if self.image is None and self.image_path:
            try:
                self.image = Image.open(self.image_path).convert("RGBA")
            except Exception as e:
                print(f"加载自定义部件图片失败: {e}")
                self.image = None
    
    def get_bounds(self) -> tuple:
        """获取部件边界框"""
        if not self.image:
            return (0, 0, 0, 0)
        
        width = int(self.image.width * self.scale)
        height = int(self.image.height * self.scale)
        return (self.x, self.y, self.x + width, self.y + height)
    
    def contains_point(self, x: int, y: int) -> bool:
        """检查点是否在部件内"""
        bounds = self.get_bounds()
        return bounds[0] <= x <= bounds[2] and bounds[1] <= y <= bounds[3]


class CharacterCustomComponents:
    """角色自定义部件管理器"""
    
    def __init__(self):
        self.components: List[CustomComponent] = []
        self._next_z_index = 10000  # 自定义部件的起始z值，设为较大值以显示在图层之上
    
    def add_component(self, name: str, image_path: str, z_index: Optional[int] = None) -> CustomComponent:
        """添加自定义部件"""
        if z_index is None:
            z_index = self._next_z_index
            self._next_z_index += 1
            
        component = CustomComponent(
            name=name,
            image_path=image_path,
            z_index=z_index
        )
        self.components.append(component)
        return component
    
    def remove_component(self, component: CustomComponent):
        """移除自定义部件"""
        if component in self.components:
            self.components.remove(component)
    
    def remove_component_by_name(self, name: str):
        """通过名称移除自定义部件"""
        self.components = [c for c in self.components if c.name != name]
    
    def get_component_by_name(self, name: str) -> Optional[CustomComponent]:
        """通过名称获取部件"""
        for component in self.components:
            if component.name == name:
                return component
        return None
    
    def get_components_sorted_by_z(self) -> List[CustomComponent]:
        """按z-index排序获取部件列表"""
        return sorted(self.components, key=lambda c: c.z_index)
    
    def move_component_up(self, component: CustomComponent):
        """将部件向上移动一层"""
        component.z_index += 1
    
    def move_component_down(self, component: CustomComponent):
        """将部件向下移动一层"""
        component.z_index = max(0, component.z_index - 1)
    
    def move_component_to_front(self, component: CustomComponent):
        """将部件移到最前"""
        max_z = max([c.z_index for c in self.components], default=0)
        component.z_index = max_z + 1
        self._next_z_index = max(self._next_z_index, component.z_index + 1)
    
    def move_component_to_back(self, component: CustomComponent):
        """将部件移到最后"""
        min_z = min([c.z_index for c in self.components], default=0)
        component.z_index = min_z - 1
    
    def set_component_z_index(self, component: CustomComponent, z_index: int):
        """设置部件的z索引"""
        component.z_index = z_index
        # 更新next_z_index以避免冲突
        max_z = max([c.z_index for c in self.components], default=0)
        self._next_z_index = max(self._next_z_index, max_z + 1)
    
    def get_component_at_position(self, x: int, y: int) -> Optional[CustomComponent]:
        """获取指定位置的最顶层部件"""
        # 按z-index从大到小排序，找到最顶层的
        sorted_components = sorted(
            [c for c in self.components if c.visible],
            key=lambda c: c.z_index,
            reverse=True
        )
        
        for component in sorted_components:
            if component.contains_point(x, y):
                return component
        return None
    
    def get_z_index_range(self) -> tuple:
        """获取当前部件的z_index范围"""
        if not self.components:
            return (self._next_z_index, self._next_z_index)
        
        min_z = min([c.z_index for c in self.components])
        max_z = max([c.z_index for c in self.components])
        return (min_z, max_z)
    
    def clear_all(self):
        """清空所有部件"""
        self.components.clear()
        self._next_z_index = 10000
    
    def to_dict(self) -> dict:
        """转换为字典格式（用于保存）"""
        return {
            'components': [
                {
                    'name': c.name,
                    'image_path': c.image_path,
                    'x': c.x,
                    'y': c.y,
                    'scale': c.scale,
                    'z_index': c.z_index,
                    'visible': c.visible
                }
                for c in self.components
            ]
        }
    
    def from_dict(self, data: dict):
        """从字典格式加载（用于加载）"""
        self.components.clear()
        
        for comp_data in data.get('components', []):
            component = CustomComponent(
                name=comp_data['name'],
                image_path=comp_data['image_path'],
                x=comp_data.get('x', 0),
                y=comp_data.get('y', 0),
                scale=comp_data.get('scale', 1.0),
                z_index=comp_data.get('z_index', 0),
                visible=comp_data.get('visible', True)
            )
            self.components.append(component)
        
        # 更新下一个z_index
        if self.components:
            self._next_z_index = max([c.z_index for c in self.components]) + 1
        else:
            self._next_z_index = 1000
