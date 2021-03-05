import os

from setuptools import find_packages, setup

scripts = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin"))
script_paths = [os.path.join("bin", script) for script in scripts]

setup(
    name="ymca_automated_registrar",
    version=0.1,
    description="Scripted tooling for automated registration of event slots",
    url="https://github.com/myz540/ymca-automated-registrar",
    packages=find_packages(),
    scripts=script_paths,
    author="Mike Zhong",
    zip_safe=False,
    install_requires=[
        "selenium==3.141.0",
        "pytz==2020.4"
        "pyautogui==0.9.52"

    ],
)
