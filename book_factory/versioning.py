"""This file contains versioning functionality
"""
import logging
import bpy

from .presets import MIX_DETAIL_BASE
from .data.faces import normalized_page_segments
from .presets import BOOK_PRESETS
from .utils import copy_bookgen_settings, get_bookgen_version

log = logging.getLogger("bookGen.versioning")


def handle_version_upgrade(scene):
    """Upgrades the given scene to the current bookGen version

    Args:
        scene (bpy.types.Scene): the scene that should be upgraded
    """
    if tuple(scene.BookGenAddonProperties.version) < (1, 0, 1):
        version_upgrade_collection_pointer_property(scene)
    if tuple(scene.BookGenAddonProperties.version) < (2, 4, 1):
        version_upgrade_mix_details(scene)
    if tuple(scene.BookGenAddonProperties.version) < (3, 6, 0):
        version_upgrade_unique_group_settings(scene)
    if tuple(scene.BookGenAddonProperties.version) < (3, 6, 1):
        version_remove_subdivision(scene)
    if tuple(scene.BookGenAddonProperties.version) < (3, 8, 2):
        version_unify_curve_segments(scene)
    if tuple(scene.BookGenAddonProperties.version) < (4, 0, 0):
        version_remove_mix_preset(scene)

    current_version = get_bookgen_version()
    scene.BookGenAddonProperties.version = current_version or (2, 4, 1)


def version_upgrade_mix_details(scene):
    """Reset Mix controls that older versions displayed but ignored."""
    for settings in scene.BookGenSettings:
        if settings.book_preset != "MIX":
            continue
        for property_name, value in MIX_DETAIL_BASE.items():
            settings[property_name] = value


def version_upgrade_unique_group_settings(scene):
    """Give every existing grouping its own independent settings block."""
    collection = scene.BookGenAddonProperties.collection
    if collection is None:
        return
    settings_by_name = {settings.name: settings for settings in scene.BookGenSettings}
    claimed_settings = set()
    for grouping in collection.children:
        settings_name = grouping.BookGenGroupingProperties.settings_name
        source = settings_by_name.get(settings_name)
        if source is None:
            continue
        if settings_name not in claimed_settings:
            claimed_settings.add(settings_name)
            continue
        copied = copy_bookgen_settings(scene, source, f"{grouping.name}_Settings")
        grouping.BookGenGroupingProperties.settings_name = copied.name


def version_remove_subdivision(scene):
    """Disable the retired whole-book subdivision option and remove its modifiers."""
    for settings in scene.BookGenSettings:
        settings["subsurf"] = False
    collection = scene.BookGenAddonProperties.collection
    if collection is None:
        return
    for grouping in collection.children:
        for obj in grouping.objects:
            for modifier in list(obj.modifiers):
                if modifier.type == "SUBSURF":
                    obj.modifiers.remove(modifier)


def version_unify_curve_segments(scene):
    """Use the higher legacy resolution for every spine and page curve."""
    auto_rebuild = scene.BookGenAddonProperties.auto_rebuild
    scene.BookGenAddonProperties.auto_rebuild = False
    try:
        for settings in scene.BookGenSettings:
            segments = normalized_page_segments(
                max(int(settings.spine_segments), int(settings.page_curve_segments))
            )
            settings.spine_segments = segments
            settings.page_curve_segments = str(segments)
    finally:
        scene.BookGenAddonProperties.auto_rebuild = auto_rebuild


def version_remove_mix_preset(scene):
    """Replace removed Mix selections with the ordinary Novel preset."""
    auto_rebuild = scene.BookGenAddonProperties.auto_rebuild
    scene.BookGenAddonProperties.auto_rebuild = False
    try:
        for settings in scene.BookGenSettings:
            raw_value = settings.get("book_preset")
            if raw_value == 4 or settings.book_preset not in {"CUSTOM", *BOOK_PRESETS.keys()}:
                settings.book_preset = "NOVEL"
    finally:
        scene.BookGenAddonProperties.auto_rebuild = auto_rebuild


def version_upgrade_collection_pointer_property(scene):
    """In versions before 1.0.1 the bookGen collection was identified by the name.
        Starting from 1.0.1 the collection is identified by a PointerProperty in BookGenAddonProperties

    Args:
        scene (bpy.types.Scene): the scene that should be upgraded
    """
    log.info("Performing version upgrade: collection_pointer_property on scene %s" % scene.name)
    if "BookGen" in bpy.data.collections.keys():
        scene.BookGenAddonProperties.collection = bpy.data.collections["BookGen"]
    else:
        log.debug("No legacy BookGen collection found; no pointer migration needed.")
