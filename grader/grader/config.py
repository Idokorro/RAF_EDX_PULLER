LANGUAGES = ['java', 'c', 'c#', 'mono', 'python', 'python2', 'python3', 'php']

BASE_CMD = [
    'docker',
    'run',
    '--rm',
    '-v'
]

# docker run --rm frolvlad/alpine-php php example.php
# docker run --rm frolvlad/alpine-python2 python2 example2.py
# docker run --rm frolvlad/alpine-python3 python3 example3.py

# docker run --rm -v "$(pwd)":/tmp frolvlad/alpine-gcc gcc --static /tmp/qq.c -o /tmp/qq
# docker run --rm -v "$(pwd)":/mnt --workdir /mnt frolvlad/alpine-oraclejdk8:slim sh -c "javac Main.java && java Main"
# docker run --rm -v "$(pwd)":/mnt frolvlad/alpine-mono sh -c "mcs -out:/mnt/qq.exe /mnt/qq.mono && mono /mnt/qq.exe"


def calculate_compile_and_execute_command(lang, folder_name, file_name):
    if lang.lower() == 'c':
        return calculate_compile_and_execute_c_command(folder_name, file_name)
    elif lang.lower() == 'java':
        return calculate_compile_and_execute_java_command(folder_name, file_name)
    elif lang.lower() == 'c#' or lang.lower() == 'mono':
        return calculate_compile_and_execute_cs_command(folder_name, file_name)
    elif lang.lower() == 'python2':
        return calculate_compile_and_execute_python2_command(folder_name, file_name)
    elif lang.lower() == 'python3' or lang.lower() == 'python':
        return calculate_compile_and_execute_python3_command(folder_name, file_name)
    elif lang.lower() == 'php':
        return calculate_compile_and_execute_php_command(folder_name, file_name)


def calculate_compile_and_execute_c_command(folder_name, file_name):
    return BASE_CMD + [
        folder_name + ':/tmp',
        'frolvlad/alpine-gcc',
        'gcc',
        '--static',
        '/tmp/' + file_name,
        '-o',
        '/tmp/qq'
    ]


def calculate_compile_and_execute_java_command(folder_name, file_name):
    return BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "frolvlad/alpine-oraclejdk8:slim",
        "sh",
        "-c",
        "'javac " + file_name + " && java " + file_name[:-5] + "'"
    ]


def calculate_compile_and_execute_cs_command(folder_name, file_name):
    return BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "frolvlad/alpine-mono",
        "sh",
        "-c",
        "'mcs -out:" + file_name[:-5] + ".exe " + file_name + " && mono " + file_name[:-5] + ".exe '"
    ]


def calculate_compile_and_execute_python2_command(folder_name, file_name):
    return BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "frolvlad/alpine-python2",
        file_name
    ]


def calculate_compile_and_execute_python3_command(folder_name, file_name):
    return BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "frolvlad/alpine-python3",
        file_name
    ]


def calculate_compile_and_execute_php_command(folder_name, file_name):
    return BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "frolvlad/alpine-php",
        file_name
    ]
