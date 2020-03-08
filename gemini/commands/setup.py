from gemini.runtimes.util import find_runtime


def run(runtime):

    runtime = find_runtime(runtime)

    runtime.setup()
