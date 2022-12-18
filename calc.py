import json


class Function:
    def __init__(self, name='test', arg='test', command='test', re_var='test'):
        self.name = name
        self.arg = arg
        self.len_arg = len(self.arg)
        self.command = command
        self.len_command = len(self.command)
        self.re_var = re_var
        print('\033[34mDef complete')


class Var:
    def __init__(self, n, x):
        self.name = n
        self.x = float(x)
        print(f'\033[34mSet complete')


class Calc:
    def __init__(self):
        self.result = 0

    def add(self, x, y):
        x, y = float(x), float(y)
        self.result = x + y
        return self.result

    def sub(self, x, y):
        x, y = float(x), float(y)
        self.result = x - y
        return self.result

    def mul(self, x, y):
        x, y = float(x), float(y)
        self.result = x * y
        return self.result

    def div(self, x, y):
        try:
            x, y = float(x), float(y)
            self.result = x / y
            return self.result
        except ZeroDivisionError:
            print(f'U divide by 0')

    def calc(self, f, x1, x2):
        x1_b = str(x1).replace('.', '', 1).isdigit()
        x2_b = str(x2).replace('.', '', 1).isdigit()
        try:
            if f == 'add':
                if not x1_b and not x2_b:
                    self.add(dict_of_var.get(f'{x1}').x, dict_of_var.get(f'{x2}').x)
                elif x1_b and not x2_b:
                    self.add(float(x1), dict_of_var.get(f'{x2}').x)
                elif not x1_b and x2_b:
                    self.add(dict_of_var.get(f'{x1}').x, float(x2))
                    dict_of_var.get(f'{x1}').x = c.result
                elif x1_b and x2_b:
                    self.add(float(x1), float(x2))
            elif f == 'sub':
                if not x1_b and not x2_b:
                    self.sub(dict_of_var.get(f'{x1}').x, dict_of_var.get(f'{x2}').x)
                elif x1_b and not x2_b:
                    self.sub(float(x1), dict_of_var.get(f'{x2}').x)
                elif not x1_b and x2_b:
                    self.sub(dict_of_var.get(f'{x1}').x, float(x2))
                    dict_of_var.get(f'{x1}').x = c.result
                elif x1_b and x2_b:
                    self.sub(float(x1), float(x2))
            elif f == 'mul':
                if not x1_b and not x2_b:
                    self.mul(dict_of_var.get(f'{x1}').x, dict_of_var.get(f'{x2}').x)
                elif x1_b and x2_b:
                    self.mul(float(x1), float(x2))
                elif x1_b and not x2_b:
                    self.mul(float(x1), dict_of_var.get(f'{x2}').x)
                elif not x1_b and x2_b:
                    self.mul(dict_of_var.get(f'{x1}').x, float(x2))
                    dict_of_var.get(f'{x1}').x = c.result
            elif f == 'div':
                if not x1_b and not x2_b:
                    self.div(dict_of_var.get(f'{x1}').x, dict_of_var.get(f'{x2}').x)
                elif x1_b and not x2_b:
                    self.div(float(x1), dict_of_var.get(f'{x2}').x)
                elif not x1_b and x2_b:
                    self.div(dict_of_var.get(f'{x1}').x, float(x2))
                    dict_of_var.get(f'{x1}').x = c.result
                elif x1_b and x2_b:
                    self.div(float(x1), float(x2))
        except AttributeError:
            print('\033[31mThis var (or vars) not exist(s)')
        return self.result

    def call(self, name=None, arg=None, re_var=None):
        t = arg[0].strip()
        if len(arg) == 1:
            arg.append(t)
        for k in range(0, len(dict_of_fun.get(name).command)):
            if dict_of_fun.get(name).command[k][0] in dict_of_fun:
                t = c.call(name=dict_of_fun.get(name).command[k][0], arg=arg,
                           re_var=dict_of_fun.get(dict_of_fun.get(name).command[k][0]).re_var)
            else:
                for i in range(1, len(arg)):
                    var_buffer = arg[i].strip()
                    t = self.calc(f=dict_of_fun.get(name).command[k][0], x1=t, x2=var_buffer)
        dict_of_var[re_var] = Var(re_var, t)
        return dict_of_var.get(f'{re_var}').x


def load(file='data'):
    print('\033[34mLoading...')
    with open(f'{file}.json', 'r') as data_js:
        data = json.load(data_js)
        for key in data['vars']:
            dict_of_var[key] = Var(key, data['vars'][f'{key}'])
        for key in data['funs']:
            dict_of_fun[key] = Function(name=key, arg=data['funs'][key][0], command=data['funs'][key][1],
                                        re_var=data['funs'][key][2])
    print('\033[34mComplete')


def save(file='data'):
    print('\033[34mSaving...')
    data = {
        'vars': {},
        'funs': {}
    }
    for item in dict_of_var:
        data['vars'][f'{item}'] = dict_of_var.get(f'{item}').x
    for item in dict_of_fun:
        data['funs'][f'{item}'] = [dict_of_fun.get(f'{item}').arg, dict_of_fun.get(f'{item}').command,
                                   dict_of_fun.get(f'{item}').re_var]
    with open(f'{file}.json', 'w') as data_js:
        json.dump(data, data_js, indent=3, sort_keys=True)
    print('\033[34mComplete')


dict_of_var = {}
dict_of_fun = {}
lst_of_fun = ['exit', 'set', 'print', 'add', 'sub', 'mul', 'div', 'call', 'def', 'load', 'save']


print('\033[32mPattern:\nDEF func_name: arg_1 ... arg_n: command_1 operand_1 operand_2; ...; RETURN var_name_or_value;')
print('\033[32mFor ex.:\nDEF pow2: x: MUL x x; RETURN x;\nor\nDEF pow3: y: pow2 y; MUL y x; RETURN c;')

s = input('\033[32mReload json? (y/n): ').lower().strip()
if s == 'y':
    print('\033[34mLoading...')
    load()

while True:
    c = Calc()
    s = input('\033[32mInput: ').lower().strip()
    start = s.split()[0]
    if start in lst_of_fun:  # mb create with 's.startswith(tuple(lst_of_fun))'?
        if start == 'exit':
            s = input('\033[32mSave to json? (y/n): ').lower().strip()
            if s == 'y':
                save()
                raise SystemExit('Exit')
            else:
                raise SystemExit('Exit')
        elif start == 'load':
            load(file=s.split()[1])
        elif start == 'save':
            save(file=s.split()[1])

        elif start in ['set', 'print', 'add', 'sub', 'mul', 'div']:
            s = s.split()
            if start == 'set':
                if (not s[1].replace('.', '', 1).isdigit() and s[1] not in dict_of_var) and \
                        (not s[2].replace('.', '', 1).isdigit() and s[2] not in dict_of_var):
                    print(f'\033[31mThis vars not exist')
                elif not s[1].replace('.', '', 1).isdigit() and s[2].replace('.', '', 1).isdigit():
                    dict_of_var[s[1]] = Var(s[1], s[2])
                elif not s[1].replace('.', '', 1).isdigit() and not s[2].replace('.', '', 1).isdigit():
                    if s[1] in dict_of_var:
                        dict_of_var[s[2]] = Var(s[2], dict_of_var.get(f'{s[1]}').x)
                    else:
                        print(f'\033[31mWrong input')
                else:
                    print(f'\033[31mWrong input')
            elif start == 'print':
                try:
                    print(f"\033[34m{dict_of_var.get(f'{s[1]}').name} = {dict_of_var.get(f'{s[1]}').x}")
                except AttributeError:
                    print('\033[31mThis var not exists')
            elif start in ['add', 'sub', 'mul', 'div']:
                print(f'\033[34m{c.calc(s[0], s[1], s[2])}')
        elif start in ['def', 'call']:
            if start == 'def':
                d = {'name': None,
                     'arg': None,
                     'command': None,
                     're_var': None}
                s = s.split(':')
                d['name'] = s[0].split()[1]
                d['arg'] = s[1].strip().split()
                s = s[2].strip().split(';')
                d['re_var'] = s[-2].split()[-1]
                s = s[:-2]
                d['command'] = [i.split() for i in s]

                dict_of_fun[d['name']] = Function(name=d['name'], arg=d['arg'],
                                                  command=d['command'], re_var=d['re_var'])
            elif start == 'call':
                d = {'name': None,
                     'arg': None,
                     're_var': None}
                s = s.split()
                if 'into' in s:
                    d['name'] = s[1]
                    d['arg'] = s[2:-2]
                    d['re_var'] = s[-1]
                elif 'into' not in s:
                    d['name'] = s[1]
                    d['arg'] = s[2:]
                    d['re_var'] = dict_of_fun.get(f'{d["name"]}').re_var
                try:
                    c.call(name=dict_of_fun.get(d['name']).name, arg=d['arg'], re_var=d['re_var'])
                    buff = d['re_var']
                    print(f"\033[34m{dict_of_var.get(f'{buff}').name} = {dict_of_var.get(f'{buff}').x}")
                except TypeError:
                    print('\033[31mOoops')
                except IndexError:
                    print('\033[31mMaybe you forgot input var?')
    else:
        print(f'\033[31mInvalid input')
