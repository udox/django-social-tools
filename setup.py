import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-social-tools',
    version='0.1',
    packages=['socialtool'],
    include_package_data=True,
    install_requires=[
          'django>=1.5.7,<1.7',
          'pillow>=1.7.8,<2.5',
          'South>=0.7.6,<0.9',
	  'python-dateutil==2.2',
	  'djangorestframework==2.3.10',
	  'python-instagram==0.8.0',
	  'requests==2.1.0',
	  'requests-oauthlib==0.4.0',
	  'simplejson==3.3.1',
    ],
    dependency_links = ['http://github.com/udox/python-twitter.git@master#egg=python-twitter'],
    license='BSD License',  # example license
    description='Django app that scrapes social posts from instagram and twitter.',
    long_description=README,
    url='http://www.example.com/',
    author='Your Name',
    author_email='yourname@example.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
