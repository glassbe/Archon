import os
import json
import subprocess
import sys
import platform
import argparse

def setup_venv(venv_path=None):
    # If no venv_path is provided, use the one at project root level
    if venv_path is None:
        # Get the absolute path to the current directory
        current_dir = os.path.abspath(os.path.dirname(__file__))
        # Go up one level to get to the project root (from iterations/v3-mcp-support to project root)
        project_root = os.path.dirname(os.path.dirname(current_dir))
        venv_path = os.path.join(project_root, 'venv')
    
    # Check if the virtual environment exists
    if not os.path.exists(venv_path):
        print(f"Error: Virtual environment at {venv_path} does not exist.")
        print("Please make sure the path is correct or create the virtual environment manually.")
        sys.exit(1)
    else:
        print(f"Using existing virtual environment at: {venv_path}")
    
    # No need to install requirements as we're using an existing venv
    print("Note: Using existing virtual environment. Make sure it has all required dependencies installed.")
    
    return venv_path

def generate_mcp_config(venv_path):
    # Get the absolute path to the current directory
    base_path = os.path.abspath(os.path.dirname(__file__))
    
    # Construct the paths based on the operating system
    if platform.system() == 'Windows':
        python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
    else:  # macOS or Linux
        python_path = os.path.join(venv_path, 'bin', 'python')
    
    server_script_path = os.path.join(base_path, 'mcp_server.py')
    
    # Create the config dictionary
    config = {
        "mcpServers": {
            "archon": {
                "command": python_path,
                "args": [server_script_path]
            }
        }
    }
    
    # Write the config to a file
    config_path = os.path.join(base_path, 'mcp-config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"\nMCP configuration has been written to: {config_path}")    
    print(f"\nMCP configuration for Cursor:\n\n{python_path} {server_script_path}")
    print("\nMCP configuration for Windsurf/Claude Desktop:")
    print(json.dumps(config, indent=2))
    
    # Also copy the config to the Codeium directory for Windsurf
    try:
        home_dir = os.path.expanduser("~")
        codeium_config_path = os.path.join(home_dir, '.codeium', 'windsurf', 'mcp_config.json')
        os.makedirs(os.path.dirname(codeium_config_path), exist_ok=True)
        with open(codeium_config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"\nMCP configuration has also been copied to: {codeium_config_path}")
    except Exception as e:
        print(f"\nWarning: Could not copy configuration to Codeium directory: {str(e)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup MCP configuration for Archon')
    parser.add_argument('--venv-path', type=str, help='Path to the virtual environment (optional)')
    args = parser.parse_args()
    
    venv_path = setup_venv(args.venv_path)
    generate_mcp_config(venv_path)
