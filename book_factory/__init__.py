# ====================== BEGIN GPL LICENSE BLOCK ======================
#    This file is part of the  bookGen-addon for generating books in Blender
#    Copyright (c) 2023 Oliver Weissbarth
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ======================= END GPL LICENSE BLOCK ========================

"""
BookGen is a add-on for the 3D graphics software Blender. It allows to procedurally generate books.
"""

from bpy.app.handlers import persistent

from .properties import BookGenProperties, BookGenGroupingProperties, BookGenAddonProperties
from .utils import get_bookgen_version, set_bookgen_version
from .shelf_list import BOOKGEN_UL_Shelves
from .versioning import handle_version_upgrade
from .panel import (
    BOOKGEN_PT_LayoutPanel,
    BOOKGEN_PT_ShelfPanel,
    BOOKGEN_PT_MainPanel,
    BOOKGEN_PT_LeaningPanel,
    BOOKGEN_PT_ProportionsPanel,
    BOOKGEN_PT_DetailsPanel,
    BOOKGEN_PT_BookPanel,
    BOOKGEN_PT_StackPanel,
)

from .generic_operators import (
    BOOKGEN_OT_Rebuild,
    BOOKGEN_OT_CreateSettings,
    BOOKGEN_OT_SetSettings,
    BOOKGEN_OT_RemoveSettings,
    BOOKGEN_OT_RemoveGrouping,
    BOOKGEN_OT_UnlinkGrouping,
    BOOKGEN_OT_SetUIMode,
)
from .shelf_operator import BOOKGEN_OT_SelectShelf

from .stack_operator import BOOKGEN_OT_SelectStack
from .freeze_operator import BOOKGEN_OT_MergeFreeze

from .preferences import BOOKGEN_AddonPreferences
from .translations import TRANSLATIONS

BOOK_FACTORY_VERSION = (1, 1, 0)
DATA_SCHEMA_VERSION = (4, 3, 0)
BOOKGEN_VERSION = BOOK_FACTORY_VERSION

bl_info = {
    "name": "Book Factory",
    "description": "Procedural book shelves, stacks, and editable book assets",
    "author": "Oliver Weissbarth, Seojin Sim; Book Factory contributors",
    "version": BOOKGEN_VERSION,
    "blender": (4, 3, 0),
    "location": "View3D > Sidebar > Book Factory",
    "tracker_url": "https://github.com/irvingao-tech/Book-Factory/issues",
    "support": "COMMUNITY",
    "wiki_url": "https://github.com/irvingao-tech/Book-Factory",
    "category": "Add Mesh",
}


classes = [
    BookGenProperties,
    BookGenGroupingProperties,
    BookGenAddonProperties,
    BOOKGEN_OT_Rebuild,
    BOOKGEN_OT_RemoveGrouping,
    BOOKGEN_OT_UnlinkGrouping,
    BOOKGEN_OT_MergeFreeze,
    BOOKGEN_OT_SetUIMode,
    BOOKGEN_PT_MainPanel,
    BOOKGEN_PT_LayoutPanel,
    BOOKGEN_PT_BookPanel,
    BOOKGEN_PT_ShelfPanel,
    BOOKGEN_PT_LeaningPanel,
    BOOKGEN_PT_ProportionsPanel,
    BOOKGEN_PT_DetailsPanel,
    BOOKGEN_OT_SelectShelf,
    BOOKGEN_UL_Shelves,
    BOOKGEN_OT_SelectStack,
    BOOKGEN_AddonPreferences,
    BOOKGEN_OT_CreateSettings,
    BOOKGEN_OT_SetSettings,
    BOOKGEN_OT_RemoveSettings,
    BOOKGEN_PT_StackPanel,
]


def _unregister_translations():
    """Remove stale translation data left by a failed enable or hot reload."""
    import bpy

    try:
        bpy.app.translations.unregister(__package__)
    except Exception:
        # Blender raises when no cache exists; cleanup must remain idempotent.
        pass


def _migrate_loaded_scenes():
    """Migrate scenes after Blender releases its restricted registration state."""
    import bpy

    if not hasattr(bpy.data, "scenes"):
        return 0.1
    for scene in bpy.data.scenes:
        handle_version_upgrade(scene)
    return None


def _cleanup_stale_registration():
    """Remove complete or partial registrations left by an extension reload."""
    import bpy

    from . import properties

    cancel_update = getattr(properties, "cancel_pending_update", None)
    if cancel_update is not None:
        cancel_update()
    if bpy.app.timers.is_registered(_migrate_loaded_scenes):
        bpy.app.timers.unregister(_migrate_loaded_scenes)

    handler_specs = (
        (bpy.app.handlers.load_post, "bookgen_startup"),
        (bpy.app.handlers.save_pre, "bookgen_mark_version"),
    )
    for handlers, function_name in handler_specs:
        for handler in tuple(handlers):
            if handler.__module__ == __name__ and handler.__name__ == function_name:
                handlers.remove(handler)

    for owner, property_name in (
        (bpy.types.Scene, "BookGenSettings"),
        (bpy.types.Scene, "BookGenAddonProperties"),
        (bpy.types.Collection, "BookGenGroupingProperties"),
    ):
        if hasattr(owner, property_name):
            delattr(owner, property_name)

    rna_bases = (
        bpy.types.PropertyGroup,
        bpy.types.Operator,
        bpy.types.Panel,
        bpy.types.UIList,
        bpy.types.AddonPreferences,
    )
    for cls in reversed(classes):
        registered_class = None
        identifiers = [cls.__name__]
        class_rna = cls.__dict__.get("bl_rna")
        if class_rna is not None:
            identifiers.append(class_rna.identifier)
        if issubclass(cls, bpy.types.Operator) and "." in cls.bl_idname:
            namespace, operator_name = cls.bl_idname.split(".", 1)
            identifiers.append(f"{namespace.upper()}_OT_{operator_name}")

        for identifier in identifiers:
            for rna_base in rna_bases:
                registered_class = rna_base.bl_rna_get_subclass_py(identifier)
                if registered_class is not None:
                    break
            if registered_class is not None:
                break
        if registered_class is None:
            continue
        if cls.__name__ == "BookGenAddonProperties":
            outline = getattr(registered_class, "outline", None)
            if outline is not None:
                outline.disable_outline()
        try:
            bpy.utils.unregister_class(registered_class)
        except RuntimeError:
            pass

    icon_collection = getattr(bpy.types.Scene, "bookgen_icons", None)
    if icon_collection is not None:
        try:
            bpy.utils.previews.remove(icon_collection)
        except Exception:
            pass
        delattr(bpy.types.Scene, "bookgen_icons")

    _unregister_translations()


def register():
    """
    Register all custom operators, panels, ui-lists and properties.
    """
    from bpy.utils import register_class, previews
    import bpy
    import os

    _cleanup_stale_registration()
    try:
        bookgen_icons = previews.new()
        bpy.types.Scene.bookgen_icons = bookgen_icons
        icons_dir = os.path.join(os.path.dirname(__file__), "icons")
        bookgen_icons.load("shelf", os.path.join(icons_dir, "shelf.png"), "IMAGE")
        bookgen_icons.load("stack", os.path.join(icons_dir, "stack.png"), "IMAGE")
        bookgen_icons.load("rebuild", os.path.join(icons_dir, "rebuild.png"), "IMAGE")

        for cls in classes:
            register_class(cls)

        bpy.types.Collection.BookGenGroupingProperties = bpy.props.PointerProperty(type=BookGenGroupingProperties)
        bpy.types.Scene.BookGenSettings = bpy.props.CollectionProperty(type=BookGenProperties)
        bpy.types.Scene.BookGenAddonProperties = bpy.props.PointerProperty(type=BookGenAddonProperties)

        bpy.app.handlers.load_post.append(bookgen_startup)
        bpy.app.handlers.save_pre.append(bookgen_mark_version)

        # Extension loaders may consume or remove legacy bl_info metadata.
        set_bookgen_version(DATA_SCHEMA_VERSION)
        bpy.app.timers.register(_migrate_loaded_scenes, first_interval=0.0)
    except Exception:
        _cleanup_stale_registration()
        raise


def unregister():
    """
    Unregister all custom operators, panels, ui-lists and properties.

    """
    _cleanup_stale_registration()


@persistent
def bookgen_mark_version(_dummy):
    """Stores the version of bookgen in the properties"""
    import bpy

    for s in bpy.data.scenes:
        s.BookGenAddonProperties.version = get_bookgen_version()


@persistent
def bookgen_startup(_dummy):
    """
    Ensure that the outline is disabled on start-up.
    """
    import bpy

    bpy.context.scene.BookGenAddonProperties.outline_active = False

    if not bpy.context.scene.BookGenSettings:
        bpy.context.scene.BookGenSettings.add()

    for s in bpy.data.scenes:
        handle_version_upgrade(s)
