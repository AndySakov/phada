from setuptools import setup

setup(
   name='phada abraham',
   version='1.0',
   description='Personal Website',
   author='Abolo Samuel',
   author_email='ikabolo59@gmail.com',
   packages=['phadaabraham'],  #same as name
   install_requires=['gunicorn', 'flask', 'numpy', 'pymysql', 'pandas'], #external packages as dependencies
)
