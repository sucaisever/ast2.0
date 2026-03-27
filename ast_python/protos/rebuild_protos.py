
import os
import subprocess
import sys
import shutil

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_dir = os.path.join(project_root, "python_protogen")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    protos = [
        "common/events.proto",
        "common/rpcmeta.proto",
        "products/understanding/base/au_base.proto",
        "products/understanding/ast/ast_service.proto"
    ]
    
    print(f"Generating Python code into {output_dir}...")
    
    # Run protoc
    cmd = [
        sys.executable, "-m", "grpc_tools.protoc",
        f"--proto_path={script_dir}",
        f"--python_out={output_dir}",
        f"--grpc_python_out={output_dir}"
    ] + [os.path.join(script_dir, p) for p in protos]
    
    try:
        subprocess.check_call(cmd)
        print("Protoc execution successful.")
    except subprocess.CalledProcessError as e:
        print(f"Protoc failed: {e}")
        return

    # Path patching (Simulating sed)
    print("Patching import paths...")
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Replace top-level imports with absolute package imports
                new_content = content.replace("from common import ", "from python_protogen.common import ")
                new_content = new_content.replace("import common.", "import python_protogen.common.")
                new_content = new_content.replace("from products import ", "from python_protogen.products import ")
                new_content = new_content.replace("import products.", "import python_protogen.products.")
                
                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
        
        # Ensure __init__.py exists
        init_file = os.path.join(root, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f: pass

    print("✅ Protobuf regeneration complete.")

if __name__ == "__main__":
    main()
