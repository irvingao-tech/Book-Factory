"""Real-world book dimension presets and their research sources."""

BOOK_PRESETS = {
    "REFERENCE": {
        "label": "Classic / Dictionary (Thick)",
        "dimensions_mm": (247.65, 184.15, 53.34),
        "source": "https://www.amazon.com/dp/0877798095",
        "values": {
            "book_height": 0.24765,
            "book_depth": 0.18415,
            "book_width": 0.05334,
            "cover_thickness": 0.003,
            "textblock_offset": 0.008,
            "spine_curl": 0.004,
            "hinge_inset": 0.0015,
            "hinge_width": 0.006,
            "rndm_book_height_factor": 0.2,
            "rndm_book_depth_factor": 0.15,
            "rndm_book_width_factor": 0.45,
            "rndm_cover_thickness_factor": 0.15,
            "rndm_textblock_offset_factor": 0.25,
            "rndm_spine_curl_factor": 0.35,
            "rndm_hinge_inset_factor": 0.25,
            "rndm_hinge_width_factor": 0.25,
        },
    },
    "NOVEL": {
        "label": "Trade Novel / Reader",
        "dimensions_mm": (228.6, 152.4, 19.05),
        "source": "https://kdp.amazon.com/en_US/help/topic/GVBQ3CMEQW3W2VL6",
        "values": {
            "book_height": 0.2286,
            "book_depth": 0.1524,
            "book_width": 0.01905,
            "cover_thickness": 0.0006,
            "textblock_offset": 0.004,
            "spine_curl": 0.0015,
            "hinge_inset": 0.0004,
            "hinge_width": 0.0025,
            "rndm_book_height_factor": 0.3,
            "rndm_book_depth_factor": 0.25,
            "rndm_book_width_factor": 0.5,
            "rndm_cover_thickness_factor": 0.25,
            "rndm_textblock_offset_factor": 0.3,
            "rndm_spine_curl_factor": 0.4,
            "rndm_hinge_inset_factor": 0.25,
            "rndm_hinge_width_factor": 0.3,
        },
    },
    "MAGAZINE": {
        "label": "US Letter Magazine (64 pages)",
        "dimensions_mm": (279.4, 215.9, 5.0),
        "source": "https://mixam.com/support/sizes",
        "values": {
            "book_height": 0.2794,
            "book_depth": 0.2159,
            "book_width": 0.005,
            "cover_thickness": 0.00025,
            "textblock_offset": 0.0015,
            "spine_curl": 0.0004,
            "hinge_inset": 0.00015,
            "hinge_width": 0.001,
            "rndm_book_height_factor": 0.1,
            "rndm_book_depth_factor": 0.1,
            "rndm_book_width_factor": 0.35,
            "rndm_cover_thickness_factor": 0.2,
            "rndm_textblock_offset_factor": 0.2,
            "rndm_spine_curl_factor": 0.25,
            "rndm_hinge_inset_factor": 0.2,
            "rndm_hinge_width_factor": 0.2,
        },
    },
}

for preset in BOOK_PRESETS.values():
    preset["low_poly"] = False

for source_key, low_poly_key in (
    ("REFERENCE", "REFERENCE_LOW"),
    ("NOVEL", "NOVEL_LOW"),
    ("MAGAZINE", "MAGAZINE_LOW"),
):
    source = BOOK_PRESETS[source_key]
    BOOK_PRESETS[low_poly_key] = {
        "label": f"{source['label']} - Low Poly",
        "dimensions_mm": source["dimensions_mm"],
        "source": source["source"],
        "low_poly": True,
        "values": dict(source["values"]),
    }

MIX_PRESET_OPTIONS = (
    ("REFERENCE", "mix_reference_enabled", "mix_reference_percentage"),
    ("NOVEL", "mix_novel_enabled", "mix_novel_percentage"),
    ("MAGAZINE", "mix_magazine_enabled", "mix_magazine_percentage"),
)

MIX_DETAIL_BASE = {
    "cover_thickness": 0.0006,
    "textblock_offset": 0.004,
    "spine_curl": 0.0015,
    "hinge_inset": 0.0004,
    "hinge_width": 0.0025,
}

MIX_DIMENSION_KEYS = (
    "book_height",
    "book_depth",
    "book_width",
    "rndm_book_height_factor",
    "rndm_book_depth_factor",
    "rndm_book_width_factor",
)


def resolve_generation_parameters(parameters):
    """Return generation parameters for the selected single preset type."""
    return parameters
