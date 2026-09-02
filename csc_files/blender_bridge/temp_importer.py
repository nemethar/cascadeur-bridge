import csc
import rig_mode.on as rm_on


def name():
    return "Blender Bridge.Temp Importer"


def description():
    return "SHOULD ONLY BE CALLED FROM BLENDER! This imports the temporarily exported file from Blender into the current scene in Cascadeur."


def run(scene):
    from .client_socket import ClientSocket
    from . import commons

    model_viewer = scene.model_viewer()
    objects_before_import = set(model_viewer.get_objects())

    mp = csc.app.get_application()
    scene_pr = mp.get_scene_manager().current_scene()
    tools_manager = csc.app.get_application().get_tools_manager()

    fbx_scene_loader = tools_manager.get_tool("FbxSceneLoader").get_fbx_loader(scene_pr)
    client = None
    try:
        client = ClientSocket()
    except Exception as e:
        scene.error(f"Couldn't connect to Blender. Error: {e}")
        return
    try:
        message: dict = client.receive_message()

        file_path = message.get("file_path")
        settings_dict: dict = message.get("import_settings")
        import_method = getattr(fbx_scene_loader, message.get("import_method"))

        fbx_scene_loader.set_settings(commons.set_fbx_settings(settings_dict))

        import_method(file_path)
        scene.info(f"File imported from {file_path}")
        client.send_message({"status": "completed"})

    except Exception as e:
        scene.error(f"Couldn't import file. Error: {e}")

        try:
            client.send_message(
                {
                    "status": "error",
                    "error_code": "IMPORT_FAILED",
                    "message": str(e),
                }
            )
        except Exception:
            # The connection may have failed while processing the request.
            pass

    finally:
        if client is not None:
            client.close()

    if message.get("import_method") == "import_model":

        behaviour_viewer = model_viewer.behaviour_viewer()

        objects_after_import = set(model_viewer.get_objects())
        imported_objects = objects_after_import.difference(objects_before_import)

        joints = {
            obj
            for obj in imported_objects
            if not behaviour_viewer.get_behaviour_by_name(obj, "Joint").is_null()
        }

        if joints:
            scene.info("Entering rigging mode.")
            rm_on.run(scene_pr.domain_scene(), [0.0, 0.5, 0.0])
        else:
            scene.info("No imported joints. Skipping entering to rigging mode.")
