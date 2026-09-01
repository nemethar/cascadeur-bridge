import csc


def name():
    return "Blender Bridge.Temp Batch Exporter"


def description():
    return "SHOULD ONLY BE CALLED FROM BLENDER! This exports every opened scene which will be imported in Blender."


def run(scene):
    from .client_socket import ClientSocket
    from . import commons

    scene_manager = csc.app.get_application().get_scene_manager()
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

        for s in scenes:
            fbx_scene_loader = (
                csc.app.get_application()
                .get_tools_manager()
                .get_tool("FbxSceneLoader")
                .get_fbx_loader(s)
            )
            export_path = commons.get_export_path(s.name())
            fbx_scene_loader.set_settings(commons.set_fbx_settings(settings_dict))
            export_method = getattr(fbx_scene_loader, method_name)
            export_method(export_path)
            export_paths.append(export_path)
            scene.info(f"File exported to {export_path}")

        client.send_message(
            {
                "status": "success",
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
