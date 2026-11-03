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
Supported `BOOT_METHOD` values: `fastboot`, `u-boot`, `efi`, `flasher`.
When using `BOOT_METHOD=efi` or `BOOT_METHOD=flasher`, set `FLASH_IMAGE` (required) and optionally `FLASH_PORT`.
For `BOOT_METHOD=flasher`, pass `--meta-qcom` to enable the `auto_login` block (login prompt `login:`, user `root`).
Example:
```
export BOOT_METHOD="fastboot"
export TARGET="qcs6490"
export TARGET_DTB="qcs6490-rb3gen2"
```
- To run the script use command. `python3 lava_Job_definition_generator.py --localjson "path_to_json_file"`

### fastboot images and kselftest

With `BOOT_METHOD=fastboot`, `FASTBOOT_IMAGE` selects the image built by the postprocess step:
- `boot` (default): a `boot.img` made with `mkbootimg`, loaded with `fastboot boot`.
- `bootfs`: a SpacemiT `bootfs.ext4` (kernel, ramdisk, dtb and `env_k3.txt`), flashed to the `bootfs` partition with `fastboot flash`.

In both cases the job boots with `method: fastboot`; how the device starts the OS comes from its device dictionary (`fastboot_sequence`, or the `pre_os_command` running `fastboot continue` on SpacemiT K3).

`TEST_METHOD=kselftest` adds the build's modules and kselftest archives to the ramdisk (kselftest in `/opt/kselftests/mainline/`) and runs the collections listed in `KSELFTEST_COLLECTIONS` with the Linaro [test-definitions](https://github.com/linaro/test-definitions) kselftest runner, as KernelCI kselftest jobs do. Every kselftest result is reported as a LAVA test case.

Other variables:
- `ARCH`: architecture of the default ramdisk used when the build has no ramdisk artifact (default `arm64`): the KernelCI Debian `trixie-kselftest` rootfs for `TEST_METHOD=kselftest`, the KernelCI buildroot rootfs otherwise.
- `KSELFTEST_COLLECTIONS`: space separated kselftest collections (default `riscv clone3 core signal kcmp size sync cachestat fchmodat2 tmpfs`).
- `TARGET_DTB`: for non-qcom dtbs, prefix the vendor directory, e.g. `spacemit/k3-pico-itx`.

Example (SpacemiT K3 Pico-ITX):
```
export BOOT_METHOD="fastboot"
export FASTBOOT_IMAGE="bootfs"
export TARGET="k3-pico-itx"
export TARGET_DTB="spacemit/k3-pico-itx"
export ARCH="riscv"
export TEST_METHOD="kselftest"
export KSELFTEST_COLLECTIONS="riscv core signal"
python3 lava_Job_definition_generator.py --node <kbuild node id>
```

# License

job_render is licensed under the [*BSD-3-clause-clear License*](https://spdx.org/licenses/BSD-3-Clause-Clear.html). See [*LICENSE*](https://github.com/qualcomm-linux/job_render/blob/main/LICENSE) for the full license text.
