
from setuptools import setup

setup(
        name='eusela',
        description='an email schedule queue and pop-up prompter',
        version='0.0.1',
	data_files = [('/usr/local/share/man/man1/', ['docs/man/paana.1/'])],
	long_description='An email schedule queue and pop-up prompter designed to replace crontab in \
	giving schedules for important email, and follow-ups. It should have it\'s own prompter that opens up \
	neomutt with the desired email and its attachemnts if any.',
        py_modules=['main', 'lib'],
        author='Luew Lawlan Leminkainen',
        install_requires=[
            'Click',
	    'apscheduler',
        'rich',
        'pretty_errors',
            'ipython'],
        entry_points={
            'console_scripts': [
                'paana = main:cli' ],
            },  
        )   

