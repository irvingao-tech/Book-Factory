# Book Factory V1.4

Book Factory is a procedural book-building add-on for Blender. It creates editable shelves, horizontal stacks,
standard books, and lightweight single-shell book assets with deterministic variation, curved book geometry,
materials, ordered UVs, and non-destructive freezing.

The project is based on [BookGen](https://github.com/oweissbarth/bookGen) by Oliver Weissbarth and contributors.
Book Factory is free software distributed under **GPL-3.0-or-later**.

## Highlights

- Procedural **Shelf** and **Stack** placement directly on scene surfaces
- Compact context-aware interface that switches between Shelf and Stack settings
- Independent settings for every generated group
- English, Simplified Chinese, and Japanese interface languages
- Real-world size presets for dictionaries, novels/readers, and magazines
- Standard and Low Poly variants for every book type
- Direct curved spine topology without whole-book subdivision
- Adjustable curved page block at both spine and fore edge
- Shelf leaning, alignment, depth offset, and planar curvature
- Stack sorting, dual-axis curvature, rotation, and four-direction offsets
- Deterministic output from a reusable random seed
- One optimized procedural mesh per group
- Non-destructive **Merge & Freeze** with ordered 0-1 UV tiles
- Per-face `book_index` metadata for downstream selection and editing

## Requirements

- Blender 4.3 or newer
- Tested with Blender 4.3, 4.5 LTS, and 5.0

## Download

Download the installable package from:

[`dist/Book-Factory-V1.4.zip`](dist/Book-Factory-V1.4.zip)

## Installation

1. Download `Book-Factory-V1.4.zip`.
2. Open Blender.
3. Go to `Edit > Preferences > Add-ons` or `Get Extensions`.
4. Open the menu and choose `Install from Disk`.
5. Select `Book-Factory-V1.4.zip`.
6. Enable **Book Factory** if Blender does not enable it automatically.
7. Open the 3D View sidebar with `N` and select the **Book Factory** tab.

The internal extension ID remains `bookgen2` so this release can update compatible Book Factory/BookGen-derived
installations without breaking existing Blender scene data.

## Language

Book Factory has an add-on-specific language selector independent of Blender's global language:

`Edit > Preferences > Add-ons > Book Factory > Preferences > Language`

Available languages:

- English
- 中文
- 日本語

Changing the language immediately redraws all open Book Factory panels. It does not change saved presets or geometry.

## Interface

The top `SHELF / STACK` tabs select the working mode. If a group of that type already exists, Book Factory selects it;
otherwise the mode prepares the corresponding Add operation.

The compact interface is divided into four collapsible cards:

- **Book Appearance**: type preset, dimensions, and dimension variation
- **Layout & Variation**: group scale, seed, curves, alignment, leaning, rotation, and offsets
- **Model Details**: cover/page construction and curved topology controls
- **Materials**: cover material, page material, random colors, and roughness

Only properties relevant to the selected Shelf or Stack are shown. Shared appearance and model properties remain
visible in both modes.

### Bidirectional Selection Sync

- Clicking a row in the Book Factory group list selects and activates its procedural object in the 3D View.
- Clicking a procedural Shelf or Stack object in the 3D View activates the corresponding list row.
- Clicking a frozen copy activates its original source row through the stored `source_group` property.
- Unrelated scene objects do not change the Book Factory list selection.
- The previous manual bounding-box highlight button is no longer required or displayed.

### V1.4 Parallel Curve Layout

Shelf and Stack curve controls now change book positions only. They preserve the original spacing axis and do not
rotate books to follow curve tangents. This prevents fan-shaped overlap and model intersections. Shelf Leaning and
Stack Rotation Variation remain explicit, independent orientation controls.

## Shelf Workflow

1. Ensure the scene contains a mesh surface, such as a shelf board.
2. Select the `SHELF` tab.
3. Click **Add Shelf**.
4. Click a surface to set the start point.
5. Click again to set the endpoint.
6. Adjust the selected Shelf in the Book Factory panel.

During endpoint placement, use `X`, `Y`, or `Z` to constrain the direction.

### Shelf Layout Controls

- **Alignment**: fore edge, spine, or center alignment
- **Overall Curve**: offsets book positions in depth while preserving original spacing and parallel orientation
- **Lean Amount**: probability that a book leans
- **Lean Direction**: preference for left or right leaning
- **Lean Angle**: maximum lean angle
- **Depth Offset (cm)**: maximum random forward/backward displacement
- **Offset Chance**: percentage of books receiving depth displacement
- **Inset / Protrude Bias**: favors inset or protruding books

Shelf offsets follow each book's local curve direction and do not alter horizontal spacing.
Overall Curve does not rotate individual books. Only the explicit Leaning controls can change a Shelf book's angle.

## Stack Workflow

1. Select the `STACK` tab.
2. Click **Add Stack**.
3. Click a surface to set the fixed base.
4. Click to set the local forward direction.
5. Move upward and click to set the stack height.
6. Adjust the selected Stack in the Book Factory panel.

The direction step snaps to a configurable angle. Hold `Shift` while moving/clicking to temporarily use free rotation.
Configure the increment under `Preferences > Add-ons > Book Factory > Stack direction snap` with 5°, 10°, 15°,
30°, or 45°. The default is 15°.

### Stack Layout Controls

- **Forward Curve**: progressively bends layer positions forward or backward
- **Side Curve**: progressively bends layer positions left or right
- **Rotation Variation**: random in-plane rotation
- **Top Face**: front or back cover facing upward
- **Planar Offset (cm)**: maximum random per-layer displacement
- **Offset Chance**: percentage of layers receiving displacement

Each affected Stack book independently chooses Left, Right, Backward, or Forward. Books remain horizontal, their Z
spacing remains unchanged, and both smooth curve axes can be combined with the random offsets.
Forward Curve and Side Curve change layer positions only and never rotate the books themselves.

Stack books are grouped by type and ordered by average cover area. Larger covers are placed lower, and books inside
each type group are also ordered from larger to smaller.

## Book Types

Book Factory includes measured real-world presets:

| Preset | Height | Cover width | Thickness |
| --- | ---: | ---: | ---: |
| Classic / Dictionary (Thick) | 24.765 cm | 18.415 cm | 5.334 cm |
| Trade Novel / Reader | 22.860 cm | 15.240 cm | 1.905 cm |
| US Letter Magazine | 27.940 cm | 21.590 cm | 0.500 cm |

Each type also has a dedicated `- Low Poly` version using the same real-world dimensions.

Research sources are documented in the source history and include Merriam-Webster product dimensions, Amazon KDP
trim and paper formulas, and Mixam magazine specifications.

## Standard Geometry

Standard books use separate procedural cover and page structures with:

- Outer and inner curved spine rails
- Constant-width cover shell around the spine
- Curved page edge beside the spine
- Independently adjustable page fore-edge curve
- Matching quad-strip topology
- Separate cover and page material regions

### Curve Controls

- **Spine Curl (cm)**: spine projection depth
- **Spine Roundness**: pointed-to-rounded spine profile
- **Page Curve Match**: page-back match to the inner spine curve
- **Page Front Curve**: concave or convex fore-edge depth
- **Page Front Roundness**: pointed-to-rounded fore-edge profile
- **Curve Segments**: synchronized rail count for outer spine, inner spine, page back, and page front

The unified segment selector always uses even values, guaranteeing an exact center longitudinal rail.

## Low Poly Geometry

Low Poly books use one connected, watertight outer shell. They omit separate internal cover/page shells while retaining
the visible curved spine and fore-edge side topology.

`Low Poly Segments` controls the curved side rail count:

| Setting | Vertices per book | Quad faces per book | Recommended use |
| --- | ---: | ---: | --- |
| 1 - Box | 8 | 6 | Maximum reduction; rectangular prism |
| 2 - Minimum | 12 | 10 | Distant shots and very large libraries |
| 4 - Balanced | 20 | 18 | General use and default |
| 6 - Smooth | 28 | 26 | Closer views |

The page fore edge can retain `Page Material`; the remaining shell uses `Cover Material`.

### V1.1 Low-Poly Box Mode

`1 - Box` removes all intermediate curve rails and creates a plain rectangular prism with 8 vertices and 6 quad
faces. It is intended for extreme background density and proxy layouts. Spine and fore-edge curve controls remain
available for the 2, 4, and 6 segment modes.

## Materials

Assign an existing Blender material to **Cover Material** and **Page Material**, or enable **Random Cover Colors**.

Random colors interpolate between Color A and Color B using a bounded reusable palette. **Cover Roughness** controls
the generated Principled BSDF materials. The same seed recreates the same color and geometry sequence.

## Independent Group Settings

Every Shelf and Stack owns a separate settings block. Creating a group copies the current visible settings into a new
independent block. Editing one row in the group list therefore does not change any other group.

Older compatible scenes with shared settings are migrated automatically by copying settings for additional users.

## Performance

Each procedural Shelf or Stack is built as one Object and one Mesh rather than one Object/Mesh pair per book. The
per-face integer attribute `book_index` retains book boundaries for editing and UV processing.

Additional performance behavior:

- Debounced updates rebuild once after slider adjustment stops
- Only groups using the changed settings are rebuilt
- Old generated data is removed in one batch operation
- Low Poly presets substantially reduce geometry and generation time

Configure **Debounced updates** and **Update delay** under the add-on Preferences. For exceptionally large scenes,
disable **Auto Rebuild**, adjust multiple values, and click **Rebuild** manually.

## Merge & Freeze

**Merge & Freeze** creates a non-destructive independent mesh copy of the selected procedural group.

It preserves the original editable Shelf/Stack collection and settings. You can continue changing and rebuilding the
source without affecting any frozen copy.

The frozen object includes:

- Applied evaluated geometry
- Material assignments
- Smooth and sharp edge state
- One ordered UV map named `Book_Order_UV`
- Face-domain integer attribute `book_index`
- Custom properties `book_count`, `uv_grid_columns`, `uv_grid_rows`, and `source_group`

Every source book receives one UV grid cell inside the 0-1 square. Cells are assigned left-to-right and top-to-bottom
in book order. `UV Tile Padding` can be adjusted in Blender's last-operation panel.

Running Merge & Freeze repeatedly creates additional independent copies such as:

```text
stack_0_Scene_Frozen
stack_0_Scene_Frozen.001
stack_0_Scene_Frozen.002
```

## Repository Layout

```text
Book-Factory/
|-- book_factory/              Blender extension source
|   |-- blender_manifest.toml
|   |-- __init__.py
|   |-- data/
|   |-- icons/
|   `-- shaders/
|-- dist/
|   |-- Book-Factory-V1.0.zip
|   |-- Book-Factory-V1.1.zip
|   |-- Book-Factory-V1.2.zip
|   |-- Book-Factory-V1.3.zip
|   `-- Book-Factory-V1.4.zip
|-- LICENSE                    GPL-3.0 license text
|-- NOTICE                     attribution and derivative-work notice
`-- README.md
```

## Development

The extension source root is `book_factory/`. It contains `blender_manifest.toml` and can be validated or built with
a compatible Blender command-line installation:

```powershell
blender --command extension validate ./book_factory
blender --command extension build --source-dir ./book_factory --output-dir ./dist
```

Internal names such as `bookgen2`, `bookgen.*`, `BookGenSettings`, and `BookGenGroupingProperties` are intentionally
retained for compatibility.

## License

Book Factory is licensed under the **GNU General Public License, version 3 or any later version**
(`GPL-3.0-or-later`). See [LICENSE](LICENSE).

You may use, study, modify, and redistribute the software under the terms of the GPL. Distributions and modified
versions must provide the corresponding source and retain applicable copyright and license notices.

## Credits And Attribution

Book Factory is a modified and extended derivative of BookGen.

- Original BookGen author: **Oliver Weissbarth**
- Additional credited BookGen contributor: **Seojin Sim**
- Original project: <https://github.com/oweissbarth/bookGen>
- Book Factory repository: <https://github.com/irvingao-tech/Book-Factory>

Original source files retain their copyright and GPL notices. See [NOTICE](NOTICE) for the derivative-work statement.

---

## 中文简介

Book Factory 是一个用于 Blender 的程序化书籍生成工具，可创建书架排列、水平书堆、标准书模和单壳低模。

主要功能包括：

- Shelf 与 Stack 表面交互放置
- 每个组合独立参数
- 真实书本尺寸预设
- 标准版与 Low Poly 版
- 可调书脊、内页后缘和前缘弧度
- Shelf 前后随机位移
- Stack 前后左右四方向随机位移与双轴整体曲线
- 随机封面颜色与独立页面材质
- 单对象高性能程序化组合
- 非破坏式 Merge & Freeze
- 按书本顺序排列到 0-1 的 UV
- 英文、中文、日文界面切换

安装包：[`dist/Book-Factory-V1.4.zip`](dist/Book-Factory-V1.4.zip)

详细中文说明：[docs/USER_GUIDE_ZH.md](docs/USER_GUIDE_ZH.md)

许可证：GPL-3.0-or-later。该项目基于 Oliver Weissbarth 等贡献者开发的 BookGen，原作者及许可证信息已保留。
