import os
import subprocess
import configparser
from pathlib import Path
import argparse

def get_config_path():
    return Path.home() / ".config" / "AppImage-Launcher" / "config.ini"

def load_config():
    config_path = get_config_path()
    config = configparser.ConfigParser()
    if config_path.exists():
        config.read(config_path)
    return config

def save_config(appimage_dir):
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config = configparser.ConfigParser()
    config["Settings"] = {"AppImageDir": appimage_dir}
    with open(config_path, "w") as configfile:
        config.write(configfile)

def get_appimage_dir():
    config = load_config()
    if "Settings" in config and "AppImageDir" in config["Settings"]:
        return config["Settings"]["AppImageDir"]
    appimage_dir = input("Enter the directory where your AppImages are stored: ").strip()
    save_config(appimage_dir)
    return appimage_dir

def create_extract_folder(base_dir):
    extract_path = Path(base_dir) / "Extract"
    extract_path.mkdir(exist_ok=True)
    return extract_path

def ensure_executable(appimage):
    if not os.access(appimage, os.X_OK):
        print(f"Setting execute permission for {appimage}")
        os.chmod(appimage, 0o755)

def extract_appimages(appimage_dir, extract_path, force=False):
    for appimage in Path(appimage_dir).glob("*.AppImage"):
        ensure_executable(appimage)
        app_name = appimage.stem
        
        app_extract_path = extract_path / app_name
        if app_extract_path.exists() and not force:
            print(f"Skipping {appimage.name}, already extracted.")
            continue
        
        app_extract_path.mkdir(exist_ok=True)
        print(f"Extracting {appimage.name}...")
        try:
            subprocess.run([str(appimage), "--appimage-extract"], cwd=app_extract_path, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error extracting {appimage.name}: {e}")

def find_best_icon(app_extract_path):
    icon_candidates = list(app_extract_path.glob("**/usr/share/icons/**/*.png"))
    icon_candidates += list(app_extract_path.glob("**/usr/share/pixmaps/*.png"))
    diricon = app_extract_path / "squashfs-root/.DirIcon"
    
    if diricon.exists():
        return diricon
    elif icon_candidates:
        return sorted(icon_candidates, key=lambda x: len(str(x)))[0]  
    return None

def find_and_move_icons(extract_path, icons_dir):
    icons_dir.mkdir(exist_ok=True)
    icon_map = {}
    
    for app_folder in extract_path.iterdir():
        if app_folder.is_dir():
            app_name = app_folder.name
            best_icon = find_best_icon(app_folder)
            
            if best_icon:
                icon_dest = icons_dir / f"{app_name}.png"
                icon_dest.write_bytes(best_icon.read_bytes())
                icon_map[app_name] = icon_dest
    
    return icon_map

def create_desktop_entry(appimage, icon_map, desktop_dir):
    app_name = appimage.stem
    icon_path = icon_map.get(app_name, "default")
    desktop_file = Path(desktop_dir) / f"{app_name}.desktop"
    
    with open(desktop_file, "w") as f:
        f.write(f"""[Desktop Entry]
Type=Application
Name={app_name}
Exec={appimage}
Icon={icon_path}
Terminal=false
Categories=Utility;
""")
    
    desktop_file.chmod(0o755)
    print(f"Shortcut created: {desktop_file}")

def refresh_launcher():
    subprocess.run(["update-desktop-database", Path.home() / ".local/share/applications"], check=False)

def delete_folder_contents(folder):
    for item in sorted(folder.glob("**/*"), reverse=True):
        if item.is_file() or item.is_symlink():
            item.unlink()
        elif item.is_dir():
            item.rmdir()

def prompt_cleanup(extract_path):
    if input("Do you want to delete the Extract folder to save space? (y/n): ").strip().lower() == "y":
        delete_folder_contents(extract_path)
        extract_path.rmdir()
        print("Extract folder deleted.")

def main():
    parser = argparse.ArgumentParser(description="AppImage Launcher")
    parser.add_argument("--force", action="store_true", help="Force re-extraction of AppImages")
    args = parser.parse_args()
    
    appimage_dir = get_appimage_dir()
    extract_path = create_extract_folder(appimage_dir)
    icons_dir = Path(appimage_dir) / "Icons"
    desktop_dir = Path.home() / ".local/share/applications"
    desktop_dir.mkdir(parents=True, exist_ok=True)
    
    extract_appimages(appimage_dir, extract_path, force=args.force)
    icon_map = find_and_move_icons(extract_path, icons_dir)  
    
    for appimage in Path(appimage_dir).glob("*.AppImage"):
        create_desktop_entry(appimage, icon_map, desktop_dir)
    
    refresh_launcher()
    print("All AppImages processed, icons stored, and shortcuts created.")
    
    prompt_cleanup(extract_path)

if __name__ == "__main__":
    main()
