import os
import subprocess
import sys
from pyngrok import ngrok, conf

from modules import launch_utils

args = launch_utils.args
python = launch_utils.python
git = launch_utils.git
index_url = launch_utils.index_url
dir_repos = launch_utils.dir_repos

commit_hash = launch_utils.commit_hash
git_tag = launch_utils.git_tag

run = launch_utils.run
is_installed = launch_utils.is_installed
repo_dir = launch_utils.repo_dir

run_pip = launch_utils.run_pip
check_run_python = launch_utils.check_run_python
git_clone = launch_utils.git_clone
git_pull_recursive = launch_utils.git_pull_recursive
list_extensions = launch_utils.list_extensions
run_extension_installer = launch_utils.run_extension_installer
prepare_environment = launch_utils.prepare_environment
configure_for_tests = launch_utils.configure_for_tests
start = launch_utils.start


def main():
    if args.dump_sysinfo:
        filename = launch_utils.dump_sysinfo()

        print(f"Sysinfo saved as {filename}. Exiting...")

        exit(0)

    launch_utils.startup_timer.record("initial startup")

    with launch_utils.startup_timer.subcategory("prepare environment"):
        if not args.skip_prepare_environment:
            prepare_environment()

    if args.test_server:
        configure_for_tests()

    prestart_dir = os.environ.get("PRESTART_DIR", "prestart")
    if not os.path.exists(prestart_dir):
        os.makedirs(prestart_dir)

    python_files = [file for file in os.listdir(prestart_dir) if file.endswith(".py")]
    if python_files:
        for python_file in python_files:
            file_path = os.path.join(prestart_dir, python_file)
            print(f"Executing: {file_path}")
            subprocess.run([sys.executable, file_path])

    ngrok_token = os.environ.get("NGROK")
    if ngrok_token:
        ngrok.kill()
        srv = ngrok.connect(7860, pyngrok_config=conf.PyngrokConfig(auth_token=ngrok_token) , bind_tls=True).public_url
        print(f"\n\nhttps://{srv[8:]}\n\n")

    config_dir = os.environ.get("CONFIG")
    if config_dir:
        config_files = ["styles.csv" ,"ui-config.json" ,"config.json" ,"cache.json"]
        for cfile in config_files:
            cfile_path = os.path.join(config_dir, cfile)
            if os.path.exists(cfile):
                os.remove(cfile)

            if os.path.exists(cfile_path):
                subprocess.run(["ln", cfile_path, cfile])


    start()


if __name__ == "__main__":
    main()
