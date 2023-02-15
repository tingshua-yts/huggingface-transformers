import time, traceback, tempfile, os
from transformers.utils import HF_MODULES_CACHE


def foo2():
    from transformers import AutoModel

    model = AutoModel.from_pretrained("hf-internal-testing/test_dynamic_model", trust_remote_code=True)
    # Test model can be reloaded.
    with tempfile.TemporaryDirectory() as tmp_dir:
        model.save_pretrained(tmp_dir)
        try:
            reloaded_model = AutoModel.from_pretrained(tmp_dir, trust_remote_code=True)
        except Exception as e:
            print(e)
            with open("output.txt", "a+") as fp:
                fp.write(f"{traceback.format_exc()}" + "\n")


if __name__ == "__main__":
    timeout = os.environ.get("PYTEST_TIMEOUT", 10)
    timeout = int(timeout)
    for i in range(1):
        time.sleep(2)
        print(i)
        with open("output.txt", "a+") as fp:
            fp.write(str(i) + "\n")
        try:
            os.system(f'rm -rf "{HF_MODULES_CACHE}"')
        except:
            pass
        foo2()
        print("=" * 80)
        with open("output.txt", "a+") as fp:
            fp.write("=" * 80 + "\n")


# /home/circleci/.pyenv/versions/3.7.12/lib/python3.7/site-packages/transformers/dynamic_module_utils.py
# /home/circleci/.pyenv/versions/3.7.12/lib/python3.7/site-packages/transformers/models/auto/configuration_auto.py
# /home/circleci/.pyenv/versions/3.7.12/lib/python3.7/site-packages/transformers/models/auto/auto_factory.py
# /home/circleci/.pyenv/versions/3.7.12/lib/python3.7/site-packages/transformers/models/auto/auto_factory.py


# os.system('ls -l "/home/huggingface/.cache/huggingface/"')
# os.system('ls -l "/home/huggingface/.cache/huggingface/modules/"')
# os.system('ls -l "/home/huggingface/.cache/huggingface/modules/transformers_modules"')
# os.system('ls -l "/home/huggingface/.cache/huggingface/modules/transformers_modules/__pycache__"')
# os.system('ls -l "/home/huggingface/.cache/huggingface/modules/transformers_modules/local"')
# os.system('ls -l "/home/huggingface/.cache/huggingface/modules/transformers_modules/local/__pycache__"')
#
#
# os.system('ls -l "/home/huggingface/.cache/huggingface/modules/transformers_modules/__pycache__"')
# os.system('rm -rf "/home/huggingface/.cache/huggingface/modules/transformers_modules/__pycache__/__init__.cpython-38.pyc"')
# os.system('rm -rf "/home/huggingface/.cache/huggingface/modules/transformers_modules/__pycache__"')
#
# os.system('rm -rf "/home/huggingface/.cache/huggingface/modules/transformers_modules/local/__pycache__/configuration.cpython-38.pyc"')
#
# # this is the way to go
# os.system('rm -rf "/home/huggingface/.cache/huggingface/modules/transformers_modules/local/__pycache__"')
#
#
# os.system('rm -rf "/home/huggingface/.cache/huggingface/modules/transformers_modules/local/configuration.py"')