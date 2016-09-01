import time
import logging
import json
import urllib
import urllib3
import xqueue_util as util
import settings
import project_urls
import os
import datetime
import subprocess
import signal


log = logging.getLogger(__name__)

QUEUE_NAME = settings.QUEUE_NAME

GRADER_ROOT = '/root/PycharmProjects/RAF_EDX/grader'

EXTENSIONS = {
    'java': '.java',
    'c': '.c',
    'c#': '.mono',
    'mono': '.mono',
    'python': '.py',
    'python2': '.py',
    'python3': '.py',
    'php': '.php'
}


def each_cycle():
    print('[*]Logging in to xqueue')
    session = util.xqueue_login()
    success_length, queue_length = get_queue_length(QUEUE_NAME, session)
    if success_length and queue_length > 0:
        success_get, queue_item = get_from_queue(QUEUE_NAME, session)
        print(queue_item)
        success_parse, content = util.parse_xobject(queue_item, QUEUE_NAME)
        if success_get and success_parse:
            grade(content)
            content_header = json.loads(content['xqueue_header'])
            content_body = json.loads(content['xqueue_body'])
            grader_payload = json.loads(content_body['grader_payload'])


            # Calling grader
            grader_status, grader_stdout, grader_stderr = run_external_grader(content_header, content_body, grader_payload)


            xqueue_header, xqueue_body = util.create_xqueue_header_and_body(content_header['submission_id'], content_header['submission_key'], True, 1, '<p><emph>Good Job!</emph></p>', 'reference_dummy_grader')
            (success, msg) = util.post_results_to_xqueue(session, json.dumps(xqueue_header), json.dumps(xqueue_body))
            if success:
                print("successfully posted result back to xqueue")


def microseconds_passed(time_delta):
    return time_delta.microseconds + time_delta.seconds * 10**6


def grade(content):
    print(content)
    body = json.loads(content['xqueue_body'])
    student_info = json.loads(body.get('student_info', '{}'))
    email = student_info.get('student_email', '')
    print("submitted by email: " + email)
    files = json.loads(content['xqueue_files'])
    for (filename, fileurl) in files.items():
        response = urllib3.urlopen(fileurl)
        with open(filename, 'w') as f:
            f.write(response.read())
        f.close()
        response.close()


def get_from_queue(queue_name,xqueue_session):
    """
        Get a single submission from xqueue
        """
    try:
        success, response = util._http_get(xqueue_session,
                                           urllib.parse.urljoin(settings.XQUEUE_INTERFACE['url'], project_urls.XqueueURLs.get_submission),
                                           {'queue_name': queue_name})
    except Exception as err:
        return False, "Error getting response: {0}".format(err)
    
    return success, response


def get_queue_length(queue_name,xqueue_session):
    """
        Returns the length of the queue
        """
    try:
        success, response = util._http_get(xqueue_session,
                                           urllib.parse.urljoin(settings.XQUEUE_INTERFACE['url'], project_urls.XqueueURLs.get_queuelen),
                                           {'queue_name': queue_name})
        
        if not success:
            return False,"Invalid return code in reply"
    
    except Exception as e:
        log.critical("Unable to get queue length: {0}".format(e))
        return False, "Unable to get queue length."
    
    return True, response


def run_external_grader(content_header, content_body, grader_payload):
    student_response_file_path = GRADER_ROOT + '/examples/' + content_header['submission_key'] + EXTENSIONS[grader_payload['lang'].lower()]

    student_response_file = open(student_response_file_path, 'w')
    student_response_file.write(content_body['student_response'])
    student_response_file.close()

    grader_command = [
        'python3.5',
        GRADER_ROOT + '/__main__.py',
        grader_payload['lang'],
        GRADER_ROOT + '/examples/' + grader_payload['tester'],
        student_response_file_path
    ]

    start = datetime.datetime.now()
    timeout = 10

    subproc = subprocess.Popen(
        grader_command,
        cwd=os.getcwd(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    reached_timeout = False
    while subproc.poll() is None:
        time.sleep(0.02)
        now = datetime.datetime.now()
        if microseconds_passed(now - start) >= timeout * 10**6:
            subproc.kill()
            os.kill(subproc.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            reached_timeout = True
            break

    os.remove(student_response_file_path)

    subproc_stdout = subproc.stdout.read()
    subproc_stderr = subproc.stderr.read()
    subproc_stdout = subproc_stdout.decode('utf-8')
    subproc_stderr = subproc_stderr.decode('utf-8')
    subproc_status = subproc.returncode

    return subproc_status, subproc_stdout, subproc_stderr


try:
    logging.basicConfig()
    while True:
        each_cycle()
        time.sleep(2)
except KeyboardInterrupt:
    print('^C received, shutting down')