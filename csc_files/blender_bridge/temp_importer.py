import csc
import rig_mode.on as rm_on


def name():
    return "Blender Bridge.Temp Importer"


def description():
    return "SHOULD ONLY BE CALLED FROM BLENDER! This imports the temporarily exported file from Blender into the current scene in Cascadeur."


def run(scene):
    from .client_socket import ClientSocket

    mp = csc.app.get_application()
    scene_pr = mp.get_scene_manager().current_scene()
    tools_manager = csc.app.get_application().get_tools_manager()

    fbx_scene_loader = tools_manager.get_tool("FbxSceneLoader").get_fbx_loader(scene_pr)
    client = None
    try:
        client = ClientSocket()
        message: dict = client.receive_message()
        file_path = message.get("file_path")

        import_method = getattr(fbx_scene_loader, message.get("import_method"))
        import_method(file_path)
        scene.info(f"File imported from {file_path}")
        client.send_message("SUCCESS")

    except Exception as e:
        scene.error(f"Couldn't create socket. Error: {e}")
        return
    finally:
        if client is not None:
            client.close()

    if message.get("import_method") == "import_model":
        model_viewer = scene.model_viewer()
        behaviour_viewer = model_viewer.behaviour_viewer()
        objects = model_viewer.get_objects()
        joints = {
            obj
            for obj in objects
            if not behaviour_viewer.get_behaviour_by_name(obj, "Joint").is_null()
        }

        if joints:
            scene.info("Entering rigging mode.")
            rm_on.run_raw(scene_pr.domain_scene(), [0.0, 0.5, 0.0])
            rig_tool = tools_manager.get_tool("RiggingToolWindowTool").editor(scene_pr)
            rig_tool.open_quick_rigging_tool()
        else:
            scene.warning("Cannot enter rigging mode. No joints in the scene.")
