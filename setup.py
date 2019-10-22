from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pybrief',
      version='1.0.1',
      description="""PyBRIEF is a small blog system (and more cause it's
modular) written in python with django""",
      long_description=readme(),
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Framework :: Django :: 1.7'],
      keywords='django blog bookmarks',
      url='https://github.com/bougie/pybrief',
      author='David Hymonnet',
      author_email='bougie@appartland.eu',
      license='BSD',
      packages=['pybrief'],
      install_requires=['django==1.11.23'],
      include_package_data=True,
      zip_safe=False)
