import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytone",
    version="0.0.1",
    author="Rein Gundersen Bentdal",
    author_email="rein.bent@gmail.com",
    description="MIDI processing environment in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ReinBentdal/pytone",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "colorama",
        "simpleaudio",
        "python-rtmidi",
        "mido",
        "pynput",
    ],
    include_package_data=True,
)
