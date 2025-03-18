from setuptools import setup, find_packages

setup(
    name="signal_untangler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'signal-untangler=signal_untangler.main:main',
        ],
        'gui_scripts': [
            'signal-untangler-gui=signal_untangler_gui.app:launch_gui',
        ],
    },
)

