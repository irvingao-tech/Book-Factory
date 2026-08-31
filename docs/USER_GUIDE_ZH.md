# Book Factory V1.5 详细使用说明

Book Factory 是一个 Blender 程序化书籍生成插件，可以在任意网格表面创建书架式排列（Shelf）和水平堆叠（Stack），并提供真实尺寸预设、标准模型、Low Poly 模型、随机变化、材质、曲线排列、UV 排列和非破坏式冻结功能。

## 1. 系统要求

- Blender 4.3 或更高版本
- 推荐 Blender 4.5 LTS
- 已测试 Blender 4.3、4.5 LTS 和 5.0

## 2. 安装

1. 下载 `Book-Factory-V1.5.zip`。
2. 打开 Blender。
3. 进入 `Edit > Preferences > Add-ons` 或 `Get Extensions`。
4. 点击右上角菜单。
5. 选择 `Install from Disk`。
6. 选择 `Book-Factory-V1.4.zip`。
7. 确认 Book Factory 已启用。
8. 回到 3D View，按 `N` 打开右侧面板。
9. 点击 `Book Factory` 标签。

升级旧版本时，建议先完全关闭 Blender，再安装新压缩包。内部扩展 ID 保留为 `bookgen2`，因此新版本可以覆盖旧版本并读取已有场景数据。

## 3. 语言设置

进入：

`Edit > Preferences > Add-ons > Book Factory > Preferences > Language`

可选语言：

- English
- 中文
- 日本語

语言设置只影响 Book Factory，不依赖 Blender 全局语言。切换后所有打开的 Book Factory 面板会立即重绘。

## 4. 界面结构

主面板顶部有两个模式：

- `Shelf`：竖直书本横向排列
- `Stack`：水平书本竖向堆叠

面板中的主要折叠区域：

- `Book Appearance`：书籍类型、尺寸及随机范围
- `Layout & Variation`：排列、曲线、倾斜、旋转和位移
- `Model Details`：书脊、封面、内页和布线
- `Materials`：封面、书页和随机颜色

底部操作：

- `Auto Rebuild`：参数改变后自动更新
- `Rebuild`：手动重新生成
- `Merge & Freeze`：创建独立冻结副本

## 5. 场景与列表双向选择

Book Factory 列表和 3D View 已双向同步。

点击工具栏列表中的 Shelf 或 Stack 名称：

- 自动取消其他场景对象选择
- 选中对应程序化对象
- 设置为 Blender Active Object
- 显示橙色轮廓
- 自动显示对应参数

在 3D View 中点击程序化书本对象：

- 自动激活列表中的对应名称
- 自动切换 Shelf/Stack 模式
- 自动显示对应独立 Settings

点击 Frozen 副本时，会通过 `source_group` 找到原始可编辑组合。

点击普通场景对象不会改变当前 Book Factory 列表项。

## 6. 每个组合独立参数

每个 Shelf 和 Stack 都有独立 Settings。

创建新组合时，插件会复制当前参数作为新组合的初始值，但之后互不影响。修改列表中的一个组合不会同时修改其他组合。

Settings 名称显示在当前组合卡片下方，可以重命名。不要手动删除 Book Factory 数据属性。

## 7. Shelf 创建流程

1. 确认场景中存在用于放置的网格表面，例如书架层板。
2. 点击顶部 `Shelf`。
3. 点击 `Add Shelf`。
4. 在表面上点击一次，确定起点。
5. 移动鼠标，在表面上再次点击，确定终点。
6. 生成后在列表中选择该 Shelf 继续调整。

确定 Shelf 终点时，可以按 `X`、`Y` 或 `Z` 约束方向。

### 7.1 Shelf 对齐

`Alignment`：

- `Fore edge`：按书页前缘对齐
- `Spine`：按书脊对齐
- `Center`：按书本深度中心对齐

### 7.2 Shelf 整体曲线

`Overall Curve` 只改变每本书的前后位置，不旋转书本本身。

- 原始横向 X 间距保持不变
- 所有未倾斜书本互相平行
- 起点保持固定
- 正负数控制相反方向
- 不会因为跟随切线旋转而产生书本交叉

只有 `Leaning` 参数会主动改变书本倾斜角度。

### 7.3 Shelf 前后随机位移

`Depth Offset (cm)`：最大前后位移距离。

`Offset Chance`：参与随机位移的书本比例。

`Inset / Protrude Bias`：

- `-1`：只向内缩进
- `0`：前后均衡
- `1`：只向前突出

位移不会改变书本横向间距。

### 7.4 Shelf 倾斜

`Lean Amount`：参与倾斜的概率。

`Lean Direction`：偏向左侧或右侧。

`Lean Angle`：基础倾斜角度。

`Var`：倾斜角随机变化。

如果希望所有书严格平行，请将 `Lean Amount` 设置为 0。

## 8. Stack 创建流程

1. 点击顶部 `Stack`。
2. 点击 `Add Stack`。
3. 在表面上点击，确定固定起点。
4. 移动鼠标确定 Stack Forward 方向。
5. 再次点击确认方向。
6. 向上移动鼠标，点击确定 Stack 高度。

### 8.1 Stack 方向角度吸附

确定 Forward 方向时默认启用角度吸附。

设置位置：

`Edit > Preferences > Add-ons > Book Factory > Stack direction snap`

可选：

- 5°
- 10°
- 15°（默认）
- 30°
- 45°

按住 `Shift` 可以临时自由旋转。

水平表面使用世界 X 轴作为 0°。倾斜表面使用世界 X 轴在表面上的投影，并围绕表面法线捕捉。

### 8.2 Stack 双轴曲线

`Forward Curve`：控制前后方向的位置曲线。

`Side Curve`：控制左右方向的位置曲线。

两条曲线只改变每层书的位置：

- 不旋转书本
- 所有书保持水平
- Z 高度不变
- 层间距不变
- 起点固定
- 两个方向可以组合

### 8.3 Stack 四方向随机位移

`Planar Offset (cm)`：最大平面位移。

`Offset Chance`：参与位移的书本比例。

每本被选中的书会随机选择一个方向：

- Left
- Right
- Back
- Forward

每本书只沿一个方向位移。随机位移会叠加在 Forward Curve 和 Side Curve 之上。

### 8.4 Stack 旋转和朝向

`Rotation Variation`：书本在自身水平面中的随机旋转。

`Top Face`：

- Front cover
- Back cover

如果要求所有书方向完全一致，将 `Rotation Variation` 设置为 0。

Stack 会按书本类型分组，并将封面面积较大的书放在下方。同类书内部也按照面积从大到小排列。

## 9. 书籍类型预设

标准类型：

- Classic / Dictionary (Thick)
- Trade Novel / Reader
- US Letter Magazine

Low Poly 类型：

- Classic / Dictionary (Thick) - Low Poly
- Trade Novel / Reader - Low Poly
- US Letter Magazine - Low Poly

真实尺寸：

| 类型 | 高度 | 封面宽度 | 厚度 |
| --- | ---: | ---: | ---: |
| 厚字典 | 24.765 cm | 18.415 cm | 5.334 cm |
| 普通小说 | 22.860 cm | 15.240 cm | 1.905 cm |
| US Letter 杂志 | 27.940 cm | 21.590 cm | 0.500 cm |

选择预设后仍可继续修改尺寸。

## 10. 尺寸和随机变化

`Height (cm)`：书本高度。

`Cover Width (cm)`：从书脊到书页前缘的封面宽度。

`Thickness (cm)`：书本总厚度。

每个尺寸右侧 `Var` 控制随机变化。0 表示固定尺寸，较高数值会增加差异。

所有面板长度使用厘米显示，内部仍以米存储，保证 Blender 数据和旧场景兼容。

## 11. 标准书模细节

`Text Inset (cm)`：书芯相对封面的内缩。

`Cover (cm)`：封面厚度。

`Spine Curl (cm)`：书脊向外突出的深度。

`Spine Roundness`：书脊从尖形到圆形的过渡。

`Page Curve Match`：靠书脊的内页后缘匹配书脊内弧的程度。

`Page Front Curve`：内页前缘内凹或外凸的深度。

`Page Front Roundness`：内页前缘曲线的圆润度。

`Curve Segments`：统一控制外书脊、内书脊、书页后缘和书页前缘的分段数。

统一分段始终保留中心纵向控制线，内外书脊和书页 rail 一一对应。

## 12. Low Poly 模型

Low Poly 使用单一封闭外壳，没有分离封面和独立书芯内部结构。

`Low Poly Segments`：

| 模式 | 顶点 | 四边面 | 说明 |
| --- | ---: | ---: | --- |
| 1 - Box | 8 | 6 | 完整长方体，无曲线 rail |
| 2 - Minimum | 12 | 10 | 一条中心控制 rail |
| 4 - Balanced | 20 | 18 | 默认平衡档 |
| 6 - Smooth | 28 | 26 | 更平滑的侧面曲线 |

`1 - Box` 适合远景、代理和超大规模书库。需要书脊和前缘曲线时使用 2、4 或 6。

## 13. 材质

`Cover Material`：封面材质。

`Page Material`：书页前缘材质。

开启 `Random Cover Colors` 后：

- `Color A` 与 `Color B` 定义颜色范围
- 每本书在范围内获得可复现颜色
- `Cover Roughness` 控制生成材质粗糙度

颜色和几何随机结果都由 `Random Seed` 控制。

## 14. Random Seed

相同参数与相同 Seed 会产生相同结果，包括：

- 尺寸随机
- 颜色随机
- Leaning
- Shelf 前后位移
- Stack 四方向位移
- Stack 平面旋转

改变 Seed 可以快速获得另一套排列。

### 14.1 随机书脊朝向

`Random Spine Side` 同时支持 Shelf 和 Stack。

开启后，`Flipped Books (%)` 控制有多少本书旋转 180°，使书脊与书页前缘交换朝向。

```text
0%    所有书保持默认朝向
25%   大约四分之一反向
50%   大约一半反向
100%  所有书反向
```

该功能只改变朝向，不改变书本位置、尺寸或排列间距。标准版和 Low Poly 都支持，相同 Seed 会得到相同的反向书本分布。

## 15. Auto Rebuild 和性能

`Auto Rebuild` 开启时，停止调整参数后自动更新。

插件使用防抖更新，不会在拖动滑块的每个事件上完整重建。

Preferences 中：

- `Debounced updates`
- `Update delay`

大型场景建议：

1. 关闭 Auto Rebuild。
2. 连续调整多个参数。
3. 点击 Rebuild。
4. 远景尽量使用 Low Poly。

每个 Shelf/Stack 只创建一个程序化 Object 和一个 Mesh，不会为每本书创建单独对象。

## 16. Merge & Freeze

`Merge & Freeze` 是非破坏式复制冻结。

执行后：

- 原 Shelf/Stack 保留
- 原 Settings 保留
- 原程序化对象可继续编辑
- 新建一个独立 Mesh 副本
- 自动选中冻结副本

多次执行会得到：

```text
stack_0_Scene_Frozen
stack_0_Scene_Frozen.001
stack_0_Scene_Frozen.002
```

修改和 Rebuild 原始组合不会改变已有冻结副本。

## 17. UV

冻结副本包含 `Book_Order_UV`。

UV 规则：

- 所有 UV 位于 0-1
- 每本书占一个独立网格单元
- 按书本顺序从左到右、从上到下排列
- `UV Tile Padding` 控制单元内部边距

冻结 Mesh 还包含面属性 `book_index`，用于识别每个面来自第几本书。

对象自定义属性：

- `book_count`
- `uv_grid_columns`
- `uv_grid_rows`
- `source_group`
- `bookgen_frozen`

## 18. 删除和解绑

列表右侧 `X`：删除当前程序化组合。

`Unlink`：将组合从 Book Factory 管理中解绑。解绑后的对象不会继续响应参数更新。

如需保留原件并获得可编辑副本，优先使用 Merge & Freeze。

## 19. 常见问题

### 参数调整后其他组合也变化

V1.0 以后每个组合使用独立 Settings。请确认使用最新版本并重新打开场景，让迁移完成。

### Overall Curve 导致书本交叉

V1.4 已修复。曲线只改变位置，不再改变模型自身旋转或压缩原间距。

### Stack 书本前高后低

Forward Curve 和 Side Curve 不会旋转书本。检查 `Rotation Variation`，并确认放置底面方向正确。

### Stack 方向难以对齐

在 Preferences 设置 Stack direction snap。按住 Shift 才会临时自由旋转。

### 调整参数卡顿

使用 Low Poly、关闭 Auto Rebuild，或增加 Update delay。

### 安装新版后出现旧类重复注册

完全关闭所有 Blender 窗口，再重新打开并安装新版本。

## 20. 许可证与原作者

Book Factory 使用 GPL-3.0-or-later。

本项目基于 BookGen：

- 原作者：Oliver Weissbarth
- 贡献者：Seojin Sim 及其他 BookGen contributors
- 原项目：https://github.com/oweissbarth/bookGen

源码分发保留原始版权和 GPL 声明。详情见仓库根目录 `LICENSE` 和 `NOTICE`。
