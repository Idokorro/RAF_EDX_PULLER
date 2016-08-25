LANGUAGES = ['Java', 'C', 'C#']

BASE_CMD = [
    '/usr/local/bin/docker',
    'run',
    '--rm',
    '-v'
]


def calculate_compile_command(lang, folder_name, file_name):
    if lang == 'C':
        return calculate_compile_c_command(folder_name, file_name)
    elif lang == 'Java':
        return calculate_compile_java_command(folder_name, file_name)
    elif lang == 'C#':
        return calculate_compile_cs_command(folder_name, file_name)

def calculate_compile_c_command(folder_name, file_name):
    return BASE_CMD + [
        folder_name + ':/tmp',
        'frolvlad/alpine-gcc',
        'gcc',
        '--static',
        '/tmp/' + file_name,
        '-o',
        '/tmp/qq'
    ]

def calculate_compile_java_command(folder_name, file_name):
    return BASE_CMD + [
        folder_name + ":/mnt",
        "--workdir",
        "/mnt",
        "frolvlad/alpine-oraclejdk8:slim",
        "sh",
        "-c",
        "'javac " + file_name + " && java " + file_name[:-5] + "'"
    ]

def calculate_compile_cs_command(folder_name, file_name):
    return BASE_CMD

def calculate_run_command(lang, folder_name, file_name):
    if lang == 'C':
        return calculate_run_c_command(folder_name, file_name)
    elif lang == 'Java':
        return calculate_run_java_command(folder_name, file_name)
    elif lang == 'C#':
        return calculate_run_cs_command(folder_name, file_name)

def calculate_run_c_command(folder_name, file_name):
    return [folder_name+'/qq']

def calculate_run_java_command(folder_name, file_name):
    return []

def calculate_run_cs_command(folder_name, file_name):
    return []