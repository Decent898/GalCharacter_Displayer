# 🎭 GINKA 立绘搭配软件 - 项目结构

## 📁 项目目录结构

```
extract_data/
├── 📄 main.py                    # 主程序入口
├── 📄 README.md                  # 项目说明
├── 📄 requirements.txt           # Python依赖
├── 📁 ginka_composer/            # 现代化角色编辑器 (主要工具)
│   ├── models/                   # 数据模型
│   ├── widgets/                  # UI组件
│   ├── ui/                       # 用户界面
│   └── utils/                    # 工具函数
├── 📁 tools/                     # 工具集合
│   ├── 📁 character_tools/       # 角色处理工具
│   │   ├── character_analyzer.py # 角色分析器
│   │   └── character_analysis.json # 分析数据
│   └── 📁 live2d_tools/          # Live2D工具
│       ├── ginka_to_live2d.py    # GINKA到Live2D转换器
│       ├── live2d_complete_builder.py # 完整Live2D构建器
│       └── live2d_web_generator.py # Web预览生成器
├── 📁 live2d_projects/           # Live2D项目输出
│   └── tgina01_l/                # 示例项目
│       ├── textures/             # 贴图文件
│       ├── web_preview/          # Web预览工具
│       └── *.json               # 配置文件
├── 📁 docs/                      # 文档资料
│   ├── live2d_guide.md          # Live2D制作指南
│   ├── 使用说明.md               # 使用说明
│   └── 项目完成报告.md           # 项目报告
├── 📁 legacy/                    # 旧版本文件
│   ├── modern_character_composer.py # 旧版编辑器
│   ├── character_composer.py     # 早期版本
│   └── character_composer/       # 旧版本模块
├── 📁 bgimage/                   # 背景图片资源
├── 📁 bgimage2/                  # 背景图片资源2
├── 📁 fgimage/                   # 前景图片资源
├── 📁 GINKA/                     # GINKA原始数据
├── 📁 cr_data/                   # 角色数据
├── 📁 cr_event/                  # 事件数据
├── 📁 data/                      # 其他数据
└── 📁 png_images/                # PNG图片缓存
```

## 🚀 快速开始

### 启动角色编辑器
```bash
python main.py
```

### 启动Live2D工具套件
```bash
python main.py --live2d
# 或
python main.py -l
```

### 使用独立工具

#### 角色分析器
```bash
python tools/character_tools/character_analyzer.py
```

#### Live2D转换器
```bash
python tools/live2d_tools/ginka_to_live2d.py
```

#### Live2D完整构建器
```bash
python tools/live2d_tools/live2d_complete_builder.py
```

#### Web预览生成器
```bash
python tools/live2d_tools/live2d_web_generator.py
```

## 🎯 主要功能

### 1. 🎨 现代化角色编辑器
- **位置**: `ginka_composer/`
- **功能**: PyQt6现代化界面，支持实时预览
- **特点**: 模块化架构，易于扩展

### 2. � Live2D转换工具链
- **GINKA转Live2D**: 自动转换角色数据为Live2D项目
- **完整项目构建**: 一键生成完整Live2D项目结构
- **Web预览生成**: 创建可交互的Web预览页面

### 3. 🌐 Web预览系统
- **位置**: `live2d_projects/tgina01_l/web_preview/`
- **功能**: 浏览器内Live2D模型预览和交互
- **特点**: 支持参数调整、表情切换、文件拖放

## 📊 工具分类

### 核心工具 (推荐使用)
- `main.py` - 主程序入口
- `ginka_composer/` - 现代化角色编辑器
- `tools/live2d_tools/` - Live2D工具集

### 辅助工具
- `tools/character_tools/` - 角色分析工具
- `docs/` - 文档和指南

### 历史版本 (仅供参考)
- `legacy/` - 旧版本代码，已不推荐使用

## 🔧 开发环境

### Python版本
- Python 3.7+

### 主要依赖
```
PyQt6>=6.4.0
Pillow>=9.0.0
```

### 安装依赖
```bash
pip install -r requirements.txt
```

## 📖 文档资源

- **Live2D制作指南**: `docs/live2d_guide.md`
- **使用说明**: `docs/使用说明.md`
- **项目报告**: `docs/项目完成报告.md`
- **Web端指南**: `live2d_projects/tgina01_l/web_preview/demo.html`

## 🎭 示例项目

### tgina01角色
- **原始数据**: 110个分类贴图文件
- **Live2D项目**: `live2d_projects/tgina01_l/`
- **Web预览**: 完整的浏览器预览系统
- **配置文件**: 自动生成的参数和动画配置

## ⚡ 快捷命令

```bash
# 查看帮助
python main.py --help

# 启动角色编辑器
python main.py

# 打开Live2D工具
python main.py --live2d

# 运行角色分析
cd tools/character_tools && python character_analyzer.py

# 生成Live2D项目
cd tools/live2d_tools && python ginka_to_live2d.py

# 创建Web预览
cd tools/live2d_tools && python live2d_web_generator.py
```
- 图层预览功能（鼠标悬停预览）
- 图层顺序调整
- 异步图像加载

### 🖱️ 交互控制
- 画布拖拽和缩放
- 角色直接拖拽移动
- 鼠标滚轮缩放画布
- 键盘快捷键支持

### 📸 导出功能
- 高分辨率导出（1x-4x）
- 高质量图像重采样
- 支持PNG、JPEG格式
- 进度显示

### 💾 场景管理
- 场景保存/加载
- JSON格式配置文件
- 完整状态恢复

## 依赖要求

```
PyQt6>=6.0.0
Pillow>=8.0.0
```

## 安装运行

1. 确保Python 3.8+已安装

2. 安装依赖：
```bash
pip install PyQt6 Pillow
```

3. 运行程序：
```bash
python main.py
```

## 使用说明

### 基本操作
1. **添加背景**：在场景标签页选择或预览背景图片
2. **添加角色**：在角色标签页选择角色和尺寸，点击"添加角色"
3. **配置图层**：在图层标签页选择要显示的图层
4. **调整位置**：使用变换控件或直接在画布上拖拽
5. **导出图像**：点击导出按钮，选择分辨率和保存位置

### 高级功能
- **图层预览**：鼠标悬停在图层选项上可预览图层
- **角色层级**：使用层级控制按钮调整角色前后顺序
- **画布操作**：切换拖拽模式，使用适应画布和重置视图
- **场景管理**：保存当前配置，随时加载之前的场景

## 模块说明

### models/
- `CharacterInstance`: 角色实例数据模型
- `ImageLoader`: 异步图像加载器

### widgets/
- `LayerPreviewWindow`: 图层预览悬浮窗口
- `PreviewableCheckBox`: 支持预览的复选框
- `PreviewableBackgroundItem`: 支持预览的背景项目
- `Canvas`: 高性能画布组件

### ui/
- `ModernCharacterComposer`: 主窗口类
- `SceneTab`: 场景标签页
- `CharacterTab`: 角色标签页  
- `LayerTab`: 图层标签页

### utils/
- `get_modern_style()`: 获取现代化样式表
- `organize_layers_by_type()`: 智能图层分组
- `pil_to_qpixmap_high_quality()`: 高质量图像转换

## 开发注意事项

### 信号连接
所有标签页组件使用信号/槽机制与主窗口通信，便于解耦和测试。

### 异步加载
图像加载使用独立线程，避免界面阻塞。

### 内存管理
合理管理PIL图像对象，避免内存泄漏。

### 性能优化
画布绘制使用硬件加速和高质量渲染提示。

## 发现的游戏立绘结构

### 文件组织方式

1. **立绘定义文件** (`GINKA/t[角色名][序号]_[尺寸].txt`)
   - 包含图层的精确位置信息 (left, top, width, height)
   - 定义图层ID和分组关系
   - 支持多种尺寸: s(小), m(中), l(大), ll(超大)

2. **图像文件** (`cr_data/t[角色名][序号]_[尺寸]_[图层ID].tlg`)
   - KiriKiri引擎的TLG图像格式
   - 文件名中的数字对应定义文件中的layer_id
   - 包含角色的各个部分：眉毛、眼睛、嘴巴、身体、服装等

3. **配置文件**
   - `standposition.txt`: 角色在不同缩放级别下的位置偏移
   - `emotion.txt`: 表情特效的位置定义

### 图层分类系统

通过分析发现，每个角色的立绘被分解为以下类型的图层：

- **眉毛类**: `眉1`, `眉2`, `眉3` 等，表示不同的眉毛表情
- **眼睛类**: `目1`, `目2`, `目3` 等，表示不同的眼部表情  
- **嘴巴类**: `口1`, `口2`, `口3` 等，表示不同的嘴部表情
- **脸颊类**: `頬1`, `頬2` 等，表示脸红等特效
- **身体类**: `base` 等，角色的基础身体部分
- **服装类**: `h1`, `h2`, `h3`, `h4` 等，不同的服装和装备

## 使用说明

### 第一步：分析游戏数据

```bash
python character_analyzer.py
```

这将解析所有角色的立绘结构，生成 `character_analysis.json` 文件。

**分析结果示例:**
```
角色: tgina01
  S尺寸: 1个分组, 112个图层, 112个图像文件
  L尺寸: 1个分组, 112个图层, 112个图像文件

角色: thim01  
  S尺寸: 1个分组, 46个图层, 46个图像文件
  L尺寸: 1个分组, 46个图层, 46个图像文件
```

### 第二步：转换TLG图像

由于TLG是专有格式，需要转换为PNG才能使用：

```bash
python tlg_converter.py
```

**推荐的转换工具:**

1. **tlg2png** (推荐)
   - 命令行工具，支持批量转换
   - 下载地址: https://github.com/uyjulian/tlg

2. **XnView** 
   - 图像查看器，支持TLG格式
   - 可以手动批量转换
   - 下载地址: https://www.xnview.com/

3. **KrkrExtract**
   - KiriKiri专用提取工具
   - 下载地址: https://github.com/xmoeproject/KrkrExtract

### 第三步：运行立绘搭配软件

```bash
python character_composer.py
```

## 软件功能

### 主要功能

1. **角色选择**: 支持所有已解析的游戏角色
2. **尺寸选择**: 支持 S/M/L/LL 四种尺寸
3. **图层管理**: 
   - 按类型智能分组 (眉毛、眼睛、嘴巴等)
   - 复选框方式选择图层
   - 实时预览效果
4. **画布操作**:
   - 实时合成显示
   - 支持缩放和滚动
   - 清空和重置功能
5. **配置管理**:
   - 保存当前搭配方案
   - 加载已保存的配置
   - 导出最终图片

### 界面说明

- **左侧控制面板**: 角色选择、图层管理
- **右侧预览区域**: 实时显示合成结果
- **底部按钮**: 功能操作按钮

## 技术实现

### 核心解析逻辑

1. **UTF-16编码处理**: 游戏配置文件使用UTF-16 LE编码
2. **图层坐标系统**: 准确解析每个图层的位置和尺寸
3. **智能分组算法**: 根据图层名称自动分类
4. **图像合成**: 按正确顺序叠加图层

### 数据结构

```json
{
  "角色名": {
    "layer_mapping": {
      "尺寸": {
        "分组名": [
          {
            "name": "图层名",
            "layer_id": 123,
            "position": [x, y],
            "size": [width, height],
            "has_image": true
          }
        ]
      }
    }
  }
}
```

## 角色数据统计

| 角色代码 | 角色名 | L尺寸图层数 | 描述 |
|---------|--------|------------|------|
| tgina01 | ギンカ | 112 | 主角，最丰富的表情变化 |
| tginc01 | 银花(子供) | 69 | 幼年版本 |
| thim01  | ひまわり | 46 | 向日葵 |
| tkar01  | 花憐 | 37 | 花恋 |
| trin01  | リン | 55 | 铃 |
| tsen01  | 先生 | 53 | 老师 |
| tsou01  | 草二 | 36 | 草二 |

## 开发扩展

### 添加新功能

1. **表情预设**: 预定义常用的表情组合
2. **动画支持**: 制作简单的表情动画
3. **背景切换**: 集成游戏背景图片
4. **批量导出**: 一键生成所有表情组合

### 文件结构

```
extract_data/
├── character_analyzer.py     # 数据分析工具
├── character_composer.py     # 立绘搭配软件
├── tlg_converter.py         # TLG转换工具
├── character_analysis.json  # 解析结果数据
├── GINKA/                   # 游戏配置文件
├── cr_data/                 # TLG图像文件
├── png_images/              # 转换后的PNG文件
└── README.md               # 本说明文件
```

## 常见问题

### Q: 为什么看不到图片？
A: 需要先使用 `tlg_converter.py` 将TLG文件转换为PNG格式。

### Q: 转换工具在哪里下载？
A: 推荐使用 tlg2png，在GitHub上可以找到。

### Q: 可以添加自定义表情吗？
A: 理论上可以，但需要了解游戏的图层命名规则。

### Q: 导出的图片质量如何？
A: 保持原游戏图片质量，支持透明通道。

## 致谢

感谢《GINKA》游戏的制作团队创造了如此精美的角色立绘系统。

本工具仅供学习和研究使用，请尊重原作的版权。

## 版权声明

本软件仅用于技术研究和学习目的。游戏《GINKA》的所有图像资源版权归原作者所有。

使用本工具时请遵守相关法律法规和游戏厂商的版权政策。
