from gemini.runtimes.util import find_runtime, detect_runtime


def run(runtime_key=None):

    if runtime_key is None:
        runtime_key = detect_runtime()

    runtime = find_runtime(runtime_key)

    version = runtime.get_database_version()
    print(f'Got version: {version}')

    print(f'Setting version: {version}')
    runtime.set_database_version(version)
