LANGUAGES = ['java', 'c', 'c#', 'mono', 'python', 'python2', 'python3', 'php']

SCRIPTS = {
    'java': 'compile_and_run_java',
    'c': 'compile_and_run_c',
    'c#': 'compile_and_run_mono',
    'mono': 'compile_and_run_mono',
    'python': 'run_python2',
    'python2': 'run_python2',
    'python3': 'run_python3',
    'php': 'run_php'
}

BASE_CMD = [
    'docker',
    'run',
    '--rm',
    # '-i',
    # '-t',
    '-v'
]

# docker run --rm -v "$(pwd)":/mnt --workdir /mnt frolvlad/alpine-php ./run_php example.php [|input.tx]
# docker run --rm -v "$(pwd)":/mnt --workdir /mnt frolvlad/alpine-python2 ./run_python2 example2.py [|input.tx]
# docker run --rm -v "$(pwd)":/mnt --workdir /mnt frolvlad/alpine-python3 ./run_python3 example3.py [|input.tx]

# docker run --rm -v "$(pwd)":/mnt --workdir /mnt frolvlad/alpine-gcc ./compile_and_run_c qq.c [|input.tx]
# docker run --rm -v "$(pwd)":/mnt --workdir /mnt frolvlad/alpine-oraclejdk8:slim ./compile_and_run_java Main.java [|input.tx]
# docker run --rm -v "$(pwd)":/mnt --workdir /mnt frolvlad/alpine-mono ./compile_and_run_mono qq.mono [|input.tx]


def calculate_compile_and_execute_command(lang, folder_name, file_name, input_file_name=""):
    if lang.lower() == 'c':
        return calculate_compile_and_execute_c_command(folder_name, file_name, input_file_name)
    elif lang.lower() == 'java':
        return calculate_compile_and_execute_java_command(folder_name, file_name, input_file_name)
    elif lang.lower() == 'c#' or lang.lower() == 'mono':
        return calculate_compile_and_execute_cs_command(folder_name, file_name, input_file_name)
    elif lang.lower() == 'python2':
        return calculate_compile_and_execute_python2_command(folder_name, file_name, input_file_name)
    elif lang.lower() == 'python3' or lang.lower() == 'python':
        return calculate_compile_and_execute_python3_command(folder_name, file_name, input_file_name)
    elif lang.lower() == 'php':
        return calculate_compile_and_execute_php_command(folder_name, file_name, input_file_name)


def calculate_compile_and_execute_c_command(folder_name, file_name, input_file_name):
    return BASE_CMD + [
        folder_name + ':/mnt',
        "--workdir",
        "/mnt",
        'frolvlad/alpine-gcc',
        "./compile_and_run_c",
        file_name,
        input_file_name
    ]


def calculate_compile_and_execute_java_command(folder_name, file_name, input_file_name):
    return BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "frolvlad/alpine-oraclejdk8:slim",
        "./compile_and_run_java",
        file_name,
        input_file_name
    ]


def calculate_compile_and_execute_cs_command(folder_name, file_name, input_file_name):
    return BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "frolvlad/alpine-mono",
        "./compile_and_run_mono",
        file_name,
        input_file_name
    ]


def calculate_compile_and_execute_python2_command(folder_name, file_name, input_file_name):
    return BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "frolvlad/alpine-python2",
        "./run_python2",
        file_name,
        input_file_name
    ]


def calculate_compile_and_execute_python3_command(folder_name, file_name, input_file_name):
    return BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "frolvlad/alpine-python3",
        "./run_python3",
        file_name,
        input_file_name
    ]


def calculate_compile_and_execute_php_command(folder_name, file_name, input_file_name):
    return BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "frolvlad/alpine-php",
        "./run_php",
        file_name,
        input_file_name
    ]
