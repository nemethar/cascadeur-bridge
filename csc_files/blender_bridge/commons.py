import csc
import tempfile
import os


def set_fbx_settings(preferences: dict = {}) -> csc.fbx.FbxSettings:
    """
    Setting the fbx export settings in Cascadeur.

    :param dict preferences: Settings in key value pairs, defaults to {}
    :return csc.fbx.FbxSettings: FbxSettings object
    """
    settings = csc.fbx.FbxSettings()
    settings.mode = csc.fbx.FbxSettingsMode.Binary

    if preferences.get("euler_filter"):
        settings.apply_euler_filter = True
    else:
        settings.apply_euler_filter = False
    if preferences.get("up_axis") == "Z":
        settings.up_axis = csc.fbx.FbxSettingsAxis.Z
    else:
        settings.up_axis = csc.fbx.FbxSettingsAxis.Y
    if not preferences.get("bake_animation"):
        settings.bake_animation = False
    else:
        settings.bake_animation = True
    return settings


def get_export_path(scene_name: str) -> str:
    """
    FBX export path in the temp folder using the scene name.

    :param str scene_name: Name of the Cascadeur scene
    :return str: FBX export path
    """
    temp_dir = tempfile.gettempdir()
    file_name = scene_name.replace(".casc", "") + ".fbx"
    return os.path.join(temp_dir, file_name)


def path_exists(file_path: str) -> bool:
    """
    Checking if file exists.

    :param str file_path: Path of the file.
    :return bool: True if the file exsits otherwise False
    """
    if file_path is None:
        return False
    return os.path.exists(file_path)


def export_fbx(
    app: csc.app.Application, scene: csc.view.Scene, message: dict, export_path: str
):
    """
    Export the scene to an FBX file.

    :param csc.app.Application app: Cascadeur application instance.
    :param csc.view.Scene scene: Cascadeur scene to export.
    :param dict message: Message containing the FBX export settings and method.
    :param str export_path: Path where the FBX file will be exported.
    """
    from . import commons

    settings_dict: dict = message.get("export_settings")

    tools_manager = app.get_tools_manager()
    fbx_scene_loader = tools_manager.get_tool("FbxSceneLoader").get_fbx_loader(scene)
    fbx_scene_loader.set_settings(commons.set_fbx_settings(settings_dict))

    method_name = message.get("export_method", "export_all_objects")
    export_method = getattr(fbx_scene_loader, method_name)
    export_method(export_path)


def import_fbx(
    app: csc.app.Application, scene: csc.view.Scene, message: dict, file_path: str
):
    """
    Import an FBX file into the scene.

    :param csc.app.Application app: Cascadeur application instance.
    :param csc.view.Scene scene: Cascadeur scene to import into.
    :param dict message: Message containing the FBX import settings and method.
    :param str file_path: Path of the FBX file to import.
    """
    from . import commons

    settings_dict: dict = message.get("import_settings")

    tools_manager = app.get_tools_manager()
    fbx_scene_loader = tools_manager.get_tool("FbxSceneLoader").get_fbx_loader(scene)
    import_method = getattr(fbx_scene_loader, message.get("import_method"))

    fbx_scene_loader.set_settings(commons.set_fbx_settings(settings_dict))

    import_method(file_path)


def get_imported_joints(
    model_viewer: csc.model.ModelViewer, objects_before_import: set
):
    """
    Get joints that were imported into the scene.

    :param csc.model.ModelViewer model_viewer: Model viewer to get the scene objects.
    :param set objects_before_import: Set of objects present before the import.
    :return set: Set of joints that were imported.
    """
    objects_after_import = set(model_viewer.get_objects())
    imported_objects = objects_after_import.difference(objects_before_import)

    behaviour_viewer = model_viewer.behaviour_viewer()
    return {
        obj
        for obj in imported_objects
        if not behaviour_viewer.get_behaviour_by_name(obj, "Joint").is_null()
    }
