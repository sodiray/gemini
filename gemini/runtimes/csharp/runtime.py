import os
import re
import subprocess

from gemini.runtimes import util
from gemini.core.util import find, regex_find, template


version_pattern = re.compile("const string version = \"([a-z0-9]{8}|root)\"")
parent_pattern = re.compile("const string parent = \"([a-z0-9]{8})\"")
name_pattern = re.compile("const string name = \"(.+?)\"")

def get_database_version():

    script_template = '''#load "{{script_location}}"
var ver = GetDatabaseVersion();
Console.WriteLine($"VERSION={ver}");

    '''

    get_version_script = template(script_template, {
        'script_location': os.path.join(os.getcwd(), 'geminiver.csx')
    })

    cmd = ["dotnet-script", "eval", get_version_script]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()

    return regex_find(str(out), re.compile("VERSION=([a-z0-9]{8}|root)"))

def set_database_version(version):

    script_template = '''#load "{{script_location}}"
SetDatabaseVersion("{{version}}");
    '''

    set_version_script = template(script_template, {
        'script_location': os.path.join(os.getcwd(), 'geminiver.csx'),
        'version': version
    })

    cmd = ["dotnet-script", "eval", set_version_script]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()

def get_migrations():

    migration_files = util.read_migration_files('./migrations')

    def map_script_to_migration_obj(script):
        return {
            'version': regex_find(script, version_pattern),
            'parent': regex_find(script, parent_pattern),
            'name': regex_find(script, name_pattern)
        }

    return list(map(map_script_to_migration_obj, migration_files))

def run_down(migration_id):

    file_name = find(util.list_migration_files(), lambda f: migration_id in f)
    file_location = os.path.join(os.getcwd(), 'migrations', file_name)

    script_template = '''#load "{{file_location}}"
Down()
    '''

    down_script = template(script_template, {
        'file_location': file_location
    })

    subprocess.run(["dotnet-script", "eval", down_script])

def run_up(migration_id):

    file_name = find(util.list_migration_files(), lambda f: migration_id in f)
    file_location = os.path.join(os.getcwd(), 'migrations', file_name)

    script_template = '''#load "{{file_location}}"
Up()
    '''

    up_script = template(script_template, {
        'file_location': file_location
    })

    subprocess.run(["dotnet-script", "eval", up_script])

def create_migration(new_version, parent, name):
    # create a new file in the migrations directory
    # that is a template for the current runtime and version

    file_name = f'{new_version}_{name}.csx'

    parent = f'"{parent}"' if parent is not None else 'null'

    script_template = '''

const string version = "{{new_version}}";
const string parent = {{parent}};
const string name = "{{name}}";

public static void Up()
{
    Console.WriteLine("Running up migration");
}

public static void Down()
{
    Console.WriteLine("Running down migration");
}

    '''

    file_content = template(script_template, {
        'new_version': new_version,
        'parent': parent,
        'name': name
    })

    curr_dir_path = os.getcwd()
    file_location = os.path.join(curr_dir_path, 'migrations', file_name)

    with open(file_location, "w") as file:
        file.write(file_content)

def setup():
    # Run whatever script needed to install csharp specific runtime
    # dependencies - dotnet-script, dotnet, etc.
    print('Installing dependencies for C# Gemini')
    pass
