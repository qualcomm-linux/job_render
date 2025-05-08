#this is the file to generate job definition
from data_validation.validate_data import Validator
from Handlers.templateHandler import TemplateHandler
from Handlers.argParseHandler import ArgParseHandler
from Handlers.dataHandler import DataHandler
from utils.path_url_identifier import is_url, is_local_path, extract_directory_name, extract_file_name
import json
import sys
import logging
import os
from datetime import datetime

# extracting configuration
boot_method = os.environ.get("BOOT_METHOD")
name = os.environ.get("TARGET")
target_dtb = os.environ.get("TARGET_DTB")
brarch = 'arm64'


# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')


# Generate a unique log file name based on the current timestamp
log_filename = datetime.now().strftime('logs/log_%Y%m%d_%H%M%S.log')


# Configure the logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_filename), logging.StreamHandler()])


platform_config = {
    'boot_method': boot_method,
    'name': name
}
# Example test method
test_method = 'baseline'
testList_path = 'testList.json'
test_names = None
test_details_json_path = testList_path if os.path.exists(testList_path) else None

print(test_details_json_path)
### Extracting all data from cli and using argparse
test_data = None
if test_details_json_path is not None:
    with open(test_details_json_path, 'r') as file:
        test_data = json.load(file)
    logging.debug('Loaded test data from %s', test_details_json_path)
else:
    logging.debug('Didn\'t find any testList(If you have testList please provide correct path), definition will be created without test block.')

if test_data is not None:
    test_names = test_data[0]['contents']
arg_parse_handler = ArgParseHandler(test_data=test_data)

# Storing node and tree values in variables
node_value = arg_parse_handler.get_node_id()
tree_value = arg_parse_handler.get_tree_value()
is_buildurl_provided = arg_parse_handler.get_buildurl()
local_json_path = arg_parse_handler.get_local_json_path()
template_path = arg_parse_handler.get_template_path()

### Error Handling for more than one arguments for json passing (options: build_url, node_id, localjson)
class ConflictError(Exception):
    pass

non_none_args = sum(arg is not None for arg in [node_value, is_buildurl_provided, local_json_path])

try:
    if non_none_args>1:
        raise ConflictError("ConflictError: Provide either build_url (for Qualcomm internal serval JSON value URL) or node_id (to fetch from Maestro Server) or local json path, or neither to fetch the latest node from Maestro Server.")
except ConflictError as e:
    logging.error(e)
    print(e)
    sys.exit(1)

### plaform_config and test_method data validation
config_validator = Validator(platform_config, test_method)
config_validator.perform_validations_and_proceed()
logging.debug('Platform config and test method validated')

### Load the template
template_handler=None
template=None
if template_path is not None:
    if template_path.startswith(('/', '\\')):
        raise ValueError("template_path must be relative to the project directory, not an absolute path.")
    elif template_path.startswith(('./','.\\')):
        template_path = template_path[2:]

if template_path is not None:
    if is_url(template_path):
        template_handler = TemplateHandler()
        template = template_handler.get_template(template_name=template_path)
    elif is_local_path(template_path):
        template_handler = TemplateHandler(extract_directory_name(template_path))
        template = template_handler.get_template(template_name=extract_file_name(template_path))
    else:
        logging.error("Either local path or web URL is wrong")
        print("Either local path or web url is wrong")
        sys.exit(1)
else:
    template_handler = TemplateHandler('templates')
    template = template_handler.get_template('lava_job_template.jinja2')
logging.info('Template loaded successfully')
print('Template loaded successfully')

###building url and getting node data
data_handler = DataHandler(node_value=arg_parse_handler.get_node_id(), tree_value=arg_parse_handler.get_tree_value(), build_url_main=arg_parse_handler.get_buildurl(), local_json_path=local_json_path)
data_handler.fetch_data()

### logging details
data_handler.log_details()

# # Extracting dtb url
data_handler.fetch_and_update_dtb(target_dtb)

# ### Injecting tests into the definition
if test_data is not None:
    data_handler.put_tests_into_fetched_data(test_names=test_names, arg_parse_handler=arg_parse_handler, test_data=test_data)

### Render the template with dynamic data
node_data = data_handler.get_fetched_data()
job_definition = template_handler.render_template(template, node=data_handler.get_fetched_data(), platform_config=platform_config, test_method=test_method, tests_count=data_handler.get_count_of_tests(),device_dtb = node_data['artifacts']['dtb'],brarch=brarch)

# Parse the rendered YAML and Save the rendered job definition
template_handler.save_rendered_template(job_definition, os.path.join('renders','lava_job_definition.yaml'))