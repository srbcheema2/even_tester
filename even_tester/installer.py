import os
import subprocess

from srblib import Colour
from srblib import abs_path
from srblib import verify_folder
from srblib import get_os_name

def _get_supported_distros(dependency_map):
    supported_distros = set()
    for rules in dependency_map.values():
        for key in rules.keys():
            supported_distros.add(key)
    return supported_distros

def _recognise_distro(distros=['ubuntu']):
    os_name = get_os_name()
    if os_name in ['windows', 'mac']:
        if os_name in distros: return os_name
        else: return None

    try:
        p = subprocess.Popen(['uname','-a'], stdout=subprocess.PIPE)
        out = p.stdout.read().decode('utf-8').lower()
        for d in distros:
            if d in out:
                return d
        return None
    except:
        return None


def is_installed(soft):
    os_name = get_os_name()
    dump_out =' > /dev/null 2>&1'
    if os_name == 'windows': dump_out =' > NUL'
    help_opt = ' --help '
    a = os.system(soft + help_opt + dump_out)
    if a == 0 or a == 256:
        '''
        0 means return 0
        256 means return 1, generally for those who dont have --help
        if command not found it will return 32512
        '''
        return True
    return False


def install_dependencies(dependency_map, verbose = False):
    supported_distros = _get_supported_distros(dependency_map)
    distro = _recognise_distro(supported_distros)
    if(verbose):
        if(not distro):
            Colour.print('unrecognised distro, please contact srbcheema2@gmail.com for support', Colour.RED)
        else:
            Colour.print('Distro detected to be '+distro+' based',Colour.GREEN)

    all_installed = True

    for d in dependency_map.keys():
        if is_installed(d):
            continue
        rules = dependency_map[d]
        if distro and distro in rules.keys():
            Colour.print('installing '+d+' dependency',Colour.GREEN)
            os.system(rules[distro])
            if not is_installed(d):
                Colour.print('please install ' +d+ ' dependency manually',Colour.YELLOW)
                Colour.print('try command : '+rules[distro],Colour.YELLOW)
                all_installed = False
        else:
            Colour.print('Please install ' +d+' dependency manually',Colour.YELLOW)
            all_installed = False

    return all_installed

def install_tester():
    os_name = get_os_name()

    pwd = str(os.getcwd())#always return without / at end;
    pwd = abs_path(pwd)
    binary_path = pwd + '/even_tester/binaries/'+os_name+'/even_validator'
    if(os_name == 'windows'): binary_path += '.exe'

    if(os_name == 'windows'):
        install_path = abs_path('~/programs','\\')
        binary_path = abs_path(binary_path,'\\')

        user_path = os.environ['path'] + ';'
        if not install_path+';' in user_path:
            print('adding to userpath')
            print(install_path)
            print(user_path)
            os.system('setx path "%path%;'+install_path+'"')
    else:
        install_path = abs_path('~/.local/bin')
    verify_folder(install_path)

    dependency_map = {
        'even_validator':{
            'ubuntu':'cp '+binary_path+' '+install_path,
            'windows':'copy "'+binary_path+'" "'+install_path+'"',
        },
    }
    install_dependencies(dependency_map,verbose=True)

if __name__ == '__main__':
    install_tester()
