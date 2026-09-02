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

    app = csc.app.get_application()
    scene_pr = app.get_scene_manager().current_scene()

    client = None
    try:
        client = ClientSocket()
    except Exception as e:
        scene.error(f"Couldn't connect to Blender. Error: {e}")
        return
    try:
        message: dict = client.receive_message()

        file_path = message.get("file_path")
        file_format = message.get("file_format", "fbx")

        if file_format == "fbx":
            commons.import_fbx(app, scene_pr, message, file_path)
        else:
            pass

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

        imported_joints = commons.get_imported_joints(
            model_viewer, objects_before_import
        )

        if imported_joints:
            scene.info("Entering rigging mode.")
            rm_on.run(scene_pr.domain_scene(), [0.0, 0.5, 0.0])
        else:
            scene.info("No imported joints. Skipping entering to rigging mode.")
