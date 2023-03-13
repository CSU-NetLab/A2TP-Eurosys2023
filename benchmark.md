# Benchmark
## Set Up
The experiment needs a Barefoot Wedge 100BF-32X programmable switch and 11 servers. All servers are connected to the switch with 100Gbps links. There are 2 jobs, each of which has 4 workers and 1 PS (Parameter Server). They share 1 aggregating switch. 
To successfully install the NIC driver, you need to use the adapted version of OS kernel. 
Ubuntu 20.04 with Linux 5.4.0-26-generic is feasible to install the NIC driver. Note that configuring 4 workers per job is not necessary. If you don't have enough machines, you can reduce the number of workers for any job.

## Experiment Steps
### Compile P4 program
```
$ cd ~/bf-sde-8.9.1/pkgsrc/p4-build
$ ./configure --prefix=$SDE_INSTALL --with-tofino P4_NAME=p4ml2 P4_PATH=/root/bf-sde-8.9.1/pkgsrc/p4-examples/programs/p4ml2/p4ml2.p4 --enable-thrift
$ make
$ make install
```
```
$ cd ~/bf-sde-8.9.1/pkgsrc/p4-examples
$ ./configure --prefix=$SDE_INSTALL 
$ make
$ make install
```


### Compile worker and parameter server
```
$ cd $A2TP/client/
$ make
```
```
$ cd $A2TP/server/
$ make
```


### Run switch program, configure ports, and install table entries
```
$ cd $SDE
$ ./run_switchd.sh -p p4ml2  (Terminal1)
```
```
$ $SDE/run_p4_tests.sh -t $A2TP/ptf_p4ml2/ -p p4ml2 (Terminal2)
```
```
$ $TOOLS/run_pd_rpc.py -p p4ml2 $A2TP/run_pd_rpc/setupp4ml2.py (Terminal3)
```

### Run server of job A and job B
```
$ #Usage: ./app [AppID]
$ sudo ./app 1
$ sudo ./app 2
```
After running successfully, the server will wait for the sender to start.

### Generate background traffic
Choose one of the workers as the sender and any idle server as the receiver. Then, use the following command to generate UDP background traffic. 
This step simply simulates the bandwidth contention in the large distributed machine learning clusters.
```
$ iperf -c [destination ip] -B [local ip] -u -l 50000 -t 90 -i 1 -b 10G -P 8
```


### Run nth worker of job A and mth worker of job B
```
$ #Usage: ./app [workerID] [Num of Worker] [AppID] [Num of PS]
$ sudo ./app n 4 1 1
$ sudo ./app m 4 2 1
```
If the step is successful, the terminal will print the throughput in each terminal. 

### Expected result

The aggregation throughput and aggregator occupancy will be printed in the terminal. Moreover, the results can be redirected to a file, and then you can use the shell to deal with the data. We collect the files of sample data from this basic experiment, and you can run "./dealdata.sh" command to generate a result.csv file, which includes the real-time aggregation throughput and aggregator occupancy of job A and job B.
The expected result is that the straggling job only occupies a small number of aggregators, relinquishing the aggregators for the non-straggling job, 
so that the non-straggling job still maintains a high aggregation throughput (about 50Gbps in our environment). 
However, the job with severe straggling can still utilize PS for aggregation, so the overall aggregation throughput is improved.
