# Role Name

linux-setup

## Description

This role automates the installation of a full-featured developer environment on Linux laptops, including all essential development tools and applications. It supports both Ubuntu 24.04 and Red Hat Enterprise Linux 9.

## Requirements

- Ansible 2.12+
- Target system must have disk partitioning already completed.
- Internet access is required to install packages from repositories.
- EPEL repository must be available for Red Hat-based systems.
- Flatpak support requires Flatpak runtime installed on the system.

## Role Variables

### General Variables
- `os_family`: (string) The OS family: `debian` or `redhat` (automatically detected).
- `package_type`: (string) The package type: `deb` or `rpm`.
- `package_manager`: (string) The package manager: `apt` or `dnf`.

### Feature Toggles
- `install_kde`: (boolean) Whether to install KDE desktop.
- `install_extra_tools`: (boolean) Whether to install extra developer tools.
- `install_citrix`: (boolean) Whether to install Citrix Workspace App.

### Package Lists
- `development_packages`: Common development tools across both distros.
- `development_packages_os_specific`: Additional dev tools per OS.
- `repository_apps`: Apps installed via system package manager.
- `repository_apps_extra`: Ubuntu-only apps from additional repositories.
- `flatpak_apps`: Flatpak apps to be installed from Flathub.
- `flatpak_apps_redhat`: Extra Flatpak apps for RedHat (e.g. OBS Studio).
- `python_packages`: Python packages installed in a virtualenv.

### KDE Packages
- `kde_packages`: KDE desktop packages.

### Citrix Workspace
- `citrix_dependencies`: Required libraries for Citrix installation.
- `citrix_temp_file`: Temporary file path for downloaded Citrix package.
- `citrix_install_path`: Path where Citrix should be installed.

### Citrix Script Integration
- A separate script (YAML playbook) is used to fetch the latest Citrix Workspace App download URL using headless Selenium and Chromium.

### Other Variables
- `vscode_extensions`: Visual Studio Code extensions to install.

## Dependencies

This role has no direct dependencies but expects repositories like Microsoft VS Code and EPEL to be available or configured.

## Example Playbook

```yaml
- name: Install full Linux development environment
  hosts: all
  become: true
  roles:
    - linux-setup
```

## License

MIT-0

## Author Information

Author: Your Name  
Company: Your Company (optional)

