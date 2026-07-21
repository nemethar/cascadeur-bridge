🟠 Blender 4.4+
🔷 Cascadeur 2024.3+
🪟 Windows
🐧 Linux
⚖ GPL-3.0

# Cascadeur Bridge for Blender

Cascadeur Bridge is a Blender add-on that enables faster and more convenient transfer of models, scenes, and animations between Blender and Cascadeur.
For a visual introduction watch the youtube video:

[![Watch the video](https://img.youtube.com/vi/3J5R1G-g8Ig/default.jpg)](https://youtu.be/3J5R1G-g8Ig)

### Table of Content:
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Remove the addon](#remove-the-addon)
- [FAQ](#faq)
- [Support the project](#support-the-project)

## Features

- Start Cascadeur from Blender
- Export from Blender to Cascadeur (Model, Scene, Animation)
- Import from Cascadeur to Blender (Model, Scene, Animation)
- Import animation to selected armature
- Batch import all opened scenes and actions from Cascadeur
- Configure Cascadeur FBX export settings
- Configure Blender FBX import/export settings

## Installation

### Compatibility
All releases are available on the **[GitHub Releases](https://github.com/nemethar/cascadeur-bridge/releases)** page.

| Bridge Version | Blender | Cascadeur |
|----------------|---------|-----------|
| **[1.1.1 (latest)](https://github.com/nemethar/cascadeur-bridge/releases/tag/1.1.1)** | **4.4+** | **2024.3+** |
| [1.1.0](https://github.com/nemethar/cascadeur-bridge/releases/tag/1.1.0) | 3.5 – 4.3 | 2024.3+ |
| [1.0.2](https://github.com/nemethar/cascadeur-bridge/releases/tag/1.0.2) | 3.5 – 4.3 | 2023.2 - 2024.2 |
| [1.0.0](https://github.com/nemethar/cascadeur-bridge/releases/tag/1.0.0) | 3.5 – 4.3 | 2022.3.1 – 2023.1 |
| [0.4.1](https://github.com/nemethar/cascadeur-bridge/releases/tag/0.4.1) | 3.5 – 4.3 | ≤2022.3.1 |

### Installation Steps

https://nemethar.github.io/cascadeur-bridge/doc/installation.mp4

1. Download the appropriate release.
2. Drag the downloaded ZIP to Blender.
3. Open the **Edit → Preferences → Add-ons**
4. Look for the **Cascadeur Bridge** add-on
5. Set the Cascadeur executable path.
6. Click **Install Requirements**.


<details>
<summary><strong> Installing legacy Bridge releases (1.1.0 and earlier)</summary></strong>

1. Download the appropriate release.
2. Open Blender and go to **Edit → Preferences**.
3. Click **Add-ons → Install**.
4. Select the downloaded ZIP.
5. Enable the add-on.
6. Set the Cascadeur executable path.
7. Click **Install Requirements**.

</details>

## Usage

The add-on is available in the **CSC Bridge** tab of Blender's **3D Viewport N-panel**.

![Cascadeur Bridge UI](/doc/addon_side_panel.png)

### Export

#### Export to Cascadeur

Exports the current Blender scene to Cascadeur.

### Import

#### Import Action

Imports the animation from the current Cascadeur scene onto the **selected armatures**.

> **Note:** The selected Blender armatures must exactly match the armature in Cascadeur.

This operator will import the Cascadeur scene as an fbx file, apply the imported action to the selected armature, and then delete the imported objects.

#### Import Scene

Imports the current Cascadeur scene as an FBX file.

#### Batch Import

Imports scenes or animations from **all currently opened Cascadeur scenes**.

### Settings

The default FBX settings are optimized for most workflows, but can be customized if needed.

- **Cascadeur Export Settings** control how Cascadeur exports FBX files.
- **Blender Import/Export Settings** control Blender's FBX importer and exporter.

Once you've found settings that work for your workflow, click **Save Settings** to make them persistent.

### Add-on Preferences

The add-on preferences allow you to:

- Set the Cascadeur executable path.
- Change the name of the **Cascadeur** tab in the N-panel. This is useful if you want to group the Bridge UI with another add-on.


## Remove the addon


### Blender
1. In **Blender** go to **Edit > Preferences > Get Extensions**
2. Search for the **Cascadeur Bridge** extension
3. Click the small dropdown arrow next to its name
4. Select Uninstall and confirm the removal

### Cascadeur
- go to your commands folder (*CASCADEUR PATH\resources\scripts\python\commands*) and delete the ***externals*** folder.


<details>
<summary><strong>Removing legacy Bridge releases (1.1.0 and earlier)</strong></summary>

- from Blender go to Edit > Preferences > Add-ons and click on the Remove button of the add-on.
from Cascadeur
- go to your commands folder (CASCADEUR PATH\resources\scripts\python\commands) and delete the externals folder.
</details>

## FAQ

### Does Bridge work with the free version of Cascadeur?

**Partially.** Sending models from Blender to Cascadeur works, but importing animations back requires an **Indie** or **Pro** license, or an active **14-day trial**.

### Which versions are supported?

Bridge is tested with the latest supported versions of Blender and Cascadeur. If either application receives a major update, the Bridge may also require an update.

### I'm getting `ModuleNotFoundError`

This usually means the required Bridge scripts weren't installed into Cascadeur. Run **Install Requirements** from the add-on preferences, then restart both Blender and Cascadeur.

### Does it support Rigify or Auto-Rig Pro?

Both add-ons generate armatures that include additional mechanism/control bones, so you'll need to export a clean deformation rig.

* **Auto-Rig Pro** includes its own exporter for this, so the **Blender → Cascadeur** transfer must be done manually. Importing the animation back into Blender can then be done with the Bridge. Guide for using ARP with Cascadeur: [video](https://youtu.be/8B2pDvErb8g?si=UadPZxB4wGYw4iFN)
* **Rigify** can be used together with the **[GameRigTools](https://toshicg.gumroad.com/l/game_rig_tools)** add-on to separate the deformation rig from the control rig. Once you have a clean deformation rig, the Bridge can transfer it between Blender and Cascadeur.

In both cases, if you want to apply the imported animation back to your original control rig, you'll need to retarget it. **Auto-Rig Pro** includes built-in retargeting tools.

### I'm getting a socket connection error

Make sure Cascadeur is running, the Bridge scripts are installed, and your firewall isn't blocking localhost communication.

If the Bridge encounters an unexpected error, restarting both Blender and Cascadeur often resolves the issue.

### Does it work on macOS?

Unfortunately no. I can't test the add-on on macOS myself.
I am open to suggestions how to get access to ARM based Mac for testing.


If you have more idea/request or you found a bug please report it in the **[Issues](https://github.com/nemethar/cascadeur-bridge/issues)**.


## Support the Project

If you find Cascadeur Bridge useful, you can support its development by:

- Starring this repository.
- Reporting bugs or suggesting new features.
- Purchasing Cascadeur through my [affiliate link](https://cascadeur.com/plans?ref=aron) and using the promo code **ARON15** to receive a **15% discount**.

Thank you for your support!
---
