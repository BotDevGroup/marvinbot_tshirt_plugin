from distutils.core import setup
from setuptools import find_packages

# apt-get install libtiff5-dev libjpeg-dev zlib1g-dev libfreetype6-dev

REQUIREMENTS = [
    'marvinbot','pillow'
]

setup(name='marvinbot-tshirt-plugin',
      version='0.1',
      description='T-Shirt Generator',
      author='Conrado Reyes',
      author_email='coreyes@gmail.com',
      url='',
      packages=[
        'marvinbot_tshirt_plugin',
      ],
      package_dir={
        'marvinbot_tshirt_plugin':'marvinbot_tshirt_plugin'
      },
      zip_safe=False,
      include_package_data=True,
      package_data={'': ['*.ini']},
      install_requires=REQUIREMENTS,
      dependency_links=[
          'git+ssh://git@github.com:BotDevGroup/marvin.git#egg=marvinbot',
      ],
)
