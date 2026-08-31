"""
This file contains the property definitions used to describe the book and shelf layouts.
"""

from math import pi, radians
import logging

import bpy
from bpy.props import (
    FloatProperty,
    IntProperty,
    IntVectorProperty,
    EnumProperty,
    BoolProperty,
    FloatVectorProperty,
    PointerProperty,
    StringProperty,
)

from .utils import (
    get_bookgen_collection,
    get_shelf_collection_by_index,
    get_shelf_parameters,
    get_settings_by_name,
    get_stack_parameters,
    select_grouping_objects,
)
from .shelf import Shelf
from .stack import Stack
from .ui_outline import BookGenShelfOutline
from .presets import BOOK_PRESETS, MIX_DETAIL_BASE
from .translations import get_language, tr

_pending_settings = set()
_update_callback = None


def _run_pending_updates():
    """Rebuild changed settings once Blender is ready and the user has paused."""
    global _update_callback
    context = bpy.context
    if context.mode != "OBJECT":
        return 0.25

    settings_names = tuple(_pending_settings)
    _pending_settings.clear()
    _update_callback = None
    for settings_name in settings_names:
        bpy.ops.bookgen.rebuild(settings_name=settings_name)
    return None


def cancel_pending_update():
    """Cancel delayed work before the add-on is disabled or reloaded."""
    global _update_callback
    if _update_callback is not None and bpy.app.timers.is_registered(_update_callback):
        bpy.app.timers.unregister(_update_callback)
    _pending_settings.clear()
    _update_callback = None


def centimeter_property(source_name, label, minimum=0.0, soft_maximum=100.0):
    """Expose an internal meter property as an editable centimeter value."""

    def get_value(self):
        return getattr(self, source_name) * 100.0

    def set_value(self, value):
        setattr(self, source_name, value / 100.0)

    return FloatProperty(
        name=label,
        description=f"{label} in centimeters",
        min=minimum,
        soft_max=soft_maximum,
        precision=3,
        step=1,
        get=get_value,
        set=set_value,
        options=set(),
    )


_ENUM_CACHE = {}


def localized_enum_items(context, cache_name, items):
    """Return stable translated enum tuples for the selected add-on language."""
    language = get_language(context)
    cache_key = (cache_name, language)
    if cache_key not in _ENUM_CACHE:
        translated = []
        for index, item in enumerate(items):
            identifier, label, description = item[:3]
            numeric_id = item[3] if len(item) > 3 else index
            translated.append((identifier, tr(context, label), description, 0, numeric_id))
        _ENUM_CACHE[cache_key] = tuple(translated)
    return _ENUM_CACHE[cache_key]


def book_preset_items(_self, context):
    return localized_enum_items(
        context,
        "book_presets",
        (
            ("CUSTOM", "Custom", "Keep the current dimensions"),
            ("REFERENCE", "Classic / Dictionary (Thick)", "247.65 x 184.15 x 53.34 mm"),
            ("NOVEL", "Trade Novel / Reader", "228.6 x 152.4 x 19.05 mm"),
            ("MAGAZINE", "US Letter Magazine", "279.4 x 215.9 x 5.0 mm"),
            ("REFERENCE_LOW", "Classic / Dictionary (Thick) - Low Poly", "Single-shell low-poly model"),
            ("NOVEL_LOW", "Trade Novel / Reader - Low Poly", "Single-shell low-poly model"),
            ("MAGAZINE_LOW", "US Letter Magazine - Low Poly", "Single-shell low-poly model"),
        ),
    )


def alignment_items(_self, context):
    return localized_enum_items(
        context,
        "alignment",
        (
            ("0", "Fore edge", "Align books at the fore edge"),
            ("1", "Spine", "Align books at the spine"),
            ("2", "Center", "Align books at the center"),
        ),
    )


def stack_top_face_items(_self, context):
    return localized_enum_items(
        context,
        "stack_top_face",
        (
            ("1", "Front cover", "Front cover facing up"),
            ("-1", "Back cover", "Back cover facing up"),
        ),
    )


def low_poly_segment_items(_self, context):
    return localized_enum_items(
        context,
        "low_poly_segments",
        (
            ("1", "1 - Box", "A rectangular prism with no intermediate curve rails", 3),
            ("2", "2 - Minimum", "Three rails including one center control line", 0),
            ("4", "4 - Balanced", "Five rails with balanced shape and cost", 1),
            ("6", "6 - Smooth", "Seven rails for a smoother low-poly silhouette", 2),
        ),
    )


class BookGenAddonProperties(bpy.types.PropertyGroup):
    """
    This store the current state of the bookGen add-on.
    """

    # GPU resources must be created lazily so the add-on also works in background mode.
    outline = None

    def update_outline_active(self, context):
        """
        If the outline was activated, generate the shelf and draw the outline.
        Otherwise disable the outline.
        """
        properties = context.scene.BookGenAddonProperties
        active_grouping = get_shelf_collection_by_index(context, properties.active_shelf)
        if active_grouping is not None:
            properties.ui_mode = active_grouping.BookGenGroupingProperties.grouping_type
            select_grouping_objects(context, active_grouping)
        if properties.outline_active and properties.active_shelf != -1:
            if BookGenAddonProperties.outline is None:
                BookGenAddonProperties.outline = BookGenShelfOutline()
            outline = BookGenAddonProperties.outline
            grouping_collection = get_shelf_collection_by_index(context, properties.active_shelf)
            if not grouping_collection:
                return
            grouping_props = grouping_collection.BookGenGroupingProperties
            settings = get_settings_by_name(context, grouping_props.settings_name)
            if grouping_props.grouping_type == "SHELF":
                parameters = get_shelf_parameters(context, grouping_props.id, settings)
                shelf = Shelf(
                    grouping_collection.name,
                    grouping_props.start,
                    grouping_props.end,
                    grouping_props.normal,
                    parameters,
                )
                shelf.fill()
                outline.enable_outline(*shelf.get_geometry(), context)
            else:
                parameters = get_stack_parameters(context, grouping_props.id, settings)
                shelf = Stack(
                    grouping_collection.name,
                    grouping_props.origin,
                    grouping_props.forward,
                    grouping_props.normal,
                    grouping_props.height,
                    parameters,
                )
                shelf.fill()
                outline.enable_outline(*shelf.get_geometry(), context)
        else:
            if BookGenAddonProperties.outline is not None:
                BookGenAddonProperties.outline.disable_outline()

    auto_rebuild: BoolProperty(
        name="auto rebuild",
        description="Automatically rebuild all books if settings are changed",
        default=True,
        options=set(),
    )
    active_shelf: IntProperty(name="Active grouping", update=update_outline_active, options=set())
    ui_mode: EnumProperty(
        name="Mode",
        items=(("SHELF", "Shelf", "Shelf placement mode"), ("STACK", "Stack", "Stack placement mode")),
        default="SHELF",
        options=set(),
    )
    show_appearance: BoolProperty(name="Book Appearance", default=True, options=set())
    show_layout: BoolProperty(name="Layout & Variation", default=True, options=set())
    show_details: BoolProperty(name="Model Details", default=True, options=set())
    show_materials: BoolProperty(name="Materials", default=True, options=set())
    outline_active: BoolProperty(
        name="Highlight active",
        description="Draws an overlay to highlight the active grouping",
        default=False,
        update=update_outline_active,
        options=set(),
    )
    collection: PointerProperty(
        type=bpy.types.Collection,
        name="collection",
        description="master collection containing all groupings",
    )
    version: IntVectorProperty(
        name="version",
        description="the version of the bookgen add-on",
        default=(-1, -1, -1),
    )


class BookGenProperties(bpy.types.PropertyGroup):
    """
    This contains the settings of a shelf including book-shape, alignment and leaning.
    """

    log = logging.getLogger("bookGen.properties")
    def update(self, context):
        """Use immediate or lazy update based on add-on preferences

        Args:
            context (bpy.types.Context): the execution context
        """
        addon = context.preferences.addons.get(__package__)
        preferences = addon.preferences if addon else None
        if getattr(preferences, "lazy_update", True):
            self.update_delayed(context)
        else:
            self.update_immediate(context)

    def update_immediate(self, context):
        """
        Updates the scene using the settings in this property group.
        """
        properties = context.scene.BookGenAddonProperties

        if properties.auto_rebuild:
            bpy.ops.bookgen.rebuild(settings_name=self.name)

    def update_delayed(self, context):
        """
        Queue one targeted rebuild after the user stops changing a value.
        """
        global _update_callback
        properties = context.scene.BookGenAddonProperties

        if not properties.auto_rebuild:
            return

        _pending_settings.add(self.name)
        if _update_callback is not None and bpy.app.timers.is_registered(_update_callback):
            bpy.app.timers.unregister(_update_callback)

        addon = context.preferences.addons.get(__package__)
        preferences = addon.preferences if addon else None
        delay = getattr(preferences, "update_delay", 0.35)
        _update_callback = _run_pending_updates
        bpy.app.timers.register(_update_callback, first_interval=delay)

    def get_name(self):
        return self.get("name", "BookGenSettings")

    def set_name(self, name):
        old_name = self.name
        self["name"] = name
        if name != old_name:
            for collection in get_bookgen_collection(
                bpy.context
            ).children:  # TODO we should not use the global context here
                if collection.BookGenGroupingProperties.settings_name == old_name:
                    collection.BookGenGroupingProperties.settings_name = name

    def apply_book_preset(self, context):
        """Apply a researched real-world size preset with one debounced rebuild."""
        if self.book_preset == "CUSTOM":
            self.update(context)
            return
        preset = BOOK_PRESETS.get(self.book_preset)
        if preset is None:
            return
        for property_name, value in preset["values"].items():
            self[property_name] = value
        self.update(context)

    # general
    name: StringProperty(
        name="name",
        default="BookGenSettings",
        set=set_name,
        get=get_name,
        options=set(),
    )

    book_preset: EnumProperty(
        name="Book Type Preset",
        description="Apply real-world dimensions and matching construction details",
        items=book_preset_items,
        default=0,
        update=apply_book_preset,
        options=set(),
    )

    mix_reference_enabled: BoolProperty(
        name="Classic / Dictionary (Thick)",
        description="Include thick classic and dictionary books in the mix",
        default=True,
        update=update,
        options=set(),
    )
    mix_reference_percentage: FloatProperty(
        name="Dictionary Percentage",
        description="Relative generation percentage for thick dictionary books",
        subtype="PERCENTAGE",
        min=0.0,
        max=100.0,
        default=33.34,
        update=update,
        options=set(),
    )
    mix_novel_enabled: BoolProperty(
        name="Trade Novel / Reader",
        description="Include novels and readers in the mix",
        default=True,
        update=update,
        options=set(),
    )
    mix_novel_percentage: FloatProperty(
        name="Novel Percentage",
        description="Relative generation percentage for novels and readers",
        subtype="PERCENTAGE",
        min=0.0,
        max=100.0,
        default=33.33,
        update=update,
        options=set(),
    )
    mix_magazine_enabled: BoolProperty(
        name="US Letter Magazine",
        description="Include magazines in the mix",
        default=True,
        update=update,
        options=set(),
    )
    mix_magazine_percentage: FloatProperty(
        name="Magazine Percentage",
        description="Relative generation percentage for magazines",
        subtype="PERCENTAGE",
        min=0.0,
        max=100.0,
        default=33.33,
        update=update,
        options=set(),
    )

    # shelf
    scale: FloatProperty(name="scale", min=0.1, default=1, update=update, options=set())

    seed: IntProperty(name="seed", default=0, update=update, options=set())

    random_spine_side: BoolProperty(
        name="random spine side",
        description="Randomly flip selected books so the spine or fore edge faces the opposite side",
        default=False,
        update=update,
        options=set(),
    )
    flipped_book_percentage: FloatProperty(
        name="flipped books",
        description="Percentage of books rotated 180 degrees to reverse spine and fore-edge sides",
        subtype="PERCENTAGE",
        min=0.0,
        max=100.0,
        default=25.0,
        update=update,
        options=set(),
    )

    group_curve: FloatProperty(
        name="overall curve",
        description="Bend the layout from a fixed start to this tangent angle at the endpoint",
        subtype="ANGLE",
        unit="ROTATION",
        min=-pi,
        max=pi,
        soft_min=-radians(60),
        soft_max=radians(60),
        default=0.0,
        update=update,
        options=set(),
    )
    stack_side_curve: FloatProperty(
        name="stack side curve",
        description="Bend stacked layer positions left or right from the fixed base",
        subtype="ANGLE",
        unit="ROTATION",
        min=-pi,
        max=pi,
        soft_min=-radians(60),
        soft_max=radians(60),
        default=0.0,
        update=update,
        options=set(),
    )

    alignment: EnumProperty(
        name="alignment",
        items=alignment_items,
        update=update,
        options=set(),
    )

    shelf_depth_offset: FloatProperty(
        name="depth offset",
        description="Maximum random book displacement along the shelf depth direction",
        min=0.0,
        soft_max=0.05,
        default=0.015,
        unit="LENGTH",
        update=update,
        options=set(),
    )
    shelf_offset_chance: FloatProperty(
        name="offset chance",
        description="Probability that an individual shelf book receives a depth offset",
        subtype="FACTOR",
        min=0.0,
        max=1.0,
        default=0.35,
        update=update,
        options=set(),
    )
    shelf_offset_bias: FloatProperty(
        name="inset protrude bias",
        description="Negative favors inset books; positive favors books protruding toward the fore edge",
        min=-1.0,
        max=1.0,
        default=-0.35,
        update=update,
        options=set(),
    )

    stack_planar_offset: FloatProperty(
        name="stack planar offset",
        description="Maximum random layer displacement in one of four local planar directions",
        min=0.0,
        soft_max=0.05,
        default=0.015,
        unit="LENGTH",
        update=update,
        options=set(),
    )
    stack_offset_chance: FloatProperty(
        name="stack offset chance",
        description="Probability that an individual stacked book moves left, right, backward, or forward",
        subtype="FACTOR",
        min=0.0,
        max=1.0,
        default=0.5,
        update=update,
        options=set(),
    )

    lean_amount: FloatProperty(
        name="lean amount",
        subtype="FACTOR",
        min=0.0,
        soft_max=1.0,
        update=update,
        options=set(),
    )

    lean_direction: FloatProperty(
        name="lean direction",
        subtype="FACTOR",
        min=-1,
        max=1,
        default=0,
        update=update,
        options=set(),
    )

    lean_angle: FloatProperty(
        name="lean angle",
        unit="ROTATION",
        min=0.0,
        soft_max=radians(30),
        max=pi / 2.0,
        default=radians(8),
        update=update,
        options=set(),
    )
    rndm_lean_angle_factor: FloatProperty(
        name="random",
        default=1,
        min=0.0,
        soft_max=1,
        subtype="FACTOR",
        update=update,
        options=set(),
    )

    # stack
    rotation: FloatProperty(
        name="rotation",
        subtype="FACTOR",
        min=0.0,
        max=1.0,
        update=update,
        options=set(),
    )

    stack_top_face: EnumProperty(
        name="stack top face",
        items=stack_top_face_items,
        update=update,
        default=0,
        options=set(),
    )

    # books

    book_height: FloatProperty(
        name="height",
        default=0.15,
        min=0.05,
        step=0.005,
        unit="LENGTH",
        update=update,
        options=set(),
    )
    rndm_book_height_factor: FloatProperty(
        name=" random",
        default=1,
        min=0.0,
        soft_max=1,
        subtype="FACTOR",
        update=update,
        options=set(),
    )

    book_width: FloatProperty(
        name="width",
        default=0.03,
        min=0.002,
        step=0.001,
        unit="LENGTH",
        update=update,
        options=set(),
    )
    rndm_book_width_factor: FloatProperty(
        name="random",
        default=1,
        min=0.0,
        soft_max=1,
        subtype="FACTOR",
        update=update,
        options=set(),
    )

    book_depth: FloatProperty(
        name="depth",
        default=0.12,
        min=0.0,
        step=0.005,
        unit="LENGTH",
        update=update,
        options=set(),
    )
    rndm_book_depth_factor: FloatProperty(
        name="random",
        default=1,
        min=0.0,
        soft_max=1,
        subtype="FACTOR",
        update=update,
        options=set(),
    )

    cover_thickness: FloatProperty(
        name="cover thickness",
        default=0.002,
        min=0.0,
        soft_max=0.01,
        step=1,
        precision=4,
        unit="LENGTH",
        update=update,
        options=set(),
    )
    rndm_cover_thickness_factor: FloatProperty(
        name="random",
        default=1,
        min=0.0,
        soft_max=1,
        subtype="FACTOR",
        update=update,
        options=set(),
    )

    textblock_offset: FloatProperty(
        name="textblock offset",
        default=0.005,
        min=0.0,
        soft_max=0.02,
        step=1,
        precision=4,
        unit="LENGTH",
        update=update,
        options=set(),
    )
    rndm_textblock_offset_factor: FloatProperty(
        name="random",
        default=1,
        min=0.0,
        soft_max=1,
        subtype="FACTOR",
        update=update,
        options=set(),
    )

    spine_curl: FloatProperty(
        name="spine curl",
        default=0.002,
        soft_max=0.02,
        step=1,
        precision=4,
        min=0.0,
        unit="LENGTH",
        update=update,
        options=set(),
    )
    spine_rounding: FloatProperty(
        name="spine rounding",
        description="Round the outer spine across a percentage of its full sloped surface width",
        subtype="FACTOR",
        min=0.0,
        max=1.0,
        default=1.0,
        update=update,
        options=set(),
    )
    page_curve_match: FloatProperty(
        name="page curve match",
        description="Match the text-block spine edge to the inner cover curve; 0 is straight and 1 is matched",
        min=0.0,
        max=2.0,
        default=1.0,
        precision=2,
        update=update,
        options=set(),
    )
    page_front_curve: FloatProperty(
        name="page front curve",
        description="Curve the page fore edge; 0 is straight, positive is concave, and negative is convex",
        min=-1.0,
        max=3.0,
        default=0.6,
        precision=2,
        update=update,
        options=set(),
    )
    page_front_roundness: FloatProperty(
        name="page front roundness",
        description="Blend the fore edge from a pointed profile to a smooth circular profile",
        subtype="FACTOR",
        min=0.0,
        max=1.0,
        default=1.0,
        update=update,
        options=set(),
    )
    page_curve_segments: EnumProperty(
        name="curve segments",
        description="Shared even resolution for outer spine, inner spine, page back, and page front curves",
        items=(
            ("4", "4", "Four page curve segments"),
            ("6", "6", "Six page curve segments"),
            ("8", "8", "Eight page curve segments"),
            ("10", "10", "Ten page curve segments"),
            ("12", "12", "Twelve page curve segments"),
        ),
        default="6",
        update=update,
        options=set(),
    )
    low_poly_segments: EnumProperty(
        name="low poly segments",
        description="Side-curve rail count used only by Low Poly book presets",
        items=low_poly_segment_items,
        default=1,
        update=update,
        options=set(),
    )
    spine_segments: IntProperty(
        name="spine segments",
        description="Number of longitudinal surface strips across the rounded spine",
        min=1,
        max=8,
        default=4,
        update=update,
        options=set(),
    )
    rndm_spine_curl_factor: FloatProperty(
        name="random",
        default=1,
        min=0.0,
        soft_max=1,
        subtype="FACTOR",
        update=update,
        options=set(),
    )

    hinge_inset: FloatProperty(
        name="hinge inset",
        default=0.001,
        min=0.0,
        soft_max=0.005,
        step=1,
        precision=4,
        unit="LENGTH",
        update=update,
        options=set(),
    )
    rndm_hinge_inset_factor: FloatProperty(
        name="random",
        default=1,
        min=0.0,
        soft_max=1,
        subtype="FACTOR",
        update=update,
        options=set(),
    )

    hinge_width: FloatProperty(
        name="hinge width",
        default=0.004,
        min=0.0,
        soft_max=0.02,
        step=1,
        precision=4,
        unit="LENGTH",
        update=update,
        options=set(),
    )
    rndm_hinge_width_factor: FloatProperty(
        name="random",
        default=1,
        min=0.0,
        soft_max=1,
        subtype="FACTOR",
        update=update,
        options=set(),
    )

    subsurf: BoolProperty(
        name="Add Subsurf-Modifier",
        default=False,
        update=update,
        options=set(),
    )

    cover_material: PointerProperty(
        name="Cover Material",
        type=bpy.types.Material,
        update=update,
        options=set(),
    )

    page_material: PointerProperty(
        name="Page Material",
        type=bpy.types.Material,
        update=update,
        options=set(),
    )

    random_cover_colors: BoolProperty(
        name="Random Cover Colors",
        description="Create deterministic cover colors between the two palette colors",
        default=False,
        update=update,
        options=set(),
    )

    cover_color_primary: FloatVectorProperty(
        name="Color A",
        description="First color in the generated cover palette",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.08, 0.18, 0.32, 1.0),
        update=update,
        options=set(),
    )

    cover_color_secondary: FloatVectorProperty(
        name="Color B",
        description="Second color in the generated cover palette",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.55, 0.12, 0.07, 1.0),
        update=update,
        options=set(),
    )

    cover_roughness: FloatProperty(
        name="Cover Roughness",
        description="Roughness of generated cover materials",
        subtype="FACTOR",
        min=0.0,
        max=1.0,
        default=0.55,
        update=update,
        options=set(),
    )

    # UI-only centimeter proxies. Internal and persisted values remain meters.
    book_height_cm: centimeter_property("book_height", "Book Height (cm)", 5.0, 50.0)
    book_depth_cm: centimeter_property("book_depth", "Book Depth (cm)", 0.0, 40.0)
    book_width_cm: centimeter_property("book_width", "Book Thickness (cm)", 0.2, 10.0)
    cover_thickness_cm: centimeter_property("cover_thickness", "Cover Thickness (cm)", 0.0, 1.0)
    textblock_offset_cm: centimeter_property("textblock_offset", "Text Block Inset (cm)", 0.0, 2.0)
    spine_curl_cm: centimeter_property("spine_curl", "Spine Curl (cm)", 0.0, 2.0)
    hinge_inset_cm: centimeter_property("hinge_inset", "Hinge Inset (cm)", 0.0, 0.5)
    hinge_width_cm: centimeter_property("hinge_width", "Hinge Width (cm)", 0.0, 2.0)
    shelf_depth_offset_cm: centimeter_property("shelf_depth_offset", "Depth Offset (cm)", 0.0, 5.0)
    stack_planar_offset_cm: centimeter_property("stack_planar_offset", "Planar Offset (cm)", 0.0, 5.0)


class BookGenGroupingProperties(bpy.types.PropertyGroup):
    """
    This describes how a grouping of books
    what type of grouping it is
    is positioned in 3d space,
    what settings it uses
    """

    """
    This describes how a shelf is positioned in 3D space.
    """
    start: FloatVectorProperty(name="start")
    end: FloatVectorProperty(name="end")
    normal: FloatVectorProperty(name="normal")

    """
    This describes how a stack is positioned in 3D space.
    """
    origin: FloatVectorProperty(name="origin")
    forward: FloatVectorProperty(name="forward")
    normal: FloatVectorProperty(name="normal")
    height: FloatProperty(name="height")

    grouping_type: EnumProperty(
        items=(("SHELF", "shelf", ""), ("STACK", "stack", "")),
        name="grouping_type",
        description="Test",
        default="SHELF",
    )
    id: IntProperty(name="id")
    settings_name: StringProperty("Settings name")
