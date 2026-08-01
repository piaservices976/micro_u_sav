from setuptools import find_packages, setup

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="micro_u_sav",
    version="0.0.1",
    description="Fonctions SAV MICRO-U (facturation des pieces detachees) pour ERPNext.",
    author="PIA Services",
    author_email="contact@piaservices.fr",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
