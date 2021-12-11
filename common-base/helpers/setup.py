from setuptools import setup

setup(
	name='application-images-helpers',
	version='0.0.0',
	description='Helper functionality for the Dockerfiles in the application-images repository',
	url='http://github.com/adamrehn/application-images',
	author='Adam Rehn',
	author_email='adam@adamrehn.com',
	license='MIT',
	packages=['application_images_helpers', 'application_images_helpers.common', 'application_images_helpers.tools'],
	zip_safe=True,
	python_requires = '>=3.7',
	install_requires = [
		'packaging>=19.1',
		'setuptools>=38.6.0',
		'termcolor>=1.1.0',
		'wheel>=0.31.0'
	],
	entry_points = {
		'console_scripts': [
			'generate-application-entrypoint=application_images_helpers.tools:generate_application_entrypoint',
			'wine-reg-add=application_images_helpers.tools:wine_reg_add'
		]
	}
)
