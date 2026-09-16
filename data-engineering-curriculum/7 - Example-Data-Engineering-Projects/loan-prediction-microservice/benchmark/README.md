

## Benchmarking the Service

There are two points to benchmark in this demo
1. The HTTPS API (FastAPI)
2. The Inference Server (RedisAI)

### Benchmarking the HTTPS API

For this we used [wrk](https://github.com/wg/wrk) which can be installed through
brew or built manually with GCC.

```bash
# for mac
brew install wrk

# for everything else
git clone https://github.com/wg/wrk
cd wrk && make
```

Then to run the benchmark, a LUA script is included that will send an example
payload to the service. You can use it by running

```bash
./wrk http://127.0.0.1:8877/v1/loan/predict -s /path/to/the/wrk-script.lua -t 4
```

### Benchmarking the Inference Server (RedisAI)

The importance of benchmarking the inference server itself is to see
how much the HTTPS server impacts the overall performance of the system.

In order to mimic the exact Python client call the HTTPS makes, one can use
the ``redis-benchmark`` tool that comes with most installations of Redis through
apt/yum/brew/etc as follows

```bash
eval redis-benchmark --threads 4 -c 50 -P 1 -n 10000 "AI.DAGEXECUTE PERSIST 2 out_1_7832417532154898461 out_2_7832417532154898461 \|\> AI.SCRIPTEXECUTE get_loan_features enrich_features KEYS 2 19510613_1349 12542 ARGS 5 29 100000 3 10000000 7.2 OUTPUTS 1 model_input \|\> AI.MODELEXECUTE loan_model INPUTS 1 model_input OUTPUTS 2 out_1_7832417532154898461 out_2_7832417532154898461"
```

This looks a little ugly but it'll give a good performance profile.


### Ways these benchmarks can be Improved

1. Use a Go HTTPS server and the Go RedisAI client
2. Separate the FastAPI server and Redis server on different compute instances
3. Add more CPUs (and hence workers) to the FastAPI server
4. Add more FastAPI server instances and put them behind a load balancer
5. Optimize the XGBoost model further (not done at all here)
