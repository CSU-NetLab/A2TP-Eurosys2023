# A2TP-Eurosys2023

## Abstract
Compared with the state-of-the-art in-network aggregation protocols, A2TP redesigns the congestion control algorithm, decouples in-network aggregator congestion and link bandwidth congestion, and considers the impact of stragglers, so as to improve the efficiency of in-network aggregation. We implement A2TP with P4 programmable switch and kernel bypass protocol stack at the end host. We provide the source code of the whole system. In addition, we conduct a benchmark experiment and provide experimental steps in detail to verify the performance of A2TP.


## Description \& Requirment
Our source code is built on ATP [1] (https://github.com/in-ATP/ATP.git), which is one of the advanced in-network aggregation schemes. Our core design is in the congestion control part, such as the decoupled window adjustment in CC_manerger.h and the straggling degree detection in p4ml_manager.cc, etc.
```
[1] C. Lao, Y. Le, K. Mahajan, Y. Chen, W. Wu, A. Akella and M.M. Swift. ATP: In-network Aggregation for Multi-tenant Learning. In Proc. NSDI, 2021.
```

### Hardware dependencies
The Mellanox NIC is required for the hosts. We recommend using the Mellanox ConnectX5 100Gbps NIC. Besides, our system requires programmable switch support and the recommended switch is Barefoot Wedge 100BF-32X.

### Software dependencies
For each host, the NIC driver version is MLNX\_OFED\_LINUX-4.9-4.1.7.0.
For aggregating switch, the SDE version is bf-sde-8.9.1.

## Directory Structure
```
./client ./common and ./server are deployed on workers and PSs
./p4ml2 ./ptf_p4ml2 and ./run_pd_rpc are used in programmable switch
./datasample is the sample data from the benchmark experiment
./shell is used to deal with the sample data and generate a .csv file
```

## Basic Performance
The detailed steps of the benchmark experiment are described in benchmark.md
