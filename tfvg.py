import glob
import re
from jinja2 import Template
import sys
import os

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
    variables = []
    clean_vars = []
    filenames = glob.glob('*.tf')
    for file in filenames:
        with open(file=file, encoding='UTF-8', mode='r') as tf:
            for line in tf:
                if re.search('var\..*', line):
                    if not re.search('\${', line):
                        variables += [line.replace(',','').strip().split('.')[1]]
                    if re.search('\${', line):
                        variables += re.findall('var\.\w+\}', line)
    for vars in variables:
        clean_vars += [vars.replace('var.', '').replace('}','')]
    clean_vars = list(set(clean_vars))
    return clean_vars

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
    return list(add_vars)

def write_vars():
    try:
        var_template = get_template(sys.argv[sys.argv.index("--template") + 1])
    except:
        var_template = get_template("empty")
    # print(var_template)
    try:
        sys.argv.index("--retemplate")
        os.remove("variables.tf")
        with open(file='variables.tf', encoding='UTF-8', mode='a') as var_file:
            var_file.write(Template(var_template).render(variables=clear_vars()))
    except:
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
