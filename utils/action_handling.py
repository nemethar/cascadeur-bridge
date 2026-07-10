from dataclasses import dataclass

import bpy


@dataclass
class ActionData:
    action: bpy.types.Action
    action_slot: bpy.types.ActionSlot
    armature_name: str


def get_imported_actions(
    selected_objects: list[bpy.types.Object],
) -> list[ActionData]:
    """
    Get the action data from all selected armatures.

    Non-armature objects may receive temporary actions during FBX import.
    Those actions are removed.

    :param list selected_objects: List of selected Blender objects.
    :return list[ActionData]: List of imported action data.
    """
    imported_action_data = []

    for obj in selected_objects:
        if hasattr(obj.animation_data, "action"):
            action = obj.animation_data.action
            action_slot = obj.animation_data.action_slot

            if obj.type == "ARMATURE":
                imported_action_data.append(
                    ActionData(
                        action=action,
                        action_slot=action_slot,
                        armature_name=obj.name,
                    )
                )
            else:
                bpy.data.actions.remove(action)

    return imported_action_data


def set_action_and_slot_for_armature(
    armature: bpy.types.Armature, action_data: ActionData
) -> None:
    """
    Apply the action and action slot from the action_data to the armature.

    :param bpy.types.Armature armature: Target armature.
    :param ActionData action_data: Action data containing the action,
        action slot, and source armature name.
    """
    armature.animation_data.action = action_data.action
    armature.animation_data.action_slot = action_data.action_slot
    armature.animation_data.action_slot.name_display = armature.name


def merge_armature_actions(
    armatures: list[bpy.types.Armature], new_name: str | None = None
) -> None:
    """
    Merge the actions of armatures into a single action and set the name if provided.

    :param list armatures: List of target armature objects.
    :param str new_name: Desired name of the new action.
    """
    bpy.ops.object.select_all(action="DESELECT")

    for armature in armatures:
        armature.select_set(True)

    bpy.context.view_layer.objects.active = armatures[0]
    bpy.ops.anim.merge_animation()
    if new_name:
        armatures[0].animation_data.action.name = new_name


def apply_action(
    armatures: list[bpy.types.Armature],
    imported_action_data: list[ActionData],
    action_name: str = "cascadeur_action",
) -> None:
    """
    Apply an action and its corresponding action slot to the armature.

    :param list armatures: List of target armature objects.
    :param list[ActionData] imported_action_data: Imported actions and their
        associated armature names.
    :param str action_name: New name of the action (from Cascadeur scene name),
        defaults to "cascadeur_action".
    """
    # Ensure armatures have animation data before assigning actions.
    for armature in armatures:
        if not hasattr(armature.animation_data, "action"):
            armature.animation_data_create()

    if len(imported_action_data) == 1:
        # If there is only one imported armature use the first selected armature to apply the data to it
        action_data = imported_action_data[0]
        action_data.action.name = action_name

        # Apply action and action slot to the original armature
        set_action_and_slot_for_armature(armatures[0], action_data)
    else:
        for action_data in imported_action_data:
            # Find the original armature for the imported one
            matching_armature = None
            for armature in armatures:
                if action_data.armature_name.startswith(armature.name):
                    matching_armature = armature
                    break

            if matching_armature is None:
                continue
            set_action_and_slot_for_armature(matching_armature, action_data)

        # Merge imported animations into one action
        merge_armature_actions(armatures, action_name)
