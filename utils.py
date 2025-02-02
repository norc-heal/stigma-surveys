import contextlib
from pathlib import Path
import os
import hashlib
from dataforge.frictionless.utils import write_stata_script

@contextlib.contextmanager
def _chdir(path):
    """Context manager to change and restore working directory."""

    d = os.getcwd()
    os.chdir(path)

    try:
        yield
    finally:
        os.chdir(d)

def write_data_package(package, path=None):
    """Write data package with stata script"""

    if not path:
        path = Path('tmp') / package.name
    else:
        path = Path(path)

    # Change to data package directory to avoid error when setting rsrc.schema
    os.makedirs(path, exist_ok=True)
    with _chdir(path):

        os.makedirs('data', exist_ok=True)
        os.makedirs('scripts', exist_ok=True)
        os.makedirs('schemas', exist_ok=True)

        for rsrc in package.resources:
            rsrc.schema.to_json(Path('schemas') / f'{rsrc.name}.json')
            rsrc.schema = f'schemas/{rsrc.name}.json'
            rsrc.data.to_csv(Path('data') / f'{rsrc.name}.csv')
            if not rsrc.path:
                rsrc.path = f'data/{rsrc.name}.csv'
            rsrc.format = 'csv'
            rsrc.encoding = 'utf-8'
            rsrc.bytes = os.stat(rsrc.path).st_size
            rsrc.mediatype = "text/csv"
            rsrc.hash = hashlib.md5(open(rsrc.path,'rb').read()).hexdigest()
            write_stata_script(rsrc, path=Path('scripts') / f'{rsrc.name}.do',
                               value_labels=rsrc.value_labels,
                               vl_from_enum=False, version=package.version,
                               fld_list=([f for f in rsrc.data.index.names if f is not None]
                                         + rsrc.data.columns.to_list()))
            rsrc.data = None

        package.to_json('datapackage.json')

def drop_excluded_fields(schema, df):
    """Drop fields marked as 'exclude_from_release' from schema and df"""

    fields_to_drop = [f.name for f in schema.fields if f.to_dict().get('custom', {}).
                      get('jcoin', {}).get('exclude_from_release', False)]
    for field in fields_to_drop:
        schema.remove_field(field)
    df.drop(columns=fields_to_drop, inplace=True)

    return


