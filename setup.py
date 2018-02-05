import os

from setuptools import find_packages, setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-slackchat-serializer',
    version='0.0.1',
    packages=find_packages(exclude=('example',)),
    include_package_data=True,
    license='',
    description='A Django app that serializes conversations in Slack and can notify a custom renderer.',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'djangorestframework',
        'markdown',
        'markslack',
        'slackclient',
        'django-rest-swagger',
        'emoji',
        'slacker',
        'celery',
    ]
)
