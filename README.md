# JCOIN Stigma Surveys Data Packaging

Schemas and files containing value labels for each wave were generated from `pyreadstat` module


## Usage

`pip install -r requirements.txt` in a virtual env.
`dvc pull`
Run python files:
`crosswalkxlsx_to_mappings.py` : creates metadata mappings from an excel file that was manually annotated by NORC Stigma Survey team with support/feedback from DASC team.
`translate.py`: uses the source `spss` files and the mappings to generate schemas, data, and metadata.
`package.py`: packages into a data package
