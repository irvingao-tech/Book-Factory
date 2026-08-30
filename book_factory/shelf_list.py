"""
Contains the UIList item for shelf
"""

import bpy
from bpy.props import StringProperty

from .utils import get_bookgen_collection, select_grouping_objects


class BOOKGEN_OT_ActivateGrouping(bpy.types.Operator):
    """Activate a Book Factory group from its list row."""

    bl_idname = "bookgen.activate_grouping"
    bl_label = "Activate Book Group"
    bl_options = {"INTERNAL"}

    grouping_name: StringProperty(options={"HIDDEN"})

    def execute(self, context):
        collection = get_bookgen_collection(context, create=False)
        if collection is None:
            return {"CANCELLED"}
        for index, grouping in enumerate(collection.children):
            if grouping.name != self.grouping_name:
                continue
            context.scene.BookGenAddonProperties.active_shelf = index
            select_grouping_objects(context, grouping)
            return {"FINISHED"}
        return {"CANCELLED"}


class BOOKGEN_UL_Shelves(bpy.types.UIList):
    """Defines the custom UIList item for shelf"""

    def draw_item(self, _context, layout, _data, item, _icon, _active_data, _active_propname):
        """Draws the UIList item for shelf"""
        icon = "BOOKMARKS" if item.BookGenGroupingProperties.grouping_type == "SHELF" else "ALIGN_JUSTIFY"
        operator = layout.operator("bookgen.activate_grouping", text=item.name, icon=icon, emboss=False)
        operator.grouping_name = item.name
