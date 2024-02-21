import os


def cd_processing(_user_path, _argument):
    if _argument == '..':
        _user_path = os.path.dirname(_user_path)
        print(os.path.basename(_user_path))
    else:
        if os.path.isdir(_argument):
            _user_path = os.path.abspath(_argument)
            # print(os.path.basename(_user_path))
            print(_user_path)
        elif os.path.isdir(_user_path + '/' + _argument):
            _user_path = _user_path + '/' + _argument
            print(_user_path)
        else:
            # print(_user_path + '/' + _argument)
            # print(_user_path, _argument)
            print('Invalid command')
    return _user_path


def convert_size(size):
    m_size = size
    if m_size < 1024:
        return f'{m_size}B'
    m_size //= 1024
    if m_size < 1024:
        return f'{m_size}KB'
    m_size //= 1024
    if m_size < 1024:
        return f'{m_size}MB'
    m_size //= 1024
    return f'{m_size}GB'


# run the user's program in our generated folders
os.chdir('module/root_folder')

print('Input the command')
user_path = os.getcwd()
while True:
    user_command = input().split(' ', 1)
    if user_command[0] == 'pwd':
        # print("Hi, pwd!")
        print(user_path)
    elif user_command[0] == 'cd':
        try:
            _command, _argument = user_command[0], user_command[1]
            user_path = cd_processing(user_path, _argument)
        except:
            print('Invalid command')
    elif user_command[0] == 'ls':
        ls_arg = None
        if len(user_command) > 1:
            ls_arg = user_command[1]

        _list = os.listdir(user_path)
        sub_dir = []
        sub_files = []
        for elem in _list:
            long_name = user_path + '/' + elem
            if os.path.isdir(long_name):
                sub_dir.append(elem)
            else:
                sub_files.append(elem)

        for elem in sub_dir:
            print(elem)

        for elem in sub_files:
            if ls_arg == '-l':
                long_name = user_path + '/' + elem
                print(elem, os.stat(long_name).st_size)
            elif ls_arg == '-lh':
                long_name = user_path + '/' + elem
                print(elem,
                      convert_size(os.stat(long_name).st_size))
            else:
                print(elem)
    elif user_command[0] == 'quit':
        break
    else:
        print('Invalid command')
