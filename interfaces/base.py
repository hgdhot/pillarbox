import re
import json


def initialize(app):
    """initialize view functions

    firstly reads interfaces schema from interfaces.isd
    then writes all view functions into a single file
    and binds view functions with flask app
    """
    with open('interfaces.isd', 'r', encoding='utf-8') as f:

        # writes all code need to be compiled into a file
        with open('interfaces/views.py', 'w+', encoding='utf-8') as w:
            # the suffix number of generated view function
            func_no = 0
            while True:
                # get the request method
                req_method = f.readline().replace('\n', '')
                if req_method.startswith('#'):
                    continue
                if req_method == '':
                    break
                # get the request url
                req_url = f.readline()
                req_url = req_url.replace('\n', '').replace("{", '<').replace('}', '>')
                req_param = re.findall(r"<\w+>", req_url)

                while True:
                    l = f.readline()
                    if l.find('resp=') != -1:
                        break
                resp = l.replace('resp=', '').replace('\n', '')
                # print(resp)
                a = json.loads(resp)
                print('dd', a)

                # remove angle brackets
                param_str = [param[1: -1] for param in req_param]
                if req_method in ['GET', 'POST', 'PUT', 'PATCH']:
                    output_lines = []
                    s = "@app.route('%s', methods=['%s'])\n" % (req_url, req_method)
                    output_lines.append(s)
                    s = "def view%s(%s):\n" % (func_no, ', '.join(param_str))
                    output_lines.append(s)
                    s = "\treturn '%s', 200, {'Content-Type': 'application/json; charset=utf-8'}\n\n" % resp
                    output_lines.append(s)
                    w.writelines(output_lines)
                # elif req_method == 'POST':
                #     output_lines = []
                #     s = "@app.route('%s', methods=['%s'])\n" % (req_url, req_method)
                #     output_lines.append(s)
                #     s = "def view%s(%s):\n" % (func_no, ', '.join(param_str))
                #     output_lines.append(s)
                #     s = "\treturn '%s', 200, {'Content-Type': 'application/json; charset=utf-8'}\n\n" % resp
                #     output_lines.append(s)
                #     w.writelines(output_lines)
                # elif req_method == 'PUT':
                #     output_lines = []
                #     s = "@app.route('%s', methods=['%s'])\n" % (req_url, req_method)
                #     output_lines.append(s)
                #     s = "def view%s(%s):\n" % (func_no, ', '.join(param_str))
                #     output_lines.append(s)
                #     s = "\treturn '%s', 200, {'Content-Type': 'application/json; charset=utf-8'}\n\n" % resp
                #     output_lines.append(s)
                #     w.writelines(output_lines)
                # skip the empty line
                f.readline()
                func_no += 1

        with open('interfaces/views.py', 'r', encoding='utf-8') as func_file:
            func_shema = func_file.read()
            code = compile(func_shema, '', 'exec')
            # execute the code stored in the code object
            exec(code, {'app': app})
