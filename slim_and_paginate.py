import json, gzip, os

# Read current modules.json
with open('modules.json', 'r', encoding='utf-8-sig') as f:
    modules = json.load(f)

orig_size = os.path.getsize('modules.json')
print(f'Original entries: {len(modules)}')
print(f'Original size: {orig_size} bytes')

# Slim: keep only latest release (first in releases array) with releaseAssets[0]
for mod in modules:
    rels = mod.get('releases', [])
    if rels:
        latest = rels[0]
        assets = latest.get('releaseAssets', [])
        if assets:
            a = assets[0]
            mod['releases'] = [{
                'tagName': latest.get('tagName', ''),
                'name': latest.get('name', ''),
                'createdAt': latest.get('createdAt', ''),
                'releaseAssets': [{
                    'name': a.get('name', ''),
                    'downloadUrl': a.get('downloadUrl', ''),
                    'size': a.get('size', 0),
                    'downloadCount': a.get('downloadCount', 0),
                }]
            }]
        else:
            mod['releases'] = []
    mod.pop('betaReleases', None)
    mod.pop('readme', None)

# Write slimmed modules.json
with open('modules.json', 'w', encoding='utf-8') as f:
    json.dump(modules, f, ensure_ascii=False, separators=(',', ':'))

slim_size = os.path.getsize('modules.json')
print(f'Slimmed entries: {len(modules)}')
print(f'Slimmed size: {slim_size} bytes')

# gzip size
with open('modules.json', 'rb') as f_in:
    with gzip.open('modules.json.gz', 'wb') as f_out:
        f_out.writelines(f_in)
gz_size = os.path.getsize('modules.json.gz')
print(f'Slimmed gzip size: {gz_size} bytes')
os.remove('modules.json.gz')

# Generate paginated files
os.makedirs('module-list', exist_ok=True)
PAGE_SIZE = 30
total = len(modules)
total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE

for page in range(1, total_pages + 1):
    start = (page - 1) * PAGE_SIZE
    end = min(start + PAGE_SIZE, total)
    page_modules = modules[start:end]
    
    page_data = {
        'page': page,
        'total': total,
        'totalPages': total_pages,
        'modules': page_modules
    }
    
    fname = f'module-list/page_{page}.json'
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(page_data, f, ensure_ascii=False, separators=(',', ':'))

# Check page sizes (first 5)
print(f'Total pages: {total_pages}')
print('First 5 pages gzip sizes:')
for page in range(1, min(total_pages + 1, 6)):
    fname = f'module-list/page_{page}.json'
    with open(fname, 'rb') as f_in:
        with gzip.open(fname + '.gz', 'wb') as f_out:
            f_out.writelines(f_in)
    gz = os.path.getsize(fname + '.gz')
    os.remove(fname + '.gz')
    print(f'  page_{page}: {gz} bytes gzip')

# Verify entry count preserved
print(f'Verification: {total} entries in modules.json')
print(f'Verification: {total_pages} pages generated')
