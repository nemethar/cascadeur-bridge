import bpy

from ..utils import file_handling, action_handling, properties_handling
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
    import_props = bpy.context.scene.cbb_settings.blender_fbx_import
    bpy.ops.import_scene.fbx(
        filepath=file_path,
        # Include
        use_custom_normals=import_props.cbb_use_custom_normals,
        use_subsurf=import_props.cbb_use_subsurf,
        use_custom_props=import_props.cbb_use_custom_props,
        use_custom_props_enum_as_string=import_props.cbb_use_custom_props_enum_as_string,
        use_image_search=import_props.cbb_use_image_search,
        colors_type=import_props.cbb_colors_type,
        # Transform
        global_scale=import_props.cbb_global_scale,
        decal_offset=import_props.cbb_decal_offset,
        bake_space_transform=import_props.cbb_bake_space_transform,
        use_prepost_rot=import_props.cbb_use_prepost_rot,
        use_manual_orientation=import_props.cbb_use_manual_orientation,
        axis_forward=import_props.cbb_axis_forward,
        axis_up=import_props.cbb_axis_up,
        # Materials
        mtl_name_collision_mode=import_props.cbb_mtl_name_collision_mode,
        # Animation
        use_anim=import_props.cbb_use_anim,
        anim_offset=import_props.cbb_anim_offset,
        # Armature
        ignore_leaf_bones=import_props.cbb_ignore_leaf_bones,
        force_connect_children=import_props.cbb_force_connect_children,
        automatic_bone_orientation=import_props.cbb_automatic_bone_orientation,
        primary_bone_axis=import_props.cbb_primary_bone_axis,
        secondary_bone_axis=import_props.cbb_secondary_bone_axis,
    )
    # Return the list of imported objects
    return bpy.context.selected_objects


def export_fbx(file_path: str) -> None:
    """
    Exporting fbx from Blender to the provided path using the settings
    set on the N panel.

    :param str file_path: Path of the fbx file.
    """
    export_props = bpy.context.scene.cbb_settings.blender_fbx_export
    bpy.ops.export_scene.fbx(
        filepath=file_path,
        # Path mode
        path_mode=export_props.cbb_path_mode,
        embed_textures=export_props.cbb_embed_textures,
        # Include
        use_selection=export_props.cbb_use_selection,
        use_visible=export_props.cbb_use_visible,
        use_active_collection=export_props.cbb_use_active_collection,
        object_types=export_props.cbb_object_types,
        use_custom_props=export_props.cbb_use_custom_props,
        # Transform
        global_scale=export_props.cbb_global_scale,
        apply_scale_options=export_props.cbb_apply_scale_options,
        axis_forward=export_props.cbb_axis_forward,
        axis_up=export_props.cbb_axis_up,
        apply_unit_scale=export_props.cbb_apply_unit_scale,
        use_space_transform=export_props.cbb_use_space_transform,
        bake_space_transform=export_props.cbb_apply_transform,
        # Geometry
        mesh_smooth_type=export_props.cbb_mesh_smooth_type,
        use_subsurf=export_props.cbb_use_subsurf,
        use_mesh_modifiers=export_props.cbb_use_mesh_modifiers,
        use_mesh_edges=export_props.cbb_use_mesh_edges,
        use_triangles=export_props.cbb_use_triangles,
        use_tspace=export_props.cbb_use_tspace,
        colors_type=export_props.cbb_colors_type,
        prioritize_active_color=export_props.cbb_prioritize_active_color,
        # Armature
        primary_bone_axis=export_props.cbb_primary_bone_axis,
        secondary_bone_axis=export_props.cbb_secondary_bone_axis,
        armature_nodetype=export_props.cbb_armature_nodetype,
        use_armature_deform_only=export_props.cbb_deform_only,
        add_leaf_bones=export_props.cbb_leaf_bones,
        # Animation
        bake_anim=export_props.cbb_bake_anim,
        bake_anim_use_all_bones=export_props.cbb_bake_anim_use_all_bones,
        bake_anim_use_nla_strips=export_props.cbb_use_nla_strips,
        bake_anim_use_all_actions=export_props.cbb_use_all_actions,
        bake_anim_force_startend_keying=export_props.cbb_bake_anim_force_startend_keying,
        bake_anim_step=export_props.cbb_bake_anim_step,
        bake_anim_simplify_factor=export_props.cbb_bake_anim_simplify_factor,
    )


def import_glb(file_path: str) -> list:
    """
    Import the provided GLB/GLTF file using the GLB import settings
    configured in the N panel.

    :param str file_path: GLB/GLTF file path to be imported
    :return list: List of selected objects in the scene
    """
    import_props = bpy.context.scene.cbb_settings.blender_glb_import

    bpy.ops.import_scene.gltf(
        filepath=file_path,
        # Lighting
        export_import_convert_lighting_mode=import_props.cbb_convert_lighting_mode,
        # Mesh
        merge_vertices=import_props.cbb_merge_vertices,
        import_shading=import_props.cbb_import_shading,
        import_merge_material_slots=import_props.cbb_import_merge_material_slots,
        import_point_as_pointcloud=import_props.cbb_import_point_as_pointcloud,
        # Texture
        import_pack_images=import_props.cbb_import_pack_images,
        import_webp_texture=import_props.cbb_import_webp_texture,
        import_unused_materials=import_props.cbb_import_unused_materials,
        # Bones & Skin
        bone_heuristic=import_props.cbb_bone_heuristic,
        guess_original_bind_pose=import_props.cbb_guess_original_bind_pose,
        disable_bone_shape=import_props.cbb_disable_bone_shape,
        bone_shape_scale_factor=import_props.cbb_bone_shape_scale_factor,
        # Pipeline
        import_scene_as_collection=import_props.cbb_import_scene_as_collection,
        import_select_created_objects=import_props.cbb_import_select_created_objects,
        import_scene_extras=import_props.cbb_import_scene_extras,
    )

    return bpy.context.selected_objects


def export_glb(file_path: str) -> None:
    """
    Exporting GLB from Blender to the provided path using the settings
    set on the N panel.

    :param str file_path: Path of the GLB file.
    """
    export_props = bpy.context.scene.cbb_settings.blender_glb_export

    bpy.ops.export_scene.gltf(
        filepath=file_path,
        # Include
        use_selection=export_props.cbb_selection,
        use_visible=export_props.cbb_visible,
        use_renderable=export_props.cbb_renderable,
        use_active_collection=export_props.cbb_active_collection,
        use_active_collection_with_nested=export_props.cbb_active_collection_with_nested,
        use_active_scene=export_props.cbb_active_scene,
        export_cameras=export_props.cbb_cameras,
        export_lights=export_props.cbb_lights,
        export_extras=export_props.cbb_extras,
        # Transform
        export_yup=export_props.cbb_yup,
        # Data - Scene Graph
        export_hierarchy_flatten_objs=export_props.cbb_hierarchy_flatten_objs,
        export_hierarchy_full_collections=export_props.cbb_hierarchy_full_collections,
        # Data - Mesh
        export_apply=export_props.cbb_apply,
        export_texcoords=export_props.cbb_texcoords,
        export_normals=export_props.cbb_normals,
        export_tangents=export_props.cbb_tangents,
        export_attributes=export_props.cbb_attributes,
        use_mesh_edges=export_props.cbb_mesh_edges,
        use_mesh_vertices=export_props.cbb_mesh_vertices,
        export_shared_accessors=export_props.cbb_shared_accessors,
        # Data - Vertex Colors
        export_vertex_color=export_props.cbb_vertex_color,
        export_vertex_color_name=export_props.cbb_vertex_color_name,
        export_all_vertex_colors=export_props.cbb_all_vertex_colors,
        export_active_vertex_color_when_no_material=(
            export_props.cbb_active_vertex_color_when_no_material
        ),
        # Data - Materials
        export_materials=export_props.cbb_materials,
        export_image_format=export_props.cbb_image_format,
        export_image_quality=export_props.cbb_image_quality,
        export_image_add_webp=export_props.cbb_image_add_webp,
        export_image_webp_fallback=export_props.cbb_image_webp_fallback,
        export_unused_images=export_props.cbb_unused_images,
        export_unused_textures=export_props.cbb_unused_textures,
        # Data - Shape Keys
        export_morph=export_props.cbb_morph,
        export_morph_normal=export_props.cbb_morph_normal,
        export_morph_tangent=export_props.cbb_morph_tangent,
        # Data - Armature
        export_rest_position_armature=export_props.cbb_rest_position_armature,
        export_def_bones=export_props.cbb_def_bones,
        export_armature_object_remove=export_props.cbb_armature_object_remove,
        export_hierarchy_flatten_bones=export_props.cbb_hierarchy_flatten_bones,
        export_leaf_bone=export_props.cbb_leaf_bone,
        # Data - Skinning
        export_skins=export_props.cbb_skins,
        export_influence_nb=export_props.cbb_influence_nb,
        export_all_influences=export_props.cbb_all_influences,
        # Lighting
        export_import_convert_lighting_mode=export_props.cbb_convert_lighting_mode,
        # Compression - Draco
        export_draco_mesh_compression_enable=(
            export_props.cbb_draco_mesh_compression_enable
        ),
        export_draco_mesh_compression_level=(
            export_props.cbb_draco_mesh_compression_level
        ),
        export_draco_position_quantization=(
            export_props.cbb_draco_position_quantization
        ),
        export_draco_normal_quantization=(export_props.cbb_draco_normal_quantization),
        export_draco_texcoord_quantization=(
            export_props.cbb_draco_texcoord_quantization
        ),
        export_draco_color_quantization=(export_props.cbb_draco_color_quantization),
        export_draco_generic_quantization=(export_props.cbb_draco_generic_quantization),
        # Compression - Meshopt
        export_meshopt_compression_enable=(export_props.cbb_meshopt_compression_enable),
        export_meshopt_extension=export_props.cbb_meshopt_extension,
        # Animation
        export_animations=export_props.cbb_animations,
        export_animation_mode=export_props.cbb_animation_mode,
        # Animation - Bake & Merge
        export_bake_animation=export_props.cbb_bake_animation,
        export_merge_animation=export_props.cbb_merge_animation,
        # Animation - Rest & Ranges
        export_current_frame=export_props.cbb_current_frame,
        export_frame_range=export_props.cbb_frame_range,
        export_anim_slide_to_zero=export_props.cbb_anim_slide_to_zero,
        export_negative_frame=export_props.cbb_negative_frame,
        # Animation - Armature
        export_anim_single_armature=export_props.cbb_anim_single_armature,
        export_reset_pose_bones=export_props.cbb_reset_pose_bones,
        # Animation - Shape Keys
        export_morph_animation=export_props.cbb_morph_animation,
        export_morph_reset_sk_data=export_props.cbb_morph_reset_sk_data,
        # Animation - Sampling
        export_force_sampling=export_props.cbb_force_sampling,
        export_frame_step=export_props.cbb_frame_step,
        export_sampling_interpolation_fallback=(
            export_props.cbb_sampling_interpolation_fallback
        ),
        # Animation - Optimization
        export_optimize_animation_size=(export_props.cbb_optimize_animation_size),
        export_optimize_animation_keep_anim_armature=(
            export_props.cbb_optimize_animation_keep_anim_armature
        ),
        export_optimize_animation_keep_anim_object=(
            export_props.cbb_optimize_animation_keep_anim_object
        ),
        export_optimize_disable_viewport=(export_props.cbb_optimize_disable_viewport),
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

        for area in context.screen.areas:
            area.tag_redraw()


class CBB_OT_export_blender_fbx(OperatorBaseClass):
    """Exports the current blender and imports them to Cascadeur"""

    bl_idname = "cbb.export_blender_fbx"
    bl_label = "Export to Cascadeur"

    def on_execute(self, context):
        self.file_format = (
            context.scene.cbb_settings.blender_to_cascadeur.cbb_file_format
        )
        # Export the selected objects to a temporary FBX/GLB.
        self.file_path = file_handling.get_export_path(self.file_format)

        if self.file_format == "fbx":
            export_fbx(self.file_path)
        else:
            export_glb(self.file_path)

        # Ask Cascadeur to start its importer. It will connect back to Blender.
        CascadeurHandler().execute_csc_command("scripts.blender_bridge.temp_importer")

    def on_connected(self, context):
        if self.file_format == "fbx":
            import_method = (
                context.scene.cbb_settings.cascadeur_fbx_import.cbb_import_methods
            )
            import_settings = properties_handling.get_csc_fbx_settings("import")
        else:
            import_method = None
            import_settings = properties_handling.get_csc_glb_settings("import")

        # Tell Cascadeur where the temporary file is located.
        self.server_socket.send_message(
            {
                "file_format": self.file_format,
                "file_path": self.file_path,
                "import_method": import_method,
                "import_settings": import_settings,
            }
        )

        response = self.server_socket.receive_message()

        if response.get("status") != "completed":
            error_code = response.get("error_code")
            error_message = response.get("message", "No error message.")

            if error_code == "IMPORT_FAILED":
                self.report({"ERROR"}, f"Import failed: {error_message}")
            else:
                self.report({"ERROR"}, f"Operation failed: {error_message}")
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

        CascadeurHandler().execute_csc_command(f"scripts.blender_bridge.{command}")

    def on_connected(self, context):
        file_format = context.scene.cbb_settings.cascadeur_to_blender.cbb_file_format

        if file_format == "fbx":
            export_method = (
                context.scene.cbb_settings.cascadeur_fbx_export.cbb_export_methods
            )
            export_settings = properties_handling.get_csc_fbx_settings("export")
        else:
            export_method = None
            export_settings = properties_handling.get_csc_glb_settings("export")

        # Send Blender's export settings to Cascadeur
        self.server_socket.send_message(
            {
                "file_format": file_format,
                "file_path": None,
                "export_method": export_method,
                "export_settings": export_settings,
            }
        )

        # Expect a list of temporary FBX files
        response = self.server_socket.receive_message()

        if not isinstance(response, dict):
            self.report({"ERROR"}, f"Unexpected response from Cascadeur: {response}")
            self.cleanup(context)
            return {"CANCELLED"}

        if response.get("error_code") == "LICENSE_REQUIRED":
            bpy.ops.cbb.license_required_popup("INVOKE_DEFAULT")
            self.cleanup(context)
            return {"CANCELLED"}

        if response.get("status") != "completed":
            error = get_cascadeur_error(response)
            if error is not None:
                self.report({"ERROR"}, error)
                self.cleanup(context)
                return {"CANCELLED"}

        files = response.get("files", [])
        for file in files:
            if file_format == "fbx":
                import_fbx(file)
            else:
                import_glb(file)
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

        CascadeurHandler().execute_csc_command(f"scripts.blender_bridge.{command}")

    def on_connected(self, context):
        file_format = context.scene.cbb_settings.cascadeur_to_blender.cbb_file_format

        if file_format == "fbx":
            export_method = (
                context.scene.cbb_settings.cascadeur_fbx_export.cbb_export_methods
            )
            export_settings = properties_handling.get_csc_fbx_settings("export")
        else:
            export_method = None
            export_settings = properties_handling.get_csc_glb_settings("export")

        # Send Blender's export settings to Cascadeur
        self.server_socket.send_message(
            {
                "file_format": file_format,
                "file_path": None,
                "export_method": export_method,
                "export_settings": export_settings,
            }
        )

        response = self.server_socket.receive_message()
        print(response)

        if not isinstance(response, dict):
            self.report({"ERROR"}, f"Unexpected response from Cascadeur: {response}")
            self.cleanup(context)
            return {"CANCELLED"}

        status = response.get("status")

        if response.get("error_code") == "LICENSE_REQUIRED":
            bpy.ops.cbb.license_required_popup("INVOKE_DEFAULT")
            self.cleanup(context)
            return {"CANCELLED"}

        elif status != "COMPLETED":
            error = get_cascadeur_error(response)
            if error is not None:
                self.report({"ERROR"}, error)
                self.cleanup(context)
                return {"CANCELLED"}

        files = response.get("files", [])

        for file in files:
            # Import the temporary FBX to extract its actions
            if file_format == "fbx":
                objects = import_fbx(file)
            else:
                objects = import_glb(file)
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


def get_cascadeur_error(response: dict) -> str | None:
    if not isinstance(response, dict):
        return f"Unexpected response from Cascadeur: {response}"

    if response.get("status") == "completed":
        return None

    error_code = response.get("error_code")
    error_message = response.get("message", "No error message.")

    if error_code == "LICENSE_REQUIRED":
        return "A Indie/Pro Cascadeur license is required for export."
    elif error_code == "PATH_NOT_WRITABLE":
        return f"Export path is not writable: {error_message}"
    elif error_code == "EXPORT_FAILED":
        return f"Export failed: {error_message}"

    return f"Cascadeur export failed: {error_message}"
