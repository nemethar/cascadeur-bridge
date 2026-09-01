import csc


def name():
    return "Blender Bridge.Temp Batch Exporter"


def description():
    return "SHOULD ONLY BE CALLED FROM BLENDER! This exports every opened scene which will be imported in Blender."


def run(scene):
    from .client_socket import ClientSocket
    from . import commons

    app = csc.app.get_application()
    scene_manager = app.get_scene_manager()
    scenes = scene_manager.scenes()
    client = None
    try:
        client = ClientSocket()
    except Exception as e:
        scene.error(f"Couldn't connect to Blender. Error: {e}")
        return
    try:
        message: dict = client.receive_message()
        settings_dict: dict = message.get("export_settings")
        method_name = message.get("export_method", "export_all_objects")
        export_paths = []

        if not app.is_export_available():
            client.send_message(
                {
                    "status": "error",
                    "error_code": "LICENSE_REQUIRED",
                    "message": "Export is not available with the current license.",
                }
            )

        for s in scenes:
            fbx_scene_loader = (
                app.get_tools_manager().get_tool("FbxSceneLoader").get_fbx_loader(s)
            )
            export_path = commons.get_export_path(s.name())
            fbx_scene_loader.set_settings(commons.set_fbx_settings(settings_dict))
            export_method = getattr(fbx_scene_loader, method_name)
            export_method(export_path)
            if not commons.path_exists(export_path):
                raise FileNotFoundError(
                    f"Export file was not created. Check Cascadeur event logs for more info!"
                )
            export_paths.append(export_path)
            scene.info(f"File exported to {export_path}")

        client.send_message(
            {
                "status": "completed",
                "files": export_paths,
            }
        )
    except Exception as e:
        scene.error(f"Couldn't export file. Error: {e}")

        try:
            client.send_message(
                {
                    "status": "error",
                    "error_code": "EXPORT_FAILED",
                    "message": str(e),
                }
            )
        except Exception:
            # The connection may have been lost while processing the request.
            pass

    finally:
        if client is not None:
            client.close()
