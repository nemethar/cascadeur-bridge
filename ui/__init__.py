if "bpy" not in locals():
    from . import main_panel
    from . import socials
    from . import settings_panel
    from . import arp_panel
else:
    import importlib

    importlib.reload(main_panel)
    importlib.reload(socials)
    importlib.reload(settings_panel)
    importlib.reload(arp_panel)

import bpy

classes = [
    main_panel.CBB_PT_parent_panel,
    arp_panel.CBB_PT_csc_bridge_arp_wrapper,
    settings_panel.CBB_PT_csc_bridge_settings,
    socials.CBB_PT_csc_bridge_info,
    socials.CBB_OT_open_url,
]
