#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
位置对齐系统 - 根据导入部件类型自动对齐到合适位置
"""

from typing import Dict, List, Tuple, Optional


class PositionAlignmentSystem:
    """位置对齐系统 - 管理导入部件的智能位置对齐"""
    
    # 部件类型定义
    LAYER_TYPES = {
        'costume': '服装',
        'expression': '表情', 
        'accessory': '配饰',
        'custom': '自定义'
    }
    
    # 位置区域定义 (相对于角色中心的偏移)
    POSITION_ZONES = {
        # 服装类 - 一般在身体区域
        'costume': {
            'head': (0, -150),      # 头部装饰 (帽子等)
            'face': (0, -50),       # 面部装饰 (面具等)
            'chest': (0, 20),       # 胸部装饰
            'waist': (0, 80),       # 腰部装饰
            'legs': (0, 150),       # 腿部装饰
            'body': (0, 0),         # 整体服装
            'default': (0, 0)       # 默认位置
        },
        
        # 表情类 - 主要在面部区域
        'expression': {
            'eyes': (0, -80),       # 眼部表情
            'eyebrows': (0, -120),  # 眉毛表情
            'mouth': (0, -20),      # 嘴部表情
            'face': (0, -60),       # 整体面部表情
            'cheeks': (-30, -50),   # 脸颊表情 (左右可能不同)
            'default': (0, -60)     # 默认面部位置
        },
        
        # 配饰类 - 分布在各个位置
        'accessory': {
            'hair': (0, -180),      # 发饰
            'ear': (-40, -100),     # 耳饰
            'neck': (0, -20),       # 颈饰
            'hand': (-80, 50),      # 手饰
            'wrist': (-60, 30),     # 腕饰
            'back': (0, 10),        # 背饰
            'side': (-100, 0),      # 侧面配饰
            'default': (0, -50)     # 默认配饰位置
        },
        
        # 自定义类 - 用户自定义位置
        'custom': {
            'default': (0, 0)       # 中心位置
        }
    }
    
    def __init__(self):
        self.learned_positions: Dict[str, Dict[str, Tuple[int, int]]] = {}
        self.character_analysis_cache: Dict[str, Dict] = {}
    
    def analyzeCharacterLayers(self, character_data: Dict, character_name: str, size: str) -> Dict[str, List[Tuple[int, int]]]:
        """分析角色原始图层，提取各类型部件的典型位置"""
        if character_name not in character_data:
            return {}
        
        cache_key = f"{character_name}_{size}"
        if cache_key in self.character_analysis_cache:
            return self.character_analysis_cache[cache_key]
        
        char_data = character_data[character_name]
        size_data = char_data['layer_mapping'].get(size, {})
        
        # 分析结果
        type_positions = {
            'costume': [],
            'expression': [],
            'accessory': [],
            'other': []
        }
        
        # 收集所有图层
        all_layers = []
        for group_name, group_layers in size_data.items():
            all_layers.extend(group_layers)
        
        # 根据图层名称和位置分类
        for layer in all_layers:
            layer_name = layer['name'].lower()
            position = layer['position']
            
            # 根据名称关键词分类
            if any(keyword in layer_name for keyword in ['服', '衣', '裙', '裤', '袖', '领']):
                type_positions['costume'].append(position)
            elif any(keyword in layer_name for keyword in ['眼', '眉', '嘴', '笑', '哭', '怒', '表情']):
                type_positions['expression'].append(position)
            elif any(keyword in layer_name for keyword in ['饰', '带', '环', '链', '帽', '花']):
                type_positions['accessory'].append(position)
            else:
                type_positions['other'].append(position)
        
        self.character_analysis_cache[cache_key] = type_positions
        return type_positions
    
    def calculateOptimalPosition(self, 
                               layer_type: str, 
                               image_size: Tuple[int, int],
                               character_data: Optional[Dict] = None,
                               character_name: Optional[str] = None,
                               size: Optional[str] = None,
                               layer_name: Optional[str] = None) -> Tuple[int, int]:
        """
        计算导入图层的最佳位置
        
        Args:
            layer_type: 图层类型 ('costume', 'expression', 'accessory', 'custom')
            image_size: 图像尺寸 (width, height)
            character_data: 角色数据（用于分析原有图层位置）
            character_name: 角色名称
            size: 角色尺寸
            layer_name: 图层名称（用于更精确的位置推测）
        
        Returns:
            (x, y) 位置坐标
        """
        # 如果有角色数据，使用智能分析
        if character_data and character_name and size:
            analyzed_positions = self.analyzeCharacterLayers(character_data, character_name, size)
            
            if layer_type in analyzed_positions and analyzed_positions[layer_type]:
                positions = analyzed_positions[layer_type]
                # 计算该类型图层的平均位置
                avg_x = sum(pos[0] for pos in positions) // len(positions)
                avg_y = sum(pos[1] for pos in positions) // len(positions)
                
                # 根据图层名称进行微调
                offset_x, offset_y = self._getNameBasedOffset(layer_name or "", layer_type)
                
                return (avg_x + offset_x, avg_y + offset_y)
        
        # 使用基础位置区域映射
        zone_key = self._inferZoneFromName(layer_name or "", layer_type)
        base_offset = self.POSITION_ZONES[layer_type].get(zone_key, 
                                                         self.POSITION_ZONES[layer_type]['default'])
        
        # 根据图像尺寸调整位置（居中对齐）
        img_width, img_height = image_size
        adjusted_x = base_offset[0] - img_width // 2
        adjusted_y = base_offset[1] - img_height // 2
        
        return (adjusted_x, adjusted_y)
    
    def _inferZoneFromName(self, layer_name: str, layer_type: str) -> str:
        """根据图层名称推断位置区域"""
        if not layer_name:
            return 'default'
        
        name_lower = layer_name.lower()
        
        if layer_type == 'costume':
            if any(keyword in name_lower for keyword in ['帽', '头', 'hat', 'head']):
                return 'head'
            elif any(keyword in name_lower for keyword in ['面', '脸', 'face', 'mask']):
                return 'face'
            elif any(keyword in name_lower for keyword in ['胸', 'chest', 'top']):
                return 'chest'
            elif any(keyword in name_lower for keyword in ['腰', 'waist', 'belt']):
                return 'waist'
            elif any(keyword in name_lower for keyword in ['腿', 'leg', 'pants', 'skirt']):
                return 'legs'
            else:
                return 'body'
        
        elif layer_type == 'expression':
            if any(keyword in name_lower for keyword in ['眼', 'eye']):
                return 'eyes'
            elif any(keyword in name_lower for keyword in ['眉', 'brow']):
                return 'eyebrows'
            elif any(keyword in name_lower for keyword in ['嘴', 'mouth', 'lip']):
                return 'mouth'
            elif any(keyword in name_lower for keyword in ['脸', 'cheek']):
                return 'cheeks'
            else:
                return 'face'
        
        elif layer_type == 'accessory':
            if any(keyword in name_lower for keyword in ['发', 'hair']):
                return 'hair'
            elif any(keyword in name_lower for keyword in ['耳', 'ear']):
                return 'ear'
            elif any(keyword in name_lower for keyword in ['颈', 'neck']):
                return 'neck'
            elif any(keyword in name_lower for keyword in ['手', 'hand']):
                return 'hand'
            elif any(keyword in name_lower for keyword in ['腕', 'wrist']):
                return 'wrist'
            elif any(keyword in name_lower for keyword in ['背', 'back']):
                return 'back'
            else:
                return 'default'
        
        return 'default'
    
    def _getNameBasedOffset(self, layer_name: str, layer_type: str) -> Tuple[int, int]:
        """根据图层名称获取额外偏移"""
        if not layer_name:
            return (0, 0)
        
        name_lower = layer_name.lower()
        
        # 左右偏移判断
        offset_x = 0
        if any(keyword in name_lower for keyword in ['左', 'left', 'l_']):
            offset_x = -20
        elif any(keyword in name_lower for keyword in ['右', 'right', 'r_']):
            offset_x = 20
        
        # 上下偏移判断
        offset_y = 0
        if any(keyword in name_lower for keyword in ['上', 'upper', 'top']):
            offset_y = -10
        elif any(keyword in name_lower for keyword in ['下', 'lower', 'bottom']):
            offset_y = 10
        
        return (offset_x, offset_y)
    
    def suggestLayerType(self, layer_name: str, image_size: Tuple[int, int]) -> str:
        """根据图层名称和图像特征建议图层类型"""
        if not layer_name:
            return 'custom'
        
        name_lower = layer_name.lower()
        
        # 服装关键词
        if any(keyword in name_lower for keyword in [
            '服装', '衣服', '上衣', '下装', '裙子', '裤子', '外套', '内衣',
            'costume', 'clothes', 'dress', 'shirt', 'pants', 'coat'
        ]):
            return 'costume'
        
        # 表情关键词
        if any(keyword in name_lower for keyword in [
            '表情', '眼睛', '眉毛', '嘴巴', '笑容', '哭泣', '愤怒',
            'expression', 'eyes', 'eyebrows', 'mouth', 'smile', 'cry'
        ]):
            return 'expression'
        
        # 配饰关键词
        if any(keyword in name_lower for keyword in [
            '配饰', '装饰', '帽子', '耳环', '项链', '手镯', '发饰',
            'accessory', 'decoration', 'hat', 'earring', 'necklace', 'bracelet'
        ]):
            return 'accessory'
        
        # 根据图像尺寸推测
        width, height = image_size
        
        # 小尺寸通常是配饰或表情细节
        if width < 100 and height < 100:
            return 'accessory'
        
        # 中等尺寸可能是表情
        if width < 200 and height < 200:
            return 'expression'
        
        # 大尺寸通常是服装
        if width > 300 or height > 300:
            return 'costume'
        
        return 'custom'
    
    def getAlignmentPresets(self, layer_type: str) -> Dict[str, Tuple[int, int]]:
        """获取指定类型的对齐预设"""
        return self.POSITION_ZONES.get(layer_type, {})
    
    def learnFromUserPlacement(self, 
                             layer_type: str, 
                             zone: str, 
                             position: Tuple[int, int],
                             character_name: Optional[str] = None):
        """从用户的位置调整中学习"""
        if character_name:
            if character_name not in self.learned_positions:
                self.learned_positions[character_name] = {}
            
            key = f"{layer_type}_{zone}"
            self.learned_positions[character_name][key] = position
        
        # 也可以更新全局预设
        if layer_type in self.POSITION_ZONES and zone in self.POSITION_ZONES[layer_type]:
            # 采用加权平均的方式逐步调整预设
            current_pos = self.POSITION_ZONES[layer_type][zone]
            new_x = int(current_pos[0] * 0.8 + position[0] * 0.2)
            new_y = int(current_pos[1] * 0.8 + position[1] * 0.2)
            self.POSITION_ZONES[layer_type][zone] = (new_x, new_y)
    
    def exportAlignmentConfig(self) -> Dict:
        """导出对齐配置（用于保存用户学习的位置偏好）"""
        return {
            'position_zones': self.POSITION_ZONES,
            'learned_positions': self.learned_positions,
            'cache': self.character_analysis_cache
        }
    
    def importAlignmentConfig(self, config: Dict):
        """导入对齐配置"""
        if 'position_zones' in config:
            self.POSITION_ZONES.update(config['position_zones'])
        if 'learned_positions' in config:
            self.learned_positions.update(config['learned_positions'])
        if 'cache' in config:
            self.character_analysis_cache.update(config['cache'])


# 全局对齐系统实例
alignment_system = PositionAlignmentSystem()
