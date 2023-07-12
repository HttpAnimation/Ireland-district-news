import os
import re
from shutil import copyfile
from jinja2 import Environment, FileSystemLoader

def get_latest_file_number():
    file_list = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']
    if file_list:
        latest_file = max(file_list, key=lambda x: int(re.findall(r'\d+', x)[-1]))
        return int(re.findall(r'\d+', latest_file)[-1])
    else:
        return 0

def update_index_html(title, latest_number):
    index_file = 'index.html'
    button_script = f'<button class="article-button" onclick="window.location.href=\'{latest_number}.html\'">{title}</button>'
    with open(index_file, 'r') as file:
        content = file.read()
    updated_content = re.sub(r'</div>\s*</body>', f'{button_script}\n</div>\n</body>', content)
    with open(index_file, 'w') as file:
        file.write(updated_content)

def create_new_article_file(template_file, title, content, latest_number):
    new_file_name = f'{latest_number}.html'
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_file)
    rendered_content = template.render(title=title, content=content)
    with open(new_file_name, 'w') as file:
        file.write(rendered_content)

# Initialize the loop control variable
add_another = True

while add_another:
    # User input
    title = input('Enter the article title (or "exit" to quit): ')

    if title.lower() == 'exit':
        add_another = False
        break

    # Read content from file
    with open('maker.api', 'r') as file:
        content = file.read()

    template_file = 'Templates/template.html'

    # Get the latest file number
    latest_number = get_latest_file_number()

    # Update index.html
    update_index_html(title, latest_number + 1)

    # Create new article file
    create_new_article_file(template_file, title, content, latest_number + 1)

    print(f'Article "{title}" added successfully!')

print('Exiting the script.')

