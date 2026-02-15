#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Создает текстовый файл с заданным содержимым

version_added: "1.0.0"

description:
    - Этот модуль создает текстовый файл на удаленном хосте.
    - Параметры: path (путь к файлу), content (содержимое), force (перезаписывать или нет).

options:
    path:
        description: Полный путь к создаваемому файлу.
        required: true
        type: str
    content:
        description: Содержимое, которое будет записано в файл.
        required: true
        type: str
    force:
        description: Перезаписывать файл, если он уже существует.
        required: false
        type: bool
        default: false

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Create file with content
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/hello.txt
    content: "Hello World!"
    force: false

# Force overwrite existing file
- name: Force overwrite file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/config.txt
    content: "new content"
    force: true
'''

RETURN = r'''
path:
    description: Путь к созданному файлу.
    type: str
    returned: always
content:
    description: Содержимое, которое было записано.
    type: str
    returned: always
'''

import os
from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
        force=dict(type='bool', required=False, default=False)
    )

    result = dict(
        changed=False,
        path='',
        content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']
    force = module.params['force']

    result['path'] = path
    result['content'] = content

    # Проверяем существование файла
    file_exists = os.path.exists(path)

    # Определяем, нужно ли что-то менять
    if not file_exists:
        result['changed'] = True
    elif force:
        # Если файл есть и force=True - перезаписываем
        result['changed'] = True
    else:
        # Если файл есть и force=False - ничего не делаем
        result['changed'] = False

    # Check mode - только проверяем, но не пишем
    if module.check_mode:
        module.exit_json(**result)

    # Режим выполнения - реально пишем файл
    if result['changed']:
        try:
            # Создаем директорию, если её нет
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            # Записываем файл
            with open(path, 'w') as f:
                f.write(content)
        except Exception as e:
            module.fail_json(msg=f"Ошибка записи файла: {str(e)}", **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
