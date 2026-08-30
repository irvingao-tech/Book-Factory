"""
Contains the preferences of bookGen that allow adjust the overall behavior
"""
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, EnumProperty, FloatProperty

from .translations import tr


def update_language(_self, context):
    """Redraw all areas immediately after changing the add-on language."""
    window_manager = getattr(context, "window_manager", None)
    if window_manager is None:
        return
    for window in window_manager.windows:
        for area in window.screen.areas:
            area.tag_redraw()


class BOOKGEN_AddonPreferences(AddonPreferences):
    """
    The add-on preferences allow to adjust the overall behavior of bookGen
    """

    bl_idname = __package__

    interface_language: EnumProperty(
        name="Language",
        description="Book Factory interface language",
        items=(
            ("ENGLISH", "English", "Display Book Factory in English"),
            ("CHINESE", "中文", "使用中文显示 Book Factory"),
            ("JAPANESE", "日本語", "Book Factoryを日本語で表示"),
        ),
        default="ENGLISH",
        update=update_language,
    )

    lazy_update: BoolProperty(
        name="Debounced updates",
        default=True,
        description="Rebuild once after parameter adjustment stops instead of rebuilding for every slider event",
    )

    update_delay: FloatProperty(
        name="Update delay",
        description="Seconds to wait after the last parameter change before rebuilding",
        min=0.1,
        max=2.0,
        default=0.35,
        subtype="TIME",
    )

    stack_angle_snap: EnumProperty(
        name="Stack direction snap",
        description="Angle increment used while choosing a Stack forward direction",
        items=(
            ("5", "5°", "Snap every 5 degrees"),
            ("10", "10°", "Snap every 10 degrees"),
            ("15", "15°", "Snap every 15 degrees"),
            ("30", "30°", "Snap every 30 degrees"),
            ("45", "45°", "Snap every 45 degrees"),
        ),
        default="15",
    )

    def draw(self, context):
        """Draws the add-on preferences

        Args:
            _context (bpy.types.Context): the execution context
        """
        layout = self.layout
        layout.prop(self, "interface_language", text=tr(context, "Language"))
        layout.separator()
        layout.label(text=tr(context, "Debounced updates improve responsiveness for large book collections."))
        layout.prop(self, "lazy_update", text=tr(context, "Debounced updates"))
        row = layout.row()
        row.enabled = self.lazy_update
        row.prop(self, "update_delay", text=tr(context, "Update delay"))
        layout.separator()
        layout.prop(self, "stack_angle_snap", text=tr(context, "Stack direction snap"))
