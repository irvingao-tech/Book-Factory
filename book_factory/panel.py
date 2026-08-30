"""
This file contains the UI panels.
"""

import bpy

from .utils import (
    get_bookgen_collection,
    get_active_settings,
    get_active_grouping,
    has_bookgen_collection,
)
from .presets import BOOK_PRESETS
from .translations import tr


def active_grouping_is(context, grouping_type):
    """Return whether the selected BookGen group matches the requested type."""
    grouping = get_active_grouping(context, create=False)
    return bool(grouping and grouping.BookGenGroupingProperties.grouping_type == grouping_type)


class BOOKGEN_PT_LayoutPanel(bpy.types.Panel):
    """Draw settings shared by shelf and stack layouts."""

    bl_label = "Layout & Variation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BookGen"
    bl_options = set()
    bl_order = 1

    @classmethod
    def poll(cls, context):
        return False

    def draw(self, context):
        properties = get_active_settings(context)
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.prop(properties, "scale", text="Global Scale")
        layout.prop(properties, "seed", text="Random Seed")
        layout.prop(properties, "group_curve", text="Overall Curve")


class BOOKGEN_PT_ShelfPanel(bpy.types.Panel):
    """
    Draws the main shelf settings panel.
    """

    bl_label = "Shelf Layout"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BookGen"
    bl_options = set()
    bl_order = 2

    @classmethod
    def poll(self, context):
        return False

    def draw(self, context):
        """Draws the shelf settings panel

        Args:
            context (bpy.types.Context): the execution context
        """
        properties = get_active_settings(context)
        if not properties:
            return

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(properties, "alignment", text="Alignment")


class BOOKGEN_PT_StackPanel(bpy.types.Panel):
    """
    Draws the main stack settings panel.
    """

    bl_label = "Stack Layout"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BookGen"
    bl_options = set()
    bl_order = 2

    @classmethod
    def poll(self, context):
        return False

    def draw(self, context):
        """Draws the stack settings panel

        Args:
            context (bpy.types.Context): the execution context
        """
        properties = get_active_settings(context)
        if not properties:
            return

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(properties, "rotation", text="Rotation Variation")

        layout.prop(properties, "stack_top_face", text="Top Face")
        layout.label(text="Grouped by type; larger covers are placed lower", icon="SORT_DESC")


class BOOKGEN_PT_LeaningPanel(bpy.types.Panel):
    """
    Draws the leaning settings panel.
    """

    bl_label = "Leaning"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BookGen"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "BOOKGEN_PT_ShelfPanel"

    @classmethod
    def poll(self, context):
        return False

    def draw(self, context):
        """Draws the leaning settings panel.

        Args:
            context (bpy.types.Context): the execution context
        """
        properties = get_active_settings(context)
        if not properties:
            return
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(properties, "lean_amount", text="Lean Amount")
        layout.prop(properties, "lean_direction", text="Lean Direction")
        col = layout.column(align=True)
        col.prop(properties, "lean_angle", text="Lean Angle")
        col.prop(properties, "rndm_lean_angle_factor", text="Variation")


class BOOKGEN_PT_ProportionsPanel(bpy.types.Panel):
    """
    Draws book proportions panel.
    """

    bl_label = "Dimensions & Materials"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BookGen"
    bl_options = set()
    bl_parent_id = "BOOKGEN_PT_BookPanel"

    @classmethod
    def poll(self, context):
        return False

    def draw(self, context):
        """Draws the proportion settings panel

        Args:
            context (bpy.types.Context): the execution context
        """
        properties = get_active_settings(context)
        if not properties:
            return

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        if properties.book_preset == "MIX":
            info = layout.box()
            info.label(text="Mix details scale each type's own baseline", icon="INFO")

        col = layout.column(align=True)
        col.prop(properties, "book_height_cm", text="Book Height (cm)")
        col.prop(properties, "rndm_book_height_factor", text="Variation")

        col = layout.column(align=True)
        col.prop(properties, "book_depth_cm", text="Book Depth (cm)")
        col.prop(properties, "rndm_book_depth_factor", text="Variation")

        col = layout.column(align=True)
        col.prop(properties, "book_width_cm", text="Book Thickness (cm)")
        col.prop(properties, "rndm_book_width_factor", text="Variation")

        layout.separator()
        layout.prop(properties, "random_cover_colors", text="Random Cover Colors")
        if properties.random_cover_colors:
            row = layout.row(align=True)
            row.prop(properties, "cover_color_primary", text="Color A")
            row.prop(properties, "cover_color_secondary", text="Color B")
            layout.prop(properties, "cover_roughness", text="Cover Roughness")
        else:
            layout.prop(properties, "cover_material", text="Cover Material")
        layout.prop(properties, "page_material", text="Page Material")


class BOOKGEN_PT_BookPanel(bpy.types.Panel):
    """
    Draws the book  panel
    """

    bl_label = "Book Appearance"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BookGen"
    bl_order = 3

    @classmethod
    def poll(self, context):
        return False

    def draw(self, context):
        properties = get_active_settings(context)
        if not properties:
            return

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.prop(properties, "book_preset", text="Book Type Preset")

        preset = BOOK_PRESETS.get(properties.book_preset)
        if preset:
            height, depth, thickness = (value / 10.0 for value in preset["dimensions_mm"])
            box = layout.box()
            box.label(text=f"Height: {height:g} cm")
            box.label(text=f"Cover width: {depth:g} cm")
            box.label(text=f"Thickness: {thickness:g} cm")
        elif properties.book_preset == "MIX":
            box = layout.box()
            mix_rows = (
                ("Classic / Dictionary (Thick)", "mix_reference_enabled", "mix_reference_percentage"),
                ("Trade Novel / Reader", "mix_novel_enabled", "mix_novel_percentage"),
                ("US Letter Magazine", "mix_magazine_enabled", "mix_magazine_percentage"),
            )
            active_total = 0.0
            for label, enabled_name, percentage_name in mix_rows:
                enabled = getattr(properties, enabled_name)
                row = box.row(align=True)
                row.prop(properties, enabled_name, text=label)
                percentage = row.row(align=True)
                percentage.enabled = enabled
                percentage.prop(properties, percentage_name, text="")
                if enabled:
                    active_total += getattr(properties, percentage_name)

            translate = bpy.app.translations.pgettext_iface
            box.label(text=f"{translate('Active total')}: {active_total:.2f}%")
            if active_total <= 0.0:
                warning = box.row()
                warning.alert = True
                warning.label(text=translate("No active weight; falling back to Novel"), icon="ERROR")
            elif abs(active_total - 100.0) > 0.01:
                box.label(text=translate("Percentages are normalized automatically"), icon="INFO")


class BOOKGEN_PT_DetailsPanel(bpy.types.Panel):
    """
    Draws the book details panel
    """

    bl_label = "Model Details"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BookGen"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "BOOKGEN_PT_BookPanel"

    @classmethod
    def poll(self, context):
        return False

    def draw(self, context):
        """Draws the detail settings panel

        Args:
            context (bpy.types.Context): the execution context
        """

        properties = get_active_settings(context)
        if not properties:
            return
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column(align=True)
        col.prop(properties, "textblock_offset_cm", text="Text Block Inset (cm)")
        col.prop(properties, "rndm_textblock_offset_factor", text="Variation")

        col = layout.column(align=True)
        col.prop(properties, "cover_thickness_cm", text="Cover Thickness (cm)")
        col.prop(properties, "rndm_cover_thickness_factor", text="Variation")

        col = layout.column(align=True)
        col.prop(properties, "spine_curl_cm", text="Spine Curl (cm)")
        col.prop(properties, "rndm_spine_curl_factor", text="Variation")
        col.prop(properties, "spine_rounding", text="Spine Roundness")
        col.prop(properties, "page_curve_match", text="Page Curve Match")
        col.prop(properties, "page_front_curve", text="Page Front Curve")
        col.prop(properties, "page_front_roundness", text="Page Front Roundness")
        if BOOK_PRESETS.get(properties.book_preset, {}).get("low_poly"):
            col.prop(properties, "low_poly_segments", text="Low Poly Segments")
        else:
            col.prop(properties, "page_curve_segments", text="Curve Segments")

        col = layout.column(align=True)
        col.prop(properties, "hinge_inset_cm", text="Hinge Inset (cm)")
        col.prop(properties, "rndm_hinge_inset_factor", text="Variation")

        col = layout.column(align=True)
        col.prop(properties, "hinge_width_cm", text="Hinge Width (cm)")
        col.prop(properties, "rndm_hinge_width_factor", text="Variation")

        layout.separator()



class BOOKGEN_PT_MainPanel(bpy.types.Panel):
    """
    Draws the main bookgen panel
    """

    bl_label = "Book Factory V1.1"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Book Factory"
    bl_options = set()
    bl_order = 0

    def draw(self, context):
        """Draw the compact adaptive BookGen interface."""
        ui_state = context.scene.BookGenAddonProperties
        icons = context.scene.bookgen_icons
        layout = self.layout
        layout.use_property_decorate = False
        t = lambda text: tr(context, text)

        mode_row = layout.row(align=True)
        shelf_tab = mode_row.operator(
            "bookgen.set_ui_mode", text=t("Shelf"), depress=ui_state.ui_mode == "SHELF"
        )
        shelf_tab.grouping_type = "SHELF"
        stack_tab = mode_row.operator(
            "bookgen.set_ui_mode", text=t("Stack"), depress=ui_state.ui_mode == "STACK"
        )
        stack_tab.grouping_type = "STACK"

        add_row = layout.row()
        add_row.scale_y = 1.35
        if ui_state.ui_mode == "SHELF":
            add_row.operator("bookgen.select_shelf", text=t("Add Shelf"), icon_value=icons["shelf"].icon_id)
        else:
            add_row.operator("bookgen.select_stack", text=t("Add Stack"), icon_value=icons["stack"].icon_id)

        group_collection = get_bookgen_collection(context, create=False)
        active_group = get_active_grouping(context, create=False)
        if group_collection:
            group_row = layout.row()
            group_row.template_list(
                "BOOKGEN_UL_Shelves",
                "compact",
                group_collection,
                "children",
                ui_state,
                "active_shelf",
                rows=2,
            )
            group_actions = group_row.column(align=True)
            group_actions.operator("bookgen.remove_grouping", icon="X", text="")
            group_actions.prop(ui_state, "outline_active", icon="SHADING_BBOX", icon_only=True)
            group_actions.operator("bookgen.unlink_grouping", icon="UNLINKED", text="")

        if active_group:
            group_type = t(active_group.BookGenGroupingProperties.grouping_type.title())
            active_card = layout.box()
            active_card.label(text=f"{group_type}  |  {active_group.name}", icon="OUTLINER_COLLECTION")

        settings = get_active_settings(context, create=False)
        if settings is None:
            layout.label(text=t("Add or select a Book Factory group to edit its settings"), icon="INFO")
            return

        settings_row = layout.row(align=True)
        settings_row.label(text="", icon="PREFERENCES")
        settings_row.prop(settings, "name", text="")

        def section(toggle_name, label, icon):
            box = layout.box()
            header = box.row()
            expanded = getattr(ui_state, toggle_name)
            header.prop(
                ui_state,
                toggle_name,
                text=t(label),
                icon="TRIA_DOWN" if expanded else "TRIA_RIGHT",
                emboss=False,
            )
            if expanded:
                content = box.column(align=True)
                content.use_property_split = True
                content.use_property_decorate = False
                return content
            return None

        def dimension_row(parent, value_name, variation_name, label):
            row = parent.row(align=True)
            row.prop(settings, value_name, text=t(label))
            row.prop(settings, variation_name, text=t("Var"))

        appearance = section("show_appearance", "Book Appearance", "BOOKMARKS")
        if appearance:
            appearance.prop(settings, "book_preset", text=t("Book Type Preset"))
            if settings.book_preset == "MIX":
                mix_rows = (
                    ("Dictionary", "mix_reference_enabled", "mix_reference_percentage"),
                    ("Novel", "mix_novel_enabled", "mix_novel_percentage"),
                    ("Magazine", "mix_magazine_enabled", "mix_magazine_percentage"),
                )
                for label, enabled_name, percentage_name in mix_rows:
                    row = appearance.row(align=True)
                    row.prop(settings, enabled_name, text=label)
                    weight = row.row(align=True)
                    weight.enabled = getattr(settings, enabled_name)
                    weight.prop(settings, percentage_name, text="")
            else:
                preset = BOOK_PRESETS.get(settings.book_preset)
                if preset:
                    height, depth, thickness = (value / 10.0 for value in preset["dimensions_mm"])
                    summary = appearance.row(align=True)
                    summary.label(text=f"H {height:g}")
                    summary.label(text=f"W {depth:g}")
                    summary.label(text=f"T {thickness:g} cm")
                    if preset.get("low_poly"):
                        appearance.label(text=t("Single connected outer shell"), icon="MESH_CUBE")
            appearance.separator(factor=0.5)
            dimension_row(appearance, "book_height_cm", "rndm_book_height_factor", "Height (cm)")
            dimension_row(appearance, "book_depth_cm", "rndm_book_depth_factor", "Cover Width (cm)")
            dimension_row(appearance, "book_width_cm", "rndm_book_width_factor", "Thickness (cm)")

        layout_card = section("show_layout", "Layout & Variation", "ORIENTATION_GLOBAL")
        if layout_card:
            layout_card.prop(settings, "scale", text=t("Global Scale"))
            layout_card.prop(settings, "seed", text=t("Random Seed"))
            layout_card.separator(factor=0.5)
            if active_grouping_is(context, "SHELF"):
                layout_card.prop(settings, "group_curve", text=t("Overall Curve"))
                layout_card.prop(settings, "alignment", text=t("Alignment"))
                layout_card.prop(settings, "shelf_depth_offset_cm", text=t("Depth Offset (cm)"))
                layout_card.prop(settings, "shelf_offset_chance", text=t("Offset Chance"))
                layout_card.prop(settings, "shelf_offset_bias", text=t("Inset / Protrude Bias"))
                layout_card.prop(settings, "lean_amount", text=t("Lean Amount"))
                layout_card.prop(settings, "lean_direction", text=t("Lean Direction"))
                dimension_row(layout_card, "lean_angle", "rndm_lean_angle_factor", "Lean Angle")
            elif active_grouping_is(context, "STACK"):
                layout_card.prop(settings, "group_curve", text=t("Forward Curve"))
                layout_card.prop(settings, "stack_side_curve", text=t("Side Curve"))
                layout_card.prop(settings, "rotation", text=t("Rotation Variation"))
                layout_card.prop(settings, "stack_top_face", text=t("Top Face"))
                layout_card.prop(settings, "stack_planar_offset_cm", text=t("Planar Offset (cm)"))
                layout_card.prop(settings, "stack_offset_chance", text=t("Offset Chance"))
                layout_card.label(text=t("Random direction: Left / Right / Back / Forward"), icon="ORIENTATION_LOCAL")
                layout_card.label(text=t("Grouped by type; larger covers are placed lower"), icon="SORT_DESC")

        details = section("show_details", "Model Details", "MODIFIER")
        if details:
            dimension_row(details, "textblock_offset_cm", "rndm_textblock_offset_factor", "Text Inset (cm)")
            dimension_row(details, "cover_thickness_cm", "rndm_cover_thickness_factor", "Cover (cm)")
            dimension_row(details, "spine_curl_cm", "rndm_spine_curl_factor", "Spine Curl (cm)")
            details.prop(settings, "spine_rounding", text=t("Spine Roundness"))
            details.prop(settings, "page_curve_match", text=t("Page Curve Match"))
            details.prop(settings, "page_front_curve", text=t("Page Front Curve"))
            details.prop(settings, "page_front_roundness", text=t("Page Front Roundness"))
            if BOOK_PRESETS.get(settings.book_preset, {}).get("low_poly"):
                details.prop(settings, "low_poly_segments", text=t("Low Poly Segments"))
            else:
                details.prop(settings, "page_curve_segments", text=t("Curve Segments"))
            dimension_row(details, "hinge_inset_cm", "rndm_hinge_inset_factor", "Hinge Inset (cm)")
            dimension_row(details, "hinge_width_cm", "rndm_hinge_width_factor", "Hinge Width (cm)")

        materials = section("show_materials", "Materials", "MATERIAL")
        if materials:
            materials.prop(settings, "random_cover_colors", text=t("Random Cover Colors"))
            if settings.random_cover_colors:
                color_row = materials.row(align=True)
                color_row.prop(settings, "cover_color_primary", text=t("Color A"))
                color_row.prop(settings, "cover_color_secondary", text=t("Color B"))
                materials.prop(settings, "cover_roughness", text=t("Cover Roughness"))
            else:
                materials.prop(settings, "cover_material", text=t("Cover Material"))
            materials.prop(settings, "page_material", text=t("Page Material"))

        layout.separator()
        layout.prop(ui_state, "auto_rebuild", text=t("Auto Rebuild"), toggle=True)
        action_row = layout.row(align=True)
        action_row.scale_y = 1.35
        action_row.operator("bookgen.rebuild", text=t("Rebuild"), icon_value=icons["rebuild"].icon_id)
        action_row.operator("bookgen.merge_freeze", text=t("Merge & Freeze"), icon="MESH_DATA")
