from transformers import AutoModel
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
        raise ValueError(f'{results["error"]}')


def foo(in_queue, out_queue, timeout):
    print(os.getpid())
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

    model = AutoModel.from_pretrained("hf-internal-testing/test_dynamic_model", trust_remote_code=True)
    # Test model can be reloaded.
    with tempfile.TemporaryDirectory() as tmp_dir:
        model.save_pretrained(tmp_dir)
        #try:
        reloaded_model = AutoModel.from_pretrained(tmp_dir, trust_remote_code=True)
        #except Exception as e:
        #    # import pdb; pdb.set_trace()
        #    print(e)


if __name__ == "__main__":
    timeout = os.environ.get("PYTEST_TIMEOUT", 10)
    timeout = int(timeout)
    for i in range(200):
        time.sleep(1)
        print(i)
        foo2()
        print("=" * 80)
