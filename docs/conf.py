import os
import sys

sys.path.append(os.path.abspath('..'))

project = 'PhotoShare'
copyright = '2024, PythonStars'
author = 'PythonStars'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']

html_theme = 'nature'
