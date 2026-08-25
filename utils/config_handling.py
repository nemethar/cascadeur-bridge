import bpy

import os
import configparser
from typing import Any
from .csc_handling import CascadeurHandler

config_path = os.path.join(os.path.dirname(__file__), "..", "settings.cfg")


def get_config() -> configparser.ConfigParser:
    """
    Get the ConfigParser object for the settings.cfg file.

    :return configparser.ConfigParser: ConfigParser for the config file
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def get_config_parameter(
    section: str,
    parameter: str,
    data_type=str,
    fallback=None,
    config: configparser.ConfigParser = None,
) -> Any:
    """
    Get config parameter value from the config file.

    :param str section: Section name of the config
    :param str parameter: Parameter name
    :param _type_ data_type: Parameter value data type, defaults to str
    :param _type_ fallback: Fallback value if parameter is not found, defaults to None
    :param configparser.ConfigParser config: ConfigParser for the config file, defaults to None
    :return Any: Value of the config parameter
    """
    if config is None:
        config = get_config()

    get_method = {
        str: config.get,
        bool: config.getboolean,
        int: config.getint,
        float: config.getfloat,
        set: config.get,
    }.get(data_type, config.get)

    if data_type is set:
        # Check if the parameter exists in the config
        if config.has_option(section, parameter):
            value = config.get(section, parameter)
            # Check if the value is empty
            value = eval(value) if value else set()
        else:
            value = fallback
    else:
        value = get_method(section, parameter, fallback=fallback)

    return value


def set_config_parameter(
    section: str,
    parameter: str,
    value: str,
    config: configparser.ConfigParser = get_config(),
) -> None:
    """
    Set the given configuration to value in the section with the provided parameter.

    :param str section: Section name in the config file
    :param str parameter: Parameter of the config
    :param str value: Value of the config
    :param configparser.ConfigParser config: ConfigParser object, defaults to get_config()
    """
    config.set(section, parameter, value)
    with open(config_path, "w") as configfile:
        config.write(configfile)


def get_panel_name() -> str:
    """
    Get the N panel name from the config file. Defaults to CSC Bridge.

    :return str: N panel name
    """
    return get_config_parameter("Addon Settings", "panel_name", fallback="CSC Bridge")


def save_settings(groups: list[str] = None) -> None:
    """
    Save settings from the specified property groups to the settings.cfg file.
    If groups is None, all property groups are saved.

    :param list[str] groups: Names of the property groups to save, defaults to None
    :return bool: True if settings were saved successfully, otherwise False
    """
    try:
        config = get_config()
        addon_props = bpy.context.scene.cbb_settings

        for group_name, _ in addon_props.rna_type.properties.items():
            if group_name in {"rna_type", "name", "network"}:
                continue

            # Filtering
            if groups is not None and group_name not in groups:
                continue

            section: str = group_name.replace("_", " ").capitalize()

            if not config.has_section(section):
                config.add_section(section)

            group = getattr(addon_props, group_name)

            for property_name, _ in group.rna_type.properties.items():
                if property_name in {"rna_type", "name"}:
                    continue

                value = getattr(group, property_name)
                config.set(section, property_name, str(value))

        with open(config_path, "w") as configfile:
            config.write(configfile)
        return True
    except Exception as e:
        print(f"Failed to save settings: {e}")
        return False


def reset_settings(groups: list[str] = None) -> None:
    """
    Reset the specified property groups to their default values and remove
    their corresponding sections from the settings.cfg file.

    If groups is None, all property groups are reset.

    :param list[str] groups: Names of the property groups to reset, defaults to None
    """
    config = get_config()
    addon_props = bpy.context.scene.cbb_settings

    for group_name, _ in addon_props.rna_type.properties.items():
        if group_name in {"rna_type", "name", "network"}:
            continue

        # Filtering
        if groups is not None and group_name not in groups:
            continue

        section = group_name.replace("_", " ").capitalize()

        # Remove the section from the config
        if config.has_section(section):
            config.remove_section(section)

        # Reset all properties in this group
        group = getattr(addon_props, group_name)

        for property_name, _ in group.rna_type.properties.items():
            if property_name in {"rna_type", "name"}:
                continue

            group.property_unset(property_name)

    # Save the modified config once
    with open(config_path, "w") as config_file:
        config.write(config_file)


def save_port_number() -> bool:
    section = "Addon Settings"
    addon_props = bpy.context.scene.cbb_settings
    port_number = addon_props.network.cbb_port

    # Cascadeur config
    ch = CascadeurHandler()
    commands_path = os.path.join(ch.commands_path, "blender_bridge", "settings.cfg")
    csc_config = configparser.ConfigParser()
    csc_config.read(commands_path)
    csc_config.set(section, "port", str(port_number))
    try:
        with open(commands_path, "w") as configfile:
            csc_config.write(configfile)
    except PermissionError as e:
        return False
    # Blender config
    config = get_config()
    if not config.has_section(section):
        config.add_section(section)

    set_config_parameter(section, "port", str(port_number))
    return True
