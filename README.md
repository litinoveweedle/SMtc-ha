# Sequent Microsystems Eight Thermocouples DAQ Home Assistant Integration

Integrate [Eight Thermocouples DAQ](https://sequentmicrosystems.com/products/eight-thermocouples-daq-8-layer-stackable-hat-for-raspberry-pi)
seamlessly with Home Assistant, bringing all your custom functionality into the Home Assistant ecosystem for enhanced control, automation, and ease of use.



## Installation

> This integration requires `SMcommonHA>=0.0.3` from PyPI. Test installed
> Sequent integrations together when changing their shared-library requirements.

> If you already have HACS, I2C and File editor configured, you can skip to [The actual installation](#the-actual-installation)


#### Video tutorials

- [Install HACS video](https://youtu.be/Fl3lATWhQVM) for step 1.
- [Enable I2C and Install file editor video](https://youtu.be/53Zj8NofS7k) for steps 2. and 3.
- [Install and config card drivers video](https://youtu.be/yH2HKjm7j24) for steps 4. and 5. (replace SMioplus-ha with SMtc-ha)

#### Prerequirements

1. Install HACS
    - Follow the official [instructions](https://www.hacs.xyz/docs/use/download/download/)

2. Install and run HassOS I2C Configurator add-on
    - Install [HassOS I2C Configurator](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fadamoutler%2FHassOSConfigurator)
    - Select your profile from the buttom left corner and enable `Advanced mode` in User settings
    - In Settings, Add-ons, Add-on Store, search and install `HassOS I2C Configurator`
    - Disable `Protection mode`
    - Start the add-on

3. Install File editor add-on
    - In Settings, Add-ons, Add-on Store, search and install `File editor`
    - Enable `Show in sidebar`
(see multiple config options bellow)


### The actual installation

4. Install SMtc-ha from HACS
    - Open HACS (from the sidebar)
    - Click on the 3 dots in the top right corner and select `Custom repositories`
    - Repository is `SequentMicrosystems/SMtc-ha` and type is `Integration`
    - Once added, you can now search it in HACS menu and download it

5. Restart Home Assistant, then open **Settings > Devices & services**.
6. Select **Add integration**, choose **Sequent Microsystems Eight Thermocouples DAQ Integration**, and enter the
   card's stack address. Repeat for each card.
7. Use **Configure** to choose entities and their update intervals.

### Upgrading from `SMtc`

Back up Home Assistant first. Uninstall the old integration and install the
updated one; Marketplace may require re-adding the repository. Ensure
`custom_components/SMtc` is removed and only `custom_components/smtc`
remains. Change the top-level `SMtc:` YAML key to `smtc:` and restart.
Existing entity registry entries are migrated to the new domain; conflicting
entries must be resolved before setup can continue.

## Migrating from YAML

Existing `smtc:` YAML is imported once. Check the entries under **Settings >
Devices & services**, remove the YAML section and restart Home Assistant. Later
YAML edits are not imported, and existing entries are not overwritten. Use the
integration UI for further changes.

The legacy examples below are retained for reference:

`configuration.yaml` example:
```yaml
# Loads default set of integrations. Do not remove.
default_config:

# Load frontend themes from the themes folder
frontend:
  themes: !include_dir_merge_named themes

automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml

smtc:
    # + optional configs
```

- Simple stack 0 config:

```yaml
smtc:
```

- Specific stack config:

```yaml
smtc:
    - stack: 2
```

- Multiple cards on different stack levels:

```yaml
smtc:
    - stack: 0
    - stack: 2
    - stack: 3
```

- Only specific entities for different stack levels:

> !The following example is provided for illustrative purposes only and does NOT necessarily represent real entities!

```yaml
smtc:
    - stack: 0
      relay_1:
      relay_3:
      opto_1:
        update_interval: 0.1
    - stack: 2
      relay:
        channels: "1,2,5"
      opto_cnt:
        chan_range: "2..6"
        update_interval: 1
```

[//]: # (__CUSTOM_README__ START)
[//]: # (__CUSTOM_README__ END)

### `configuration.yaml` entities

Possible entities:
```yaml
type_1: -> type_8:  (type: select)
temp_1: -> temp_8:  (type: sensor)
```

Entity options:
- `channels: "1,3,5"` (comma-separated unique channels; takes precedence over `chan_range`)
- `chan_range: "start..end"` (specify inclusive channel range)
- `update_interval: seconds` (specify the update interval for `sensor` and `binary_sensor`, default **30s**)



### Troubleshooting:

1. Enities show up in the overview but do not function correctly
    - Make sure the I2C was enabled correctly. You can check if I2C was initialized properly by running the HassOS I2C Configurator again and checking the logs.

## Preparing a release

1. Publish and verify any required `SMcommonHA` release on PyPI first; update
   and test card requirements together. Check the existing repository releases
   and tags, then set the manifest version to a newer version. Use `X.Y.Z` or a
   prerelease such as `X.Y.Zrc1`.
2. Push the release commit and run **Prepare draft release** from the Actions
   tab on that branch. It runs the card tests, HACS validation and hassfest;
   if they pass, it creates a draft for that commit with tag `v<version>`.
   Prerelease is selected by default. Existing tags are rejected.
3. Review the generated notes and add migration steps, breaking changes,
   supported Home Assistant versions, and any hardware or watchdog limitations.
   Test installation, upgrade and card behavior, then publish the draft manually.

HACS and Marketplace use published GitHub releases for updates. The
`homeassistant` minimum is currently 2026.11.1, the version tested in CI;
older versions have not been verified. HACS validation also requires a
repository description, topics, enabled GitHub issues, and a GitHub-
recognized OSI-approved license. The repository owner must configure these
before the draft-release workflow can pass its validation gate.

## Testing

CI uses Super-Linter to check changed Python and JSON files.

With Python 3.14, install `homeassistant==2026.11.1`,
`pytest-homeassistant==2026.11.1`, and the integration requirements from the
manifest, then run:

```shell
python -m pytest -p no:respx --asyncio-mode=auto -o asyncio_default_fixture_loop_scope=function tests
```

Tests simulate hardware and check the installed driver API. CI installs the
manifest requirements from PyPI. The shared-library release must be published
before that installation can succeed.
