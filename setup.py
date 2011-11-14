from setuptools import setup

setup(
    name="xhttpnode",
    version="0.1.0",
    author="Jeronimo Jose Albi",
    description="Node server that processes XHTTP requests",
    license="BSD",
    install_requires=[
        "simplejson",
        "WebOb",
    ],
    url="https://github.com/jeronimoalbi/xhttp-node",
    keywords="xhttp web wsgi protocol",
    zip_safe=True,
    include_package_data=True,
    test_suite="tests",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

