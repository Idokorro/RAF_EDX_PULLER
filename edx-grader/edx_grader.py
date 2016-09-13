import time, logging, json, urllib, os
import settings, urls, xqueue_util as util

log = logging.getLogger(__name__)

QUEUE_NAME = settings.QUEUE_NAME

CURRENT_FOLDER = os.path.abspath(os.path.dirname(__file__))
GRADER_ROOT = os.path.join(os.path.dirname(CURRENT_FOLDER), "grader")
SUBMISSIONS_ROOT = os.path.join(GRADER_ROOT, "submissions")

def each_cycle():
    print('[*]Logging in to xqueue')
    session = util.xqueue_login()
    success_length, queue_length = get_queue_length(QUEUE_NAME, session)

    if success_length and queue_length > 0:

        success_get, queue_item = get_from_queue(QUEUE_NAME, session)
        success_parse, content = util.parse_xobject(queue_item, QUEUE_NAME)

        if success_get and success_parse:

            content_header = json.loads(content['xqueue_header'])
            content_body = json.loads(content['xqueue_body'])

            # Calling grader
            correct, score, msg = grade_submission(content_header, content_body)

            xqueue_header, xqueue_body = util.create_xqueue_header_and_body(content_header['submission_id'], content_header['submission_key'], correct, score, msg, 'reference_dummy_grader')
            (success, msg) = util.post_results_to_xqueue(session, json.dumps(xqueue_header), json.dumps(xqueue_body))
            if success:
                print("successfully posted result back to xqueue")


def get_from_queue(queue_name, xqueue_session):
    """ Get a single submission from xqueue """
    try:
        success, response = util._http_get(xqueue_session, urllib.parse.urljoin(settings.XQUEUE_INTERFACE['url'], urls.XqueueURLs.get_submission), {'queue_name': queue_name})
    except Exception as err:
        return False, "Error getting response: {0}".format(err)

    return success, response


def get_queue_length(queue_name, xqueue_session):
    """ Returns the length of the queue """
    try:
        success, response = util._http_get(xqueue_session, urllib.parse.urljoin(settings.XQUEUE_INTERFACE['url'], urls.XqueueURLs.get_queuelen), {'queue_name': queue_name})
        if not success:
            return False, "Invalid return code in reply"
    except Exception as e:
        log.critical("Unable to get queue length: {0}".format(e))
        return False, "Unable to get queue length."

    return True, response

def grade_submission(content_header, content_body):
    from grader.grader import test_code
    from grader.working_directory import WorkingDirectory
    grader_payload = json.loads(content_body['grader_payload'])
    grader_url = urllib.request.urlopen("http://" + grader_payload['tester'])

    language = grader_payload['lang']
    grader_code = grader_url.read().decode("utf-8")
    submission_code = content_body['student_response']

    result = test_code(language, grader_code, submission_code)

    return True, 1, "<p>Correct</p>"


# def run_external_grader(content_header, content_body):
#     grader_payload = json.loads(content_body['grader_payload'])
#     path = os.path.join(SUBMISSIONS_ROOT, content_header['submission_key'])
#     os.makedirs(path)
#
#     # GRADER
#     grader_url = urllib.request.urlopen("http://" + grader_payload['tester'])
#     grader_file_path = os.path.join(path, 'Grader.py')
#     with open(grader_file_path, 'wb') as f:
#         f.write(grader_url.read())
#     f.close()
#     grader_url.close()
#
#     # SUBMISSION
#     student_response_file_path = os.path.join(path, 'Submission' + EXTENSIONS[grader_payload['lang']])
#     with open(student_response_file_path, 'w') as f:
#         f.write(content_body['student_response'])
#     f.close()
#
#     # EXECUTE
#     results = grader.test_solution(grader_payload['lang'], grader_file_path, student_response_file_path)
#
#     return calculate_correction(results)
#
#
# def calculate_correction(results):
#     for result in results["results"]:
#         if not result["success"]:
#             return False, 0, "<p><emph>" + result["error_message"] + "</emph></p>" + "<p>" + result[
#                 "traceback"] + "</p>"
#     return True, 1, "<p><emph>Uspešno ste rešili problem. Čestitamo!</emph></p>"


try:
    logging.basicConfig()
    while True:
        each_cycle()
        time.sleep(2)
except KeyboardInterrupt:
    print('^C received, shutting down')

