import datetime
import os
import re
import shutil


QUARANTINE_ROOT_DIR='/tmp/php_cleaning/quarantine'

class Site(object):
  def __init__(self, name, directory):
    self.name = name
    self.directory = directory
    self.quarantine = Quarantine(QUARANTINE_ROOT_DIR, self.name)

  def files(self):
    all_filenames = []
    for root, dirnames, filenames in os.walk(self.directory):
      for filename in filenames:
        all_filenames.append(
            File(filename, path=root, quarantine=self.quarantine))
    return all_filenames

  def php_files(self):
    files =  []
    for file in self.files():
      if file.is_php():
        files.append(file)
    return files


class Quarantine(object):
  def __init__(self, root_dir, name):
    self.root_dir = root_dir
    self.name = name
    self.timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    self.directory = os.path.join(self.root_dir, self.name, self.timestamp)
    self.create_directory_tree()

  def create_directory_tree(self):
    if not os.path.isdir(self.directory):
      os.makedirs(self.directory)
    
  def add_file(self, file):
    target_directory = '%s/%s' % (self.directory, file.path)
    if not os.path.isdir(target_directory):
      os.makedirs(target_directory)
    shutil.copyfile(file.full_path(), os.path.join(target_directory, file.name))
    

class File(object):
  SUSPICIOUS_LINE_LENGTH = 2000

  def __init__(self, filename, path=None, quarantine=None):
    self.name = filename
    self.path = path
    self.quarantine = quarantine

  def full_path(self):
    return os.path.join(self.path, self.name)

  def is_php(self):
    return re.search('\.php$', self.name) is not None

  def line_count(self):
    return len(self.content())

  def check_first_line(self):
    if self.line_count() > 0:
      if (len(self.content()[0]) > self.SUSPICIOUS_LINE_LENGTH):
        return True
    return False

  def is_infected(self):
    return self.check_first_line()

  def fix_first_line(self, line):
    fixed_line = re.sub(r'\<\?php.*?\?\>', '', line, count=1)
    if (fixed_line == line):
      print line
    else:
      if line != '<?php':
        print fixed_line
      return fixed_line

  def cure(self):
    if self.quarantine:
      self.quarantine.add_file(self)
    first_line = self.fix_first_line(self.content()[0])
    new_content = first_line + '\n' + ''.join(self.content()[1:])
    self.write(new_content)

  def write(self, new_content):
    myFile = open(self.full_path(), 'w')
    myFile.write(new_content)
    myFile.close()

  def convert_003_chars(self, content):
    new_content = []
    for line in content:
      lines = re.sub(r'\r', '\n', line)
    for line in lines.split('\n'):
      new_content.append(line)
    return new_content

  def content(self, encoding=None):
    with open(self.full_path(), 'r') as content_file:
      content = content_file.readlines()
    # Some DOS files (^M) are considered as a single long line. 
    if content and re.search(r'\r', content[0]):
      content = self.convert_003_chars(content)
    if encoding:
      return [line.encode(encoding) for line in content]
    else:
      return content


site = Site('all_sites', '/Users/sebadel/src/php_site_curator')
# site = Site('all_sites', '/webspace')
for file in site.php_files():
  if file.is_infected():
    print file.full_path()
    file.cure()
