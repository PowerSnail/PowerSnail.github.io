import shutil
import datetime
import subprocess

draft_name = '{}-{}.md'.format(datetime.date.today().isoformat(), hash(datetime.datetime.today().isoformat()).__str__()[0:6])
markdown_editor = "code"

shutil.copyfile('./page_simple.md', draft_name)

process = subprocess.Popen([markdown_editor, draft_name])
process.wait()

title = category = 'unspecified'

with open(draft_name, 'r') as f:
    f.readline()
    line = f.readline()
    while line != '---':
        if 'title: ' in line:
            title = line.split(':').pop().strip()
        elif 'categories' in line:
            category = f.readline().split('-').pop().strip()


filename = '{}-{}.md'.format(datetime.date.today().isoformat(), title)
shutil.copyfile(draft_name, '../_posts/{}/{}'.format(category, filename))



