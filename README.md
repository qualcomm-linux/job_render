# Job Render

This Python script is designed to generate job definitions for LAVA (Linaro Automated Validation Architecture) jobs. 
It leverages the Jinja Templating engine to dynamically inject data into templates, creating customized job definitions. 

# Branches

**main:** Primary development branch. Contributors should develop submissions based on this branch, and submit pull requests to this branch.

# Requirements

Install python3 in your system
    - use command `python --version` to ensure the proper installation of python in your system.

# Installation Instructions

Clone the Repository:
```
git clone https://github.com/qualcomm-linux/job_render.git
cd job_render
```
# Usage

- Set environment variables (BOOT_METHOD, TARGET, TARGET_DTB) in your shell before running the script using the export command.
Example:
```
export BOOT_METHOD="fastboot"
export TARGET="qcs6490"
export TARGET_DTB="qcs6490-rb3gen2"
```
- To run the script use command. `python3 lava_Job_definition_generator.py --localjson "path_to_json_file"`

# License

job_render is licensed under the [*BSD-3-clause-clear License*](https://spdx.org/licenses/BSD-3-Clause-Clear.html). See [*LICENSE*](https://github.com/qualcomm-linux/job_render/blob/main/LICENSE) for the full license text.

