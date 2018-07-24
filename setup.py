from setuptools import setup

setup(name="zookeeper_exporter",
	version="0.1.0",
	description="Zoopkeeper prometheus exporter",
	author="Hiroaki Kawai",
	author_email="hiroaki.kawai@gmail.com",
	url="https://github.com/hkwi/zookeeper_exporter",
	py_modules = ["zookeeper_exporter"],
	entry_points={
		"console_scripts": [
			"zookeeper_exporter:cli"
		]
	},
	install_requires=["flask"]
)