import json
import os
import re
import shutil
from datetime import datetime
import markdownify

# Configuration
EXPORT_DIR = r"C:\Users\micha\Downloads\C-S-452-Database-Modeling-Concepts-2026-Jan-02_21-54-27-884\C-S-452-Database-Modeling-Concepts-2026-Jan-02_21-54-27-884"
COURSE_DATA_PATH = os.path.join(EXPORT_DIR, "viewer", "course-data.js")
FILES_SOURCE_DIR = os.path.join(EXPORT_DIR, "viewer", "files")

TARGET_BASE = r"C:\repos\cs452\canvas"
MODULES_DIR = os.path.join(TARGET_BASE, "modules")
PAGES_DIR = os.path.join(TARGET_BASE, "pages")
FILES_DEST_DIR = os.path.join(TARGET_BASE, "files")
GLOBAL_ARGS_PATH = os.path.join(TARGET_BASE, "global_args.yaml")

# Helpers
def safe_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '', name).strip().replace(' ', '-').replace('--', '-')

def load_course_data():
    with open(COURSE_DATA_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
        # Strip "window.COURSE_DATA = " and ";"
        json_str = content.replace("window.COURSE_DATA = ", "").strip().rstrip(";")
        return json.loads(json_str)

def convert_html(html, rel_path_prefix="../"):
    if not html:
        return ""
    # Fix file links: "viewer/files/" -> "files/" or relative
    # In mdx-canvas, usually best to use absolute from content root or standard paths.
    # But for markdown files in pages/, images usually need to be reachable.
    # Let's assume we copy files to canvas/files.
    # Pages in canvas/pages/xxxx.md need ../files/xxxx
    
    html = html.replace('src="viewer/files/', f'src="{rel_path_prefix}files/')
    html = html.replace('href="viewer/files/', f'href="{rel_path_prefix}files/')
    
    try:
        md = markdownify.markdownify(html, heading_style="ATX")
        return md
    except Exception as e:
        print(f"Error converting HTML: {e}")
        return html

def main():
    data = load_course_data()
    
    # Ensure directories
    os.makedirs(MODULES_DIR, exist_ok=True)
    os.makedirs(PAGES_DIR, exist_ok=True)
    os.makedirs(FILES_DEST_DIR, exist_ok=True)

    # 1. Copy Files
    print("Copying files...")
    if os.path.exists(FILES_SOURCE_DIR):
        # We need to copy recursively but flatten or keep structure?
        # The viewer/files seems flat + Uploaded Media.
        # Let's simple copy the whole tree to canvas/files
        # shutil.copytree(FILES_SOURCE_DIR, FILES_DEST_DIR, dirs_exist_ok=True)
        # Actually user wants "files" dir.
        pass # Doing this manually or via command might be safer/faster, but script can do it.
        # Check if too large? The list_dir showed it's manageable.
    
    dates_map = {}
    
    # 2. Process Modules
    for i, mod in enumerate(data.get('modules', [])):
        mod_name = mod['name']
        print(f"Processing Module: {mod_name}")
        safe_mod_name = f"{i:02d}-{safe_filename(mod_name)}"
        mod_dir = os.path.join(MODULES_DIR, safe_mod_name)
        os.makedirs(mod_dir, exist_ok=True)
        
        # Create module XML
        xml_content = [f'<module title="{mod_name}">']
        
        for item in mod.get('items', []):
            title = item['title']
            item_type = item['type'] # Assignment, Quizzes::Quiz, WikiPage, File, ExternalUrl, SubHeader
            indent = item.get('indent', 0)
            
            if item_type == "SubHeader":
                xml_content.append(f'    <item type="SubHeader" title="{title}" />')
                continue
            
            if item_type == "ExternalUrl":
                url = item.get('external_url', '')
                xml_content.append(f'    <item type="ExternalUrl" title="{title}" external_url="{url}" indent="{indent}" />')
                continue

            # Check dates
            due_at = item.get('dueAt')
            date_var = ""
            if due_at:
                # Create variable name
                var_name = f"DUE_{re.sub(r'[^A-Z0-9]', '_', title.upper())}_{i}"
                dates_map[var_name] = due_at
                date_var = f' due_at="{{{{ {var_name} }}}}"'

            if item_type == "Assignment":
                # Create Assignment File
                safe_title = safe_filename(title)
                assign_filename = f"{safe_title}.canvas.md.xml.jinja"
                assign_path = os.path.join(mod_dir, assign_filename)
                
                desc_md = convert_html(item.get('content', ''), rel_path_prefix="../../")
                points = item.get('pointsPossible', 0)
                
                # Check submission types logic (simplified)
                sub_types = item.get('submissionTypes', [])
                if isinstance(sub_types, str): sub_types = [sub_types]
                # Map to xml tags... simplified for now:
                # <assignment ...> <description> ... </description> </assignment>
                
                with open(assign_path, 'w', encoding='utf-8') as f:
                    f.write(f'<assignment title="{title}" points_possible="{points}"{date_var}>\n')
                    f.write(f'  <description>\n{desc_md}\n  </description>\n')
                    f.write('</assignment>')
                
                xml_content.append(f'    <include path="{assign_filename}" />')

            elif item_type == "Quizzes::Quiz":
                # Create Placeholder Quiz
                safe_title = safe_filename(title)
                quiz_filename = f"{safe_title}-quiz.canvas.md.xml.jinja"
                quiz_path = os.path.join(mod_dir, quiz_filename)
                
                with open(quiz_path, 'w', encoding='utf-8') as f:
                    f.write(f'<quiz title="{title}"{date_var}>\n')
                    f.write(f'  <description>TODO: Migrate Quiz Questions</description>\n')
                    f.write('</quiz>')
                
                xml_content.append(f'    <include path="{quiz_filename}" />')

            elif item_type == "WikiPage":
                # Find page content in data['pages']? Or is it in item?
                # The export usually has 'page_url' in item, and content in pages list.
                # But looking at snippet: "type":"WikiPage"... "content": "..."
                # Wait, the snippet shows items with type WikiPage having content!
                # ex: "id":2643445 ... "content":"<p>Today we will..."
                
                page_content = item.get('content', '')
                safe_title = safe_filename(title)
                page_filename = f"{safe_title}.md"
                # Pages go to canvas/pages/ usually, but can be module specific.
                # Let's put them in global pages to avoid duplicates if referenced multiple times?
                # or just global pages folder.
                page_file_path = os.path.join(PAGES_DIR, page_filename)
                
                md_content = convert_html(page_content, rel_path_prefix="../")
                
                with open(page_file_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                
                # In module xml:
                # We need to define the page content? or just link?
                # mdx-canvas allows <item type="page" title="..." content_id="...">
                # We need to ensure the page resource is created.
                # We can use <page> tag in the module file to define it, or <include>.
                # Best pattern: <page title="..." url="..."> <include ...> </page>
                # Then <item type="page" ...>
                
                # To keep module file clean, let's allow the page definition to be in the module or separate?
                # Simplified: Define page IN the module file for now to ensure connectivity.
                
                xml_content.append(f'    <div class="page-def">') # Logic block
                xml_content.append(f'      <page title="{title}"> <include path="../../pages/{page_filename}" /> </page>')
                xml_content.append(f'    </div>')
                xml_content.append(f'    <item type="page" title="{title}" indent="{indent}" />')

            elif item_type == "File":
                # Copy file logic handled by bulk copy?
                # We just need to reference it.
                # The item title might not match filename.
                # Check if item has 'url' or 'filename'?
                # Snippet: {"id":2643447,"title":"ColumnFamilyDatabases.pptx","type":"Attachment"... "content":"viewer/files/ColumnFamilyDatabases-1.pptx"}
                # "type": "Attachment" or "File"? Snippet says "Attachment".
                # "type": "Quizzes::Quiz"
                pass
            
            elif item_type == "Attachment":
                 # Handle file attachment
                 file_path = item.get('content', '') # "viewer/files/..."
                 fname = os.path.basename(file_path)
                 xml_content.append(f'    <file path="../../files/{fname}" />') # This uploads the file
                 # And adds it to module? <item type="file"> requires file ID.
                 # <file> tag uploads it.
                 # <item type="file" title="..."> needs to link to it.
                 # mdx-canvas <file> tag *is* a module item if inside a module?
                 # No, <file> uploads it. <item type="file"> adds it to module.
                 # Actually, <file> tag inside <module> adds it as an item?
                 # Documentation says: <file path>
                 xml_content.append(f'    <item type="file" title="{title}" > <file path="../../files/{fname}" /> </item>')
                 # Wait, looking at docs/examples...
                 # <file path="..." /> uploads and potentially return id.
                 # Let's use <file path="..." /> inside module if supported.
                 pass

        xml_content.append('</module>')
        
        # Write module file
        mod_file_path = os.path.join(mod_dir, f"{safe_mod_name}.canvas.md.xml.jinja")
        with open(mod_file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(xml_content))
            
    # 3. Update global_args.yaml
    with open(GLOBAL_ARGS_PATH, 'a', encoding='utf-8') as f:
        f.write("\n# Migrated Due Dates\n")
        for k, v in dates_map.items():
            f.write(f'{k}: "{v}"\n')
    
    # 4. Copy Files
    shutil.copytree(FILES_SOURCE_DIR, FILES_DEST_DIR, dirs_exist_ok=True)
    print("Migration complete!")

if __name__ == "__main__":
    main()
