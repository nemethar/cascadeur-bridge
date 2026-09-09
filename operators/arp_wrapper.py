import bpy
import os
from .file_transfer import OperatorBaseClass
from ..utils.csc_handling import CascadeurHandler
from ..utils import file_handling, properties_handling


class ARPExportOperatorBase(OperatorBaseClass):
    """
    Base class for CBB operators that use Auto-Rig Pro's
    export operators and then import the exported file into
    Cascadeur.
    """

    arp_quick_export: bpy.props.BoolProperty(
        default=False,
    )

    # Path of the file exported by Auto-Rig Pro.
    arp_export_path: str = ""

    # Prevent starting the Cascadeur command more than once.
    cascadeur_command_called: bool = False

    # ------------------------------------------------------------------
    # Format-specific configuration
    # ------------------------------------------------------------------

    arp_operator: str = ""
    arp_operator_class: str = ""
    file_format: str = ""

    def on_execute(self, context):
        """
        Start Auto-Rig Pro's exporter.

        Subclasses only need to provide the ARP operator and
        file format.
        """

        # Reset internal state.
        self.arp_export_path = ""
        self.cascadeur_command_called = False

        # Clear ARP's previous export path so that a cancelled
        # export cannot accidentally use an old path.
        context.scene.arp_ge_fp = ""

        # Start ARP's exporter.
        result = getattr(bpy.ops.arp, self.arp_operator)(
            "INVOKE_DEFAULT",
            quick_export=self.arp_quick_export,
        )

        # Quick export runs synchronously inside ARP.
        if self.arp_quick_export:
            self._get_export_path()

            # Quick export should have produced the file already.
            self._validate_export_file()

            return

        # Normal export opens ARP's file browser and continues
        # asynchronously.
        if "CANCELLED" in result:
            raise RuntimeError(
                f"Auto-Rig Pro {self.file_format.upper()} export was cancelled."
            )

    def on_timer(self, context):
        """
        Wait for Auto-Rig Pro to finish exporting, then start
        Cascadeur's temporary importer.
        """

        # Quick export has already completed.
        if self.arp_quick_export:
            self._start_cascadeur()
            return {"RUNNING_MODAL"}

        # Check whether ARP's exporter is still running.
        arp_operator_running = any(
            operator.bl_idname == self.arp_operator_class
            for operator in context.window_manager.operators
        )

        if arp_operator_running:
            return {"RUNNING_MODAL"}

        # ARP has finished. Get the path it exported to.
        export_path = getattr(
            context.scene,
            "arp_ge_fp",
            "",
        )

        # No path means the user cancelled the file browser.
        if not export_path:
            self.report(
                {"WARNING"},
                f"Auto-Rig Pro {self.file_format.upper()} export was cancelled.",
            )
            return {"CANCELLED"}

        self.arp_export_path = export_path

        # Make sure ARP actually created the file.
        if not os.path.isfile(self.arp_export_path):
            self.report(
                {"ERROR"},
                f"Auto-Rig Pro did not create the {self.file_format.upper()} file.",
            )
            return {"CANCELLED"}

        # Start Cascadeur exactly once.
        self._start_cascadeur()

        return {"RUNNING_MODAL"}

    def _get_export_path(self):
        """Get and validate the path produced by ARP."""

        self.arp_export_path = getattr(
            bpy.context.scene,
            "arp_ge_fp",
            "",
        )

        if not self.arp_export_path:
            raise RuntimeError(
                f"Auto-Rig Pro did not provide a {self.file_format.upper()} export path."
            )

    def _validate_export_file(self):
        """Make sure ARP created the exported file."""

        if not os.path.isfile(self.arp_export_path):
            raise RuntimeError(
                f"Auto-Rig Pro did not create the expected "
                f"{self.file_format.upper()} file."
            )

    def _start_cascadeur(self):
        """Start Cascadeur's temporary importer exactly once."""

        if self.cascadeur_command_called:
            return

        CascadeurHandler().execute_csc_command("scripts.blender_bridge.temp_importer")

        self.cascadeur_command_called = True

    def on_connected(self, context):
        """
        Send the exported file to Cascadeur and wait for the
        import result.
        """

        import_settings = self.get_import_settings(context)

        self.server_socket.send_message(
            {
                "file_format": self.file_format,
                "file_path": self.arp_export_path,
                "import_method": self.get_import_method(context),
                "import_settings": import_settings,
            }
        )

        response = self.server_socket.receive_message()

        if response.get("status") != "completed":
            error_code = response.get("error_code")
            error_message = response.get(
                "message",
                "No error message.",
            )

            if error_code == "IMPORT_FAILED":
                self.report(
                    {"ERROR"},
                    f"Import failed: {error_message}",
                )
            else:
                self.report(
                    {"ERROR"},
                    f"Operation failed: {error_message}",
                )

            self.cleanup(context)
            return {"CANCELLED"}

        addon_props = context.scene.cbb_settings

        if addon_props.blender_to_cascadeur.cbb_delete_arp_export:
            # Delete the temporary exported file.
            file_handling.delete_file(self.arp_export_path)

        self.report({"INFO"}, "Finished")
        return {"FINISHED"}

    def get_import_method(self, context):
        """Override when the format supports an import method."""
        return None

    def get_import_settings(self, context):
        """Override in subclasses."""
        raise NotImplementedError


class CBB_OT_export_arp_fbx(ARPExportOperatorBase):
    """
    Export the character using Auto-Rig Pro's FBX exporter
    and then import the resulting FBX into Cascadeur.
    """

    bl_idname = "cbb.export_arp_fbx"
    bl_label = "Export ARP FBX"

    arp_operator = "arp_export_fbx_panel"
    arp_operator_class = "ARP_OT_GE_export_fbx_panel"
    file_format = "fbx"

    def get_import_method(self, context):
        return context.scene.cbb_settings.cascadeur_fbx_import.cbb_import_methods

    def get_import_settings(self, context):
        return properties_handling.get_csc_fbx_settings("import")


class CBB_OT_export_arp_glb(ARPExportOperatorBase):
    """
    Export the character using Auto-Rig Pro's GLTF/GLB exporter
    and then import the resulting GLB into Cascadeur.
    """

    bl_idname = "cbb.export_arp_glb"
    bl_label = "Export ARP GLB"

    arp_operator = "arp_export_gltf_panel"
    arp_operator_class = "ARP_OT_GE_export_gltf_panel"
    file_format = "glb"

    def get_import_settings(self, context):
        return properties_handling.get_csc_glb_settings("import")
