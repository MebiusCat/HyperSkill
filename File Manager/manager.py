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


# run the user's program in our generated folders
os.chdir('module/root_folder')

print('Input the command')
user_path = os.getcwd()
while True:
    user_command = input()
    if user_command == 'pwd':
        # print("Hi, pwd!")
        print(user_path)
    elif user_command[:2] == 'cd':
        # put your code here
        # print("Hi!")
        try:
            _command, _argument = user_command.split(' ', 1)
            user_path = cd_processing(user_path, _argument)
        except:
            print('Invalid command')

    elif user_command == 'quit':
        break
    else:
        print('Invalid command')
