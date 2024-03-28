"""Are you kidding me?"""
import math
import os
import shutil

# determine root directory
# run the user's program in our generated folders
# synth perfect

os.chdir('module/root_folder')


def cmd_pwd():

    """Print the name of current folder"""

    return os.getcwd()


def cmd_cd():

    """Allow change current directory"""

    try:
        os.chdir(command[3:])
        return cmd_pwd()
    except FileNotFoundError:
        return 'Invalid command'


def humanize_size(size):

    """Return size of file in humanreadable format"""

    base = 1024
    sizes = ['B', 'KB', 'MB', 'GB']
    deg = int(min(math.log(size, base), 3))
    return f'{size // base ** deg}{sizes[deg]}'


def get_size(st_size, is_file):

    """Return size of file in requested format"""

    if not args or not is_file:
        return ''
    if args[0] == '-l':
        return f' {st_size}'
    if args[0] == 'lh':
        return f' {humanize_size(st_size)}'
    return ''


def cmd_ls():

    """Show list of folders/files in requested directory"""

    files: list[os.DirEntry] = list(os.scandir())
    files.sort(key=lambda x: not x.is_dir())
    return '\n'.join(
        file.name + get_size(file.stat().st_size, file.is_file())
        for file in files
    )


def cmd_mv():

    """Move files or directory to another place"""

    if len(args) != 2:
        return 'Specify the current name of the file or directory and the new location and/or name'
    fr, to = args
    if not os.path.isfile(fr) and not os.path.isdir(fr):
        return 'No such file or directory'
    if os.path.isfile(to) or os.path.isdir(to):
        return 'The file or directory already exists'
    shutil.move(fr, to)


def cmd_mkdir():

    """Create directory"""

    if len(args) != 1:
        return 'Specify the name of the directory to be made'
    name = args[0]
    if os.path.isdir(name):
        return 'The directory already exists'
    os.mkdir(name)


def cmd_rm():

    """Removing file or directory"""

    if not args:
        return 'Specify the file or directory'
    name = args[0]
    try:
        if os.path.isfile(name):
            os.remove(name)
        else:
            shutil.rmtree(name)
    except FileNotFoundError:
        return 'No such file or directory'


def cmd_cp():

    """
    Copying files or directories
    """

    if len(args) > 2:
        return 'Specify the current name of the file or directory and the new location and/or name'
    elif len(args) != 2:
        return 'Specify the file'
    fr, to = args
    if not os.path.isdir(fr) and not os.path.isfile(fr):
        return 'No such file or directory'
    try:
        shutil.copy(fr, to)
    except shutil.SameFileError:
        return f'{fr} already exists in this directory'


ACTIONS = {
    'pwd': cmd_pwd, 'cd': cmd_cd, 'ls': cmd_ls,
    'mv': cmd_mv, 'mkdir': cmd_mkdir, 'cp': cmd_cp,
    'rm': cmd_rm,
}

print('Input the command')
while (command := input()) != 'quit':
    cmd, *args = command.split()
    if cmd not in ACTIONS:
        print('Invalid command')
    else:
        if out := ACTIONS.get(cmd)():
            print(out)
