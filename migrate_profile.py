import os
import shutil
import re
import urllib.parse

base_dir = r"c:\Users\shiva\OneDrive\Desktop\anu_bhai"
src_html = os.path.join(base_dir, "securetech_profile.html")
dest_html = os.path.join(base_dir, r"secure\templates\securetech_profile.html")
dest_img_dir = os.path.join(base_dir, r"secure\static\images\profile")

os.makedirs(dest_img_dir, exist_ok=True)

with open(src_html, 'rb') as f:
    content = f.read()

text = None
for enc in ['utf-8', 'utf-16', 'utf-16le']:
    try:
        text = content.decode(enc)
        break
    except Exception:
        pass

if not text:
    text = content.decode('latin-1')

def replacer(match):
    original_src = match.group(1)
    if not original_src.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp')):
        return match.group(0)
    
    file_path_unquoted = urllib.parse.unquote(original_src)
    # We also check the unquoted vs quoted as fallback
    
    paths_to_try = [
        os.path.join(base_dir, original_src),
        os.path.join(base_dir, file_path_unquoted),
        os.path.join(base_dir, original_src.replace('/', '\\')),
        os.path.join(base_dir, file_path_unquoted.replace('/', '\\'))
    ]
    
    full_src = None
    for p in paths_to_try:
        if os.path.exists(p) and os.path.isfile(p):
            full_src = p
            break
            
    basename = os.path.basename(file_path_unquoted)
    full_dest = os.path.join(dest_img_dir, basename)
    
    if full_src:
        try:
            shutil.copy2(full_src, full_dest)
        except Exception as e:
            print(f"Failed to copy {full_src}: {e}")
    else:
        print(f"Warning: File not found for: {original_src}")
        
    new_src = f"{{{{ url_for('static', filename='images/profile/{basename}') }}}}"
    return f'src="{new_src}"'

new_text = re.sub(r'''src=['"]([^'"]+)['"]''', replacer, text)

with open(dest_html, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Migration completed.")
