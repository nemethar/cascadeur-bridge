import bpy

from .addon_properties import get_csc_export_settings
from ..utils import file_handling, action_handling
from ..utils.server_socket import ServerSocket
from ..utils.csc_handling import CascadeurHandler
from .. import addon_info

import os


def import_fbx(file_path: str) -> list:
    """
    Importing the provided file with the fbx import settings set on the N panel.

    :param str file_path: FBX file path to be imported
    :return list: List of selected objects in the scene
    """
    addon_props = bpy.context.scene.cbb_fbx_settings
    bpy.ops.import_scene.fbx(
        filepath=file_path,
        # Transform
        global_scale=addon_props.cbb_import_global_scale,
        bake_space_transform=addon_props.cbb_import_apply_transform,
        use_manual_orientation=addon_props.cbb_import_manual_orientation,
        axis_forward=addon_props.cbb_import_axis_forward,
        axis_up=addon_props.cbb_import_axis_up,
        # Animation
        use_anim=addon_props.cbb_import_use_anim,
        anim_offset=addon_props.cbb_import_anim_offset,
        # Armature
        ignore_leaf_bones=addon_props.cbb_import_ignore_leaf_bones,
        force_connect_children=addon_props.cbb_import_force_connect_children,
        automatic_bone_orientation=addon_props.cbb_import_automatic_bone_orientation,
        primary_bone_axis=addon_props.cbb_import_primary_bone_axis,
        secondary_bone_axis=addon_props.cbb_import_secondary_bone_axis,
        use_prepost_rot=addon_props.cbb_import_use_prepost_rot,
    )
    # Return the list of imported objects
    return bpy.context.selected_objects


def export_fbx(file_path: str) -> None:
    """
    Exporting fbx from Blender to the provided path using the settings
    set on the N panel.

    :param str file_path: Path of the fbx file.
    """
    addon_props = bpy.context.scene.cbb_fbx_settings
    bpy.ops.export_scene.fbx(
        filepath=file_path,
        # Include
        use_selection=addon_props.cbb_export_use_selection,
        object_types=addon_props.cbb_export_object_types,
        # Transform
        global_scale=addon_props.cbb_export_global_scale,
        axis_forward=addon_props.cbb_export_axis_forward,
        axis_up=addon_props.cbb_export_axis_up,
        bake_space_transform=addon_props.cbb_export_apply_transform,
        # Armature
        primary_bone_axis=addon_props.cbb_export_primary_bone_axis,
        secondary_bone_axis=addon_props.cbb_export_secondary_bone_axis,
        use_armature_deform_only=addon_props.cbb_export_deform_only,
        add_leaf_bones=addon_props.cbb_export_leaf_bones,
        # Animation
        bake_anim=addon_props.cbb_export_bake_anim,
        bake_anim_use_nla_strips=addon_props.cbb_export_use_nla_strips,
        bake_anim_use_all_actions=addon_props.cbb_export_use_all_actions,
    )


def delete_objects(objects: list) -> None:
    """
    Delete the provided list of objects.

    :param list objects: List of objects
    """
    # Create a copy of the objects list
    objects_copy = objects.copy()

    for obj in objects_copy:
        # Check if the object exists in Blender's data before attempting to remove it
        obj_in_data = bpy.data.objects.get(obj.name)
        if obj_in_data:
            bpy.data.objects.remove(obj, do_unlink=True)
            # Remove the object from the original list to avoid reprocessing
            objects.remove(obj)

    # Update the scene to reflect the changes
    bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)


class OperatorBaseClass(bpy.types.Operator):
    """
    Base class for all operators that communicate with Cascadeur.

    Lifecycle:
        execute()
            -> start_operator()
            -> on_execute()            # Starts the Cascadeur side.
            -> modal()                 # Waits for Cascadeur to connect.
                -> on_connected()      # Exchange data once connected.
                -> cleanup()

    Subclasses only need to implement:
        on_execute()      - Trigger the Cascadeur command.
        on_connected()    - Handle socket communication.
    """
    server_socket = None
    _timer = None

    def start_operator(self):
        # Used by the UI to display in progress text
        addon_info.operation_completed = False

        try:
            # Open the socket and start listening for Cascadeur
            self.server_socket = ServerSocket()
        except Exception as e:
            self.report({"ERROR"}, str(e))
            addon_info.operation_completed = True
            return {"CANCELLED"}

    def execute(self, context):
        # Create the listening socket
        result = self.start_operator()
        if result:
            return result

        # Let the subclass start the corresponding Cascadeur command
        self.on_execute(context)

        # Poll the socket from Blender's modal timer until Cascadeur connects
        self._timer = context.window_manager.event_timer_add(
            0.05,
            window=context.window,
        )
        context.window_manager.modal_handler_add(self)

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        try:

            # Allow the user to abort the operation
            if event.type == "ESC":
                self.cleanup(context)
                return {"CANCELLED"}

            # Ignore everything except timer events
            if event.type != "TIMER":
                return {"PASS_THROUGH"}

            # Accept incoming socket connections
            self.server_socket.run()

            # Keep waiting until Cascadeur connects
            if not self.server_socket.client_socket:
                return {"RUNNING_MODAL"}

            # Once connected, let the subclass perform its communication
            status = self.on_connected(context)

            # Any state other than RUNNING_MODAL means we're finished
            if status != {"RUNNING_MODAL"}:
                self.cleanup(context)

            return status

        except Exception as e:
            self.report({"ERROR"}, str(e))
            self.cleanup(context)
            return {"CANCELLED"}

    def on_execute(self, context):
        """
        Called once before entering modal mode.

        Subclasses should launch the corresponding Cascadeur command here.
        """
        raise NotImplementedError

    def on_connected(self, context):
        """
        Called once Cascadeur has connected to the socket.

        Perform all socket communication here.
        """
        raise NotImplementedError

    def cleanup(self, context):
        """Release all resources used by the modal operator."""
        addon_info.operation_completed = True
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None

        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None


class CBB_OT_export_blender_fbx(OperatorBaseClass):
    """Exports the selected objects and imports them to Cascadeur"""

    bl_idname = "cbb.export_blender_fbx"
    bl_label = "Export to Cascadeur"

    def on_execute(self, context):
        # Export the selected objects to a temporary FBX.
        self.file_path = file_handling.get_export_path()
        export_fbx(self.file_path)

        # Ask Cascadeur to start its importer. It will connect back to Blender.
        CascadeurHandler().execute_csc_command("commands.blender_bridge.temp_importer")

    def on_connected(self, context):
        # Tell Cascadeur where the temporary FBX is located.
        self.server_socket.send_message(
            {
                "file_path": self.file_path,
                "import_method": bpy.context.scene.cbb_fbx_settings.cbb_import_methods,
            }
        )

        response = self.server_socket.receive_message()

        if response != "SUCCESS":
            self.cleanup(context)
            return {"CANCELLED"}

        # Delete exported file
        file_handling.delete_file(self.file_path)
        self.report({"INFO"}, "Finished")
        return {"FINISHED"}


class CBB_OT_import_cascadeur_fbx(OperatorBaseClass):
    """Imports the currently opened Cascadeur scene"""

    bl_idname = "cbb.import_cascadeur_fbx"
    bl_label = "Import Cascadeur Scene"

    batch_export: bpy.props.BoolProperty(
        name="Import all scene",
        description="",
        default=False,
    )

    def on_execute(self, context):
        # Ask Cascadeur to export the current scene (or every scene)
        command = "temp_batch_exporter" if self.batch_export else "temp_exporter"

        CascadeurHandler().execute_csc_command(f"commands.blender_bridge.{command}")

    def on_connected(self, context):
        # Send Blender's export settings to Cascadeur
        self.server_socket.send_message(get_csc_export_settings())

        # Expect a list of temporary FBX files
        data = self.server_socket.receive_message()

        if not isinstance(data, list):
            self.report({"ERROR"}, f"Unexpected response: {data}")
            return {"CANCELLED"}

        for file in data:
            import_fbx(file)
            file_handling.delete_file(file)

        self.cleanup(context)
        self.report({"INFO"}, "Finished")
        return {"FINISHED"}


class CBB_OT_import_action_to_selected(OperatorBaseClass):
    """Imports the action from Cascadeur and apply to selected armature"""

    bl_idname = "cbb.import_cascadeur_action"
    bl_label = "Import Cascadeur Action"

    ao = None
    selected_objects = []
    imported_objects = []

    batch_export: bpy.props.BoolProperty(
        name="Import all scene",
        description="",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        selected = context.selected_objects
        return bool(selected) and any(obj.type == "ARMATURE" for obj in selected)

    def on_execute(self, context):
        # Store the current selection because importing FBXs changes it
        self.ao = context.active_object
        self.selected_objects = context.selected_objects.copy()
        self.imported_objects = []

        command = "temp_batch_exporter" if self.batch_export else "temp_exporter"

        CascadeurHandler().execute_csc_command(f"commands.blender_bridge.{command}")

    def on_connected(self, context):
        self.server_socket.send_message(get_csc_export_settings())

        data = self.server_socket.receive_message()

        if not isinstance(data, list):
            self.cleanup(context)
            self.report({"ERROR"}, f"Unexpected response: {data}")
            return {"CANCELLED"}

        for file in data:
            # Import the temporary FBX to extract its actions
            objects = import_fbx(file)
            self.imported_objects.extend(objects)

            # Use the FBX filename as the name of the action
            scene_name = os.path.splitext(os.path.basename(file))[0]

            file_handling.delete_file(file)

            actions = action_handling.get_imported_actions(objects)

            selected_armatures = [
                obj for obj in self.selected_objects if obj.type == "ARMATURE"
            ]

            # Copy the imported actions onto the user's selected armatures
            action_handling.apply_action(
                selected_armatures,
                actions,
                scene_name,
            )

        delete_objects(self.imported_objects)

        # Restore the user's original selection
        bpy.ops.object.select_all(action="DESELECT")

        for obj in self.selected_objects:
            obj.select_set(True)

        context.view_layer.objects.active = self.ao

        self.report({"INFO"}, "Finished")
        return {"FINISHED"}
