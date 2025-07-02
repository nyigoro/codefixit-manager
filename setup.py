from setuptools import setup, find_packages

setup(
    name="codefixit-manager",
    version="1.0.3",
    description="Modernize and auto-refactor legacy code using rule-based fixers.",
    author="Nyigoro",
    author_email="nyigoro@gmail.com",
    url="https://github.com/nyigoro/codefixit-manager",
    packages=find_packages(include=["cfm", "cfm.*"]),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "cfm = cfm.cli:main"
        ]
    },
    install_requires=[
        "openai>=1.0.0",  # Optional, for rule-gen
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
