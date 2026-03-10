import re

path = 'c:/Users/shiva/OneDrive/Desktop/anu_bhai/securetech_profile.html'
with open(path, 'rb') as f:
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

urls = re.findall(r'''src=['"]([^'"]+)['"]''', text)

with open('c:/Users/shiva/OneDrive/Desktop/anu_bhai/images_list.txt', 'w', encoding='utf-8') as f:
    for u in sorted(set(urls)):
        if u.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp')):
            f.write(u + '\n')
