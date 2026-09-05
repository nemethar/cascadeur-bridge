import csc


def name():
    return "Blender Bridge.Temp Exporter"


def description():
    return "SHOULD ONLY BE CALLED FROM BLENDER! This exports the current scene which will be imported in Blender."


def run(scene):
    from .client_socket import ClientSocket
    from . import commons

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

        if not app.is_export_available():
            client.send_message(
                {
                    "status": "error",
                    "error_code": "LICENSE_REQUIRED",
                    "message": "Export is not available with the current license.",
                }
            )
            return

        export_path = commons.get_export_path(scene_pr.name())
        file_format = message.get("file_format", "fbx")

        if file_format == "fbx":
            commons.export_fbx(app, scene_pr, message, export_path)
        else:
            commons.export_glb(scene_pr, message, export_path)

        if not commons.path_exists(export_path):
            raise FileNotFoundError(
                f"Export file was not created. Check Cascadeur event logs for more info!"
            )
        scene.info(f"File exported to {export_path}")
        client.send_message(
            {
                "status": "completed",
                "files": [export_path],
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
