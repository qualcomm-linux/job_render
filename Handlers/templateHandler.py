# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause-Clear

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, Template
import yaml, requests
import logging
from urllib.parse import urlparse


class TemplateHandler:
    def __init__(self, template_dir=None):
        if template_dir or template_dir=="":
            self.env = Environment(loader=FileSystemLoader(template_dir))
        logging.debug('Initializing TemplateHandler with template_dir: %s', template_dir)

    def get_template(self, template_name):
        try:
            #checking if template_name is a url or Local path
            result = urlparse(template_name)
            if all([result.scheme, result.netloc]):
                response = requests.get(template_name)
                logging.debug('Fetching template from URL: %s', template_name)
                print("weblink for template: ",template_name)
                if response.status_code == 200:
                    logging.debug('Successfully fetched template from URL')
                    return Template(response.text)
                else:
                    logging.error('Failed to download the template. Status code: %d', response.status_code)
                    print("Failed to download the template.")
                    return None
            else:
                logging.debug('Fetching template from local path: %s', template_name)
                return self.env.get_template(template_name)
        except TemplateNotFound:
            logging.error('Template file not found at the given path: %s', template_name)
            print("Template file not found at the given path.")
            return None
        except Exception as e:
            logging.error('An error occurred in get_template: %s', e)
            print(f"An error occurred in get_template: {e}")
            return None

    def render_template(self, template, **kwargs):
        try:
            logging.debug('Rendering template with arguments: %s', kwargs)
            return template.render(**kwargs)
        except Exception as e:
            logging.error('An error occurred during rendering: %s', e)
            print(f"An error occurred during rendering: {e}")
            return None

    def save_rendered_template(self, rendered_content, output_path):
        try:
            # Parse the rendered YAML
            yaml_content = yaml.safe_load(rendered_content)
            logging.debug('Parsed rendered content into YAML')
            # Save the rendered job definition
            with open(output_path, 'w') as f:
                yaml.dump(yaml_content, f, default_flow_style=False)
            print("Job definition created successfully!")
            logging.debug('Job definition created successfully at: %s', output_path)
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")
            logging.error('An error occurred while saving the file: %s', e)