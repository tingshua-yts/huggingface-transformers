import pdb, multiprocessing, time, traceback, tempfile, os


def run_test_in_subprocess(target_func, inputs=None, timeout=600):
    start_methohd = "spawn"
    ctx = multiprocessing.get_context(start_methohd)

    input_queue = ctx.Queue(1)
    output_queue = ctx.JoinableQueue(1)

    # We can't send `unittest.TestCase` to the child, otherwise we get issues regarding pickle.
    input_queue.put(inputs, timeout=timeout)

    process = ctx.Process(target=target_func, args=(input_queue, output_queue, timeout))
    process.start()
    # Kill the child process if we can't get outputs from it in time: otherwise, the hanging subprocess prevents
    # the test to exit properly.
    try:
        results = output_queue.get(timeout=timeout)
        output_queue.task_done()
    except Exception as e:
        process.terminate()
        raise ValueError(f'{str(e)}')
    process.join(timeout=timeout)

    if results["error"] is not None:
        print(f'{results["error"]}')
        with open("output.txt", "a+") as fp:
            fp.write(results["error"] + "\n")


def foo(in_queue, out_queue, timeout):

    print(os.getpid())
    with open("output.txt", "a+") as fp:
        fp.write(str(os.getpid()) + "\n")

    error = None
    try:
        _ = in_queue.get(timeout=timeout)
        foo2()
    except Exception:
        error = f"{traceback.format_exc()}"

    results = {"error": error}
    out_queue.put(results, timeout=timeout)
    out_queue.join()


def foo2():
    from transformers import AutoModel

    model = AutoModel.from_pretrained("hf-internal-testing/test_dynamic_model", trust_remote_code=True)
    # Test model can be reloaded.
    with tempfile.TemporaryDirectory() as tmp_dir:
        model.save_pretrained(tmp_dir)
        reloaded_model = AutoModel.from_pretrained(tmp_dir, trust_remote_code=True)


if __name__ == "__main__":
    timeout = os.environ.get("PYTEST_TIMEOUT", 10)
    timeout = int(timeout)
    for i in range(200):
        time.sleep(2)
        print(i)
        with open("output.txt", "a+") as fp:
            fp.write(str(i) + "\n")
        try:
            os.system('rm -rf "/home/circleci/.cache/huggingface/modules/transformers_modules/"')
        except:
            pass
        try:
            os.system('rm -rf "/home/huggingface/.cache/huggingface/modules/"')
        except:
            pass
        run_test_in_subprocess(target_func=foo, inputs=None)
        print("=" * 80)
        with open("output.txt", "a+") as fp:
            fp.write("=" * 80 + "\n")


# /home/circleci/.pyenv/versions/3.7.12/lib/python3.7/site-packages/transformers/dynamic_module_utils.py
