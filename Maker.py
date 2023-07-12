import os
import re
from shutil import copyfile

def get_latest_file_number():
    file_list = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']
    if file_list:
        latest_file = max(file_list, key=lambda x: int(re.findall(r'\d+', x)[0]))
        return int(re.findall(r'\d+', latest_file)[0])
    else:
        return 0

def update_index_html(title, latest_number):
    index_file = 'index.html'
    button_script = f'<button class="article-button" onclick="window.location.href=\'{latest_number}.html\'">{title}</button>'
    with open(index_file, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            file.write(line)
            if line.strip().startswith('<button class="article-button"'):
                file.write('\n')
                continue
            if line.strip().startswith('</body>'):
                file.write('\n' + button_script + '\n')
        file.truncate()

def create_new_article_file(template_file, title, content, latest_number):
    new_file_name = f'{latest_number + 1}.html'
    copyfile(template_file, new_file_name)
    with open(new_file_name, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if line.strip().startswith('<!-- Article Content -->'):
                file.write(line)
                file.write(f'{content}\n')
            else:
                file.write(line)
        file.truncate()

# User input
title = input('Enter the article title: ')
content = input('Enter the article content: ')
template_file = 'Templates/template.html'

# Get the latest file number
latest_number = get_latest_file_number()

# Update index.html
update_index_html(title, latest_number + 1)

# Create new article file
create_new_article_file(template_file, title, content, latest_number + 1)

print(f'Article "{title}" added successfully!')
