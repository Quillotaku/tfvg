#!/usr/bin/python3
import glob
import re
import string
from jinja2 import Template
import sys
import os

#add option to delete deleted variables only

def get_template(tpl):
    if tpl == "var_with_default":
        var_template = '''
{% for i in variables -%}
variable "{{ i }}" { default = }

{% endfor -%}
'''
    elif tpl == "var_with_description":
        var_template = '''
{% for i in variables -%}
variable "{{ i }}" { description = "" }

{% endfor -%}
    '''
    elif tpl == "var_with_description_and_default":
        var_template = '''
{% for i in variables -%}
variable "{{ i }}" {
  default = 
  description = ""
}

{% endfor -%}
'''
    elif tpl == "empty":
        var_template = '''
{% for i in variables -%}
variable "{{ i }}" {}

{% endfor -%}
'''
    return var_template

def help():
    try:
        sys.argv.index("--help")
        print("""
        Uso: python tfvg.py --help
        --template TEMPLATE_OPTION: Nombre de la template de jinja para generar el fichero de variables.tf. Si no se indica coge la template por defecto.
        --retemplate: Borra el fichero actual de variables.tf y lo vuelve a generar a partir del fichero de template que se indique o el por defecto. Se puede usar en conjunto con --template.

        TEMPLATE_OPTION:

           * var_with_default:
                {% for i in variables -%}
                variable "{{ i }}" { default = }

                {% endfor -%}

            * var_with_description:
                {% for i in variables -%}
                variable "{{ i }}" { description = "" }

                {% endfor -%}

            * var_with_description_and_default:
                {% for i in variables -%}
                variable "{{ i }}" {
                  default = 
                  description = ""
                }

                {% endfor -%}

            * empty:
                {% for i in variables -%}
                variable "{{ i }}" {}

                {% endfor -%}
        """,)
        sys.exit(1)
    except ValueError:
        pass

def get_vars():
    normal_var = r'\bvar\.([\w-]+)\b'
    string_var = r'\$\{var\.([\w-]+)\}'
    ternary_var = r'\bvar\.([\w-]+)\s*==\s*\w+\s*\?\s*var\.\w+\s*:\s*\w+'
    all_matches = set()
    filenames = glob.glob('*.tf')
    for file in filenames:
        with open(file=file, encoding='UTF-8', mode='r') as tf:
            tf_file = tf.read()
            normal_var_match = re.findall(normal_var, tf_file)
            string_var_match = re.findall(string_var, tf_file)
            ternary_var_match = re.findall(ternary_var, tf_file)
            all_matches.update(normal_var_match + string_var_match + ternary_var_match)
    return all_matches

def check_var_file():
    if glob.glob('variables.tf') == []:
        with open(file='variables.tf', encoding='UTF-8', mode='w') as var_file:
            var_file.write('')

def check_vars():
    vars = []
    var_file = 'variables.tf'
    with open(file=var_file, encoding='UTF-8', mode='r') as var_file:
        for line in var_file:
            if re.search('variable \"', line):
                vars += [line.split('"')[1]]
    return vars

def clear_vars():
    current_vars = check_vars()
    got_vars = get_vars()
    add_vars = set(got_vars) - set(current_vars)
    add_vars = list(add_vars)
    add_vars.sort()
    return add_vars

def write_vars():
    try:
        var_template = get_template(sys.argv[sys.argv.index("--template") + 1])
    except:
        var_template = get_template("empty")
    # print(var_template)
    try:
        sys.argv.index("--retemplate")
        os.remove("variables.tf")
    except:
        pass
    with open(file='variables.tf', encoding='UTF-8', mode='a') as var_file:
        var_file.write(Template(var_template).render(variables=clear_vars()))

def pretty_output():
    lines = []
    with open(file='variables.tf', encoding='UTF-8', mode='r') as var_file_r:
        for line_r in var_file_r:
            if not line_r.isspace():
                lines += [line_r]
    with open(file='variables.tf', encoding='UTF-8', mode='w') as var_file_w:
        for line in lines:
            var_file_w.write(line)



help()
check_var_file()
check_vars()
clear_vars()
write_vars()
pretty_output()
