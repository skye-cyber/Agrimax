import os
import subprocess

from colorama import Fore, Style, init
from setuptools import find_packages, setup

# Initialize colorama
init(autoreset=True)

# Define color constants
RESET = Style.RESET_ALL

# POSIX color definitions
if os.name == "posix":
    RED, DRED, FRED, IRED, LRED, URED = (
        '\033[91m', '\033[1;91m', '\033[2;91m', '\033[3;91m', '\033[4;91m', '\033[5;91m')
    GREEN, DGREEN, FGREEN, IGREEN, LGREEN, UGREEN = (
        '\033[92m', '\033[1;92m', '\033[2;92m', '\033[3;92m', '\033[4;92m', '\033[5;92m')
    YELLOW, DYELLOW, FYELLOW, IYELLOW, LYELLOW, UYELLOW = (
        '\033[93m', '\033[1;93m', '\033[2;93m', '\033[3;93m', '\033[4;93m', '\033[5;93m')
    BLUE, DBLUE, FBLUE, IBLUE, LBLUE, UBLUE = (
        '\033[94m', '\033[1;94m', '\033[2;94m', '\033[3;94m', '\033[4;94m', '\033[5;94m')
    MAGENTA, DMAGENTA, FMAGENTA, IMAGENTA, LMAGENTA, UMAGENTA = (
        '\033[95m', '\033[1;95m', '\033[2;95m', '\033[3;95m', '\033[4;95m', '\033[5;95m')
    CYAN, DCYAN, ICYAN, FCYAN, LCYAN, UCYAN = (
        '\033[96m', '\033[1;96m', '\033[2;96m', '\033[3;96m', '\033[4;96m', '\033[5;96m')
    BWHITE, BBWHITE, WHITE, DWHITE, FWHITE, IWHITE, LWHITE, UWHITE = (
        '\033[1m', '\033[5;97;1m', '\033[97m', '\033[1;97m', '\033[2;97m', '\033[3;97m', '\033[4;97m', '\033[5;97m')

# Windows color definitions
elif os.name == "nt":
    RED, DRED, FRED, IRED, LRED, URED = (
        Fore.LIGHTRED_EX, Fore.RED, Fore.RED, Fore.RED, Fore.LIGHTRED_EX, Fore.RED)
    GREEN, DGREEN, FGREEN, IGREEN, LGREEN, UGREEN = (
        Fore.LIGHTGREEN_EX, Fore.GREEN, Fore.GREEN, Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.GREEN)
    YELLOW, DYELLOW, FYELLOW, IYELLOW, LYELLOW, UYELLOW = (
        Fore.LIGHTYELLOW_EX, Fore.YELLOW, Fore.YELLOW, Fore.YELLOW, Fore.LIGHTYELLOW_EX, Fore.YELLOW)
    BLUE, DBLUE, FBLUE, IBLUE, LBLUE, UBLUE = (
        Fore.LIGHTBLUE_EX, Fore.BLUE, Fore.BLUE, Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.BLUE)
    MAGENTA, DMAGENTA, FMAGENTA, IMAGENTA, LMAGENTA, UMAGENTA = (
        Fore.LIGHTMAGENTA_EX, Fore.MAGENTA, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.LIGHTMAGENTA_EX, Fore.MAGENTA)
    CYAN, DCYAN, ICYAN, FCYAN, LCYAN, UCYAN = (
        Fore.LIGHTCYAN_EX, Fore.CYAN, Fore.BLUE, Fore.CYAN, Fore.LIGHTCYAN_EX, Fore.CYAN)
    BWHITE, BBWHITE, WHITE, DWHITE, FWHITE, IWHITE, LWHITE, UWHITE = (
        Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE)

# ASCII Art Logo
logo = """
                     _ __  __
     /\             (_)  \/  |
    /  \   __ _ _ __ _| \  / | __ ___  __
   / /\ \ / _` | '__| | |\/| |/ _` \ \/ /
  / ____ \ (_| | |  | | |  | | (_| |>  <
 /_/    \_\__, |_|  |_|_|  |_|\__,_/_/\_\
           __/ |
          |___/
"""
"""

"""
# Package requirements
python_requires = ">=3.6"
use_requires = [
    'django',
    'matplotlib',
    'requests',
    'numpy',
    'pandas',
    'seaborn',
    'base64',
    'geopy'
]

# Platform-specific dependencies
linux_requires = [
    # Add any Linux-specific dependencies here
]

windows_requires = [
    # Add any Windows-specific dependencies here
]


def _clone_repo(repo_url):
    """Clone the Django app repository."""
    try:
        print(f"{GREEN}Cloning repository from {repo_url}...{RESET}")
        subprocess.run(['git', 'clone', repo_url], check=True)
        repo_dir = os.path.basename(repo_url).rsplit('.', 1)[0]
        os.chdir(repo_dir)
        print(
            f"{DGREEN}Repository cloned successfully! Navigated to {repo_dir} directory.{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{DRED}Failed to clone repository: {e}{RESET}")
        exit(1)
    except Exception as e:
        print(f"{DRED}An error occurred: {e}{RESET}")
        exit(1)


def _info():
    """Display required packages and prompt user to install them."""
    print(f"{YELLOW}The following packages are required in order to run this project:{RESET}")
    for req in use_requires:
        print(f"{BWHITE}{req}{RESET}")

    req_install = input(
        f"{BLUE}Please press {YELLOW}`Enter`{BLUE} to install them now!⏲️{RESET}")
    if req_install.lower() in ('yes', 'y', 'okay', 'ok', ''):
        print(f"{DMAGENTA}{'_'*30}Begin install{'_'*30}{RESET}")
        installer()
    else:
        print(f"{RED}Exit!{RESET}")
        exit(1)


def installer():
    """Install required packages."""
    try:
        python_version = subprocess.run(
            ['python', '-V'], stdout=subprocess.PIPE, text=True).stdout[7:].strip()
        print(f"{GREEN}Python Version = {DCYAN}{python_version}{RESET}")
        if python_version.startswith("3"):
            print(f"{DYELLOW}Python 3 is recommended{RESET}")

        # Install platform-specific dependencies
        if os.name == "posix":
            for req in linux_requires:
                print(f"{GREEN}Installing Linux-specific {req}...{RESET}")
                subprocess.run(
                    ['python', '-m', 'pip', 'install', req], check=True)
        elif os.name == "nt":
            for req in windows_requires:
                print(f"{GREEN}Installing Windows-specific {req}...{RESET}")
                subprocess.run(
                    ['python', '-m', 'pip', 'install', req], check=True)

        # Install general dependencies
        for req in use_requires:
            print(f"{GREEN}Installing {req}...{RESET}")
            subprocess.run(['python', '-m', 'pip', 'install', req], check=True)

        print(f"{DGREEN}Done{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{DRED}Failed to install package: {e}{RESET}")
        exit(1)
    except Exception as e:
        print(f"{DRED}An error occurred: {e}{RESET}")
        exit(1)


def _set():
    """Set up the project database."""
    try:
        print(f"{BLUE}SET UP PROJECT DB{RESET}")
        subprocess.run(['python', 'manage.py', 'makemigrations'], check=True)
        subprocess.run(['python', 'manage.py', 'migrate'], check=True)
        print(f"{GREEN}ALL SET, Run `{DCYAN}python manage.py runserver{RESET}` to start your project{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{DRED}Failed to set up the database: {e}{RESET}")
        exit(1)
    except Exception as e:
        print(f"{DRED}An error occurred: {e}{RESET}")
        exit(1)


def main():
    try:
        print(logo)
        print(
            f"{DMAGENTA}{'_'*30}Welcome to the AgriMax Django Project Setup!{'_'*30}{RESET}")
        repo_url = "https://github.com/skye-cyber/AgriMax.git"
        clone_setup = input(
            f"{BLUE}Do you need to clone the AgriMax project from a Git repository? (yes/no){RESET}: ")
        if clone_setup.lower() in ('yes', 'y'):
            _clone_repo(repo_url)
        else:
            print(f"{YELLOW}Skipping repository cloning.{RESET}")

        # Check if the user wants to create a virtual environment
        venv_setup = input(
            f"{BLUE}Do you want to create a virtual environment? (yes/no){RESET}: ")
        if venv_setup.lower() in ('yes', 'y'):
            venv_dir = input(
                f"{BLUE}Enter the directory name for the virtual environment [venv]: {RESET}") or "venv"
            print(f"{GREEN}Creating virtual environment in {venv_dir}...{RESET}")
            subprocess.run(['python', '-m', 'venv', venv_dir], check=True)
            print(
                f"{DGREEN}Virtual environment created successfully in {venv_dir}.{RESET}")

            # Activate the virtual environment
            if os.name == "posix":
                activate_script = os.path.join(venv_dir, 'bin', 'activate')
            elif os.name == "nt":
                activate_script = os.path.join(venv_dir, 'Scripts', 'activate')
            print(f"{GREEN}Activating virtual environment...{RESET}")
            activate_command = f"source {activate_script}" if os.name == "posix" else activate_script
            print(
                f"{DGREEN}Run the following command to activate the virtual environment:\n{RESET}{activate_command}")

            # Ask the user to activate the virtual environment
            activate_now = input(
                f"{BLUE}Do you want to activate the virtual environment now? (yes/no){RESET}: ")
            if activate_now.lower() in ('yes', 'y'):
                print(
                    f"{YELLOW}Please run the following command in your terminal:\n{RESET}{activate_command}")

        _info()
        _set()
    except KeyboardInterrupt:
        print(f"{RED}Interrupted! Exiting...{RESET}")
        exit(1)


if __name__ == "__main__":
    main()
