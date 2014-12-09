# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

from setuptools import setup, find_packages


setup(
    name='zeit.content.video',
    version='2.2.10.dev0',
    author='gocept',
    author_email='mail@gocept.com',
    url='https://svn.gocept.com/repos/gocept-int/zeit.content.video',
    description="""\
""",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='gocept proprietary',
    namespace_packages=['zeit', 'zeit.content'],
    install_requires=[
        'gocept.form',
        'gocept.selenium',
        'grokcore.component',
        'lxml',
        'plone.testing',
        'pytz',
        'setuptools',
        'zeit.cms>=2.31.0.dev0',
        'zeit.connector',
        'zeit.solr>=2.2.0.dev0',
        'zope.annotation',
        'zope.app.zcmlfiles',
        'zope.component',
        'zope.dublincore',
        'zope.formlib',
        'zope.interface',
        'zope.schema',
        'zope.traversing',
    ],
)
