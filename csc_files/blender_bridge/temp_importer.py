import csc


def name():
    return "Blender Bridge.Temp Importer"


def description():
    return "SHOULD ONLY BE CALLED FROM BLENDER! This imports the temporarily exported file from Blender into the current scene in Cascadeur."


def run(scene):
    from .client_socket import ClientSocket

    mp = csc.app.get_application()
    scene_pr = mp.get_scene_manager().current_scene()
    fbx_scene_loader = (
        csc.app.get_application()
        .get_tools_manager()
        .get_tool("FbxSceneLoader")
        .get_fbx_loader(scene_pr)
    )
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
