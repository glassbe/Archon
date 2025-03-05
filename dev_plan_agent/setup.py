from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="dev_plan_agent",
    version="0.1.0",
    author="Benedikt Glass",
    author_email="example@example.com",
    description="Ein Agent, der einen detaillierten Entwicklungsplan für Softwareprojekte erstellt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glassbe/Archon",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "dev-plan-agent=dev_plan_agent.run_mcp:main",
        ],
    },
)
