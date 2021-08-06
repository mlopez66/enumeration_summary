import subprocess
import json
from pathlib import Path
import re

import pystache
from tomark import Tomark


def targeted_to_port_data(content):
    string = ""
    service_position = 0
    data = []
    for line in content.splitlines():
        if not line.startswith('#') and not line.startswith('Nmap') and not line.startswith('Host') and line != '':
            if line.startswith("PORT"):
                service_position = line.find("VERSION")
            if line[0].isdigit():
                port = re.search(r'^\d*', line)[0]
                service = line[service_position:]
                data.append({
                    'Port': port,
                    'Service': service,
                    'Idea': '',
                    'Needs': '[ ]'
                })
    return Tomark.table(data)


def parse_targeted_content(content):
    port_table = targeted_to_port_data(content)
    targeted = """
## Targeted

```bash
{}
```

""".format(content)
    return port_table, targeted


def parse_ffuf_json_content(filename, content):
    fuzzed_urls = []
    json_content = json.loads(content)
    for elements in json_content['results']:
        fuzzed_urls.append({
            'url': elements['url'],
            'status': elements['status'],
            'redirect': elements['redirectlocation']
        })
    fuzzed_urls = sorted(fuzzed_urls, key=lambda k: k['status'])
    return """
## {}

{}

""".format(filename, Tomark.table(fuzzed_urls))


def parse_other_content(filename, content):
    return """"
## {}

```bash
{}
```

""".format(filename, content)


def parse_info_file_content(project, files):
    port_table = ""
    parsed_content = ""
    targeted_content = ""
    ffuf_content = ""
    for file in files:
        filename = file.name
        with open(file.absolute(), 'r') as f:
            content = f.read()
        if filename == "allPorts":
            pass
        elif filename == "targeted":
            port_table, targeted_content = parse_targeted_content(content)
        elif "fuzz" in filename:
            ffuf_content = parse_ffuf_json_content(filename, content)
        else:
            parsed_content += parse_other_content(filename, content)

    return {
        'project_name': project,
        'port_table': port_table,
        'targeted': targeted_content,
        'ffuf': ffuf_content,
        'other': parsed_content
    }


def generate_attacker_file(content, output_filename, output_folder):
    path_temp = Path(__file__).resolve().parent / "files"
    renderer = pystache.Renderer(file_encoding='utf-8', search_dirs=str(path_temp), string_encoding='utf-8')
    return renderer.render(renderer.load_template('attack'), content)


def write_file(output_file, info_content):
    with open(output_file, "w") as f:
        f.write(info_content)


def create_attack_info(enumeration_directory_path, output_filename, output_folder):
    files = [x for x in enumeration_directory_path.glob('**/*') if x.is_file()]
    content = parse_info_file_content(enumeration_directory_path.resolve().parent.name, files)
    info_content = generate_attacker_file(content, output_filename, output_folder)
    output_file = output_folder / output_filename
    write_file(output_file.absolute(), info_content)
    subprocess.Popen(['typora', str(output_file.absolute())], close_fds=True)
