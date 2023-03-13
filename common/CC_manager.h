#ifndef CC_MANAGER_H
#define CC_MANAGER_H

#define MAX_BYTES 200 * P4ML_PACKET_SIZE

#define A2TPENABLE 1

#include "packet.h"
#include <iostream>
#include <stdint.h>
#include <stdio.h>
#include <math.h>
using namespace std;
#define do_div(n, base) ({            \
    uint32_t __base = (base);         \
    uint32_t __rem;                   \
    __rem = ((uint64_t)(n)) % __base; \
    (n) = ((uint64_t)(n)) / __base;   \
    __rem;                            \
})
#define GET_MIN(a, b) (a < b ? a : b)
#define GET_MAX(a, b) (a > b ? a : b)

class CC_manager {

public:
    CC_manager(int init_window, int max_window_size)
    {
        cwnd_bytes = init_window * P4ML_PACKET_SIZE;
        aggr_bytes = cwnd_bytes;
        max_window = max_window_size;
        last_window = max_window;
        ecn_count = 0;
        col_count = 0;
        aggr_count = init_window;
        last_aggr_count = init_window;
        alpha = 0;
        beta = 0;
        urgent = 1;
        last_ts = std::chrono::high_resolution_clock::now();
        receive_ack = 0;
        update_urgent = 1;
        gam = 1;
        print_gamflag = 0;
    }

 //   int adjustWindow(bool isECN, bool isCollision, int appID)
 void adjustWindow(bool isECN, bool isCollision, int appID, int looptime){

        if(A2TPENABLE){

            gam = (1 - 1.0 / 64) * gam + 1.0 / 64 * urgent; //smooth straggler degree

            alpha = (1 - 1.0 / 8) * alpha + 1.0 / 8 * (1.0 * ecn_count / (cwnd_bytes / P4ML_PACKET_SIZE)); //smooth link congestion factor
            beta = (1 - 1.0 / 8) * beta + 1.0 / 8 * (1.0 * col_count / (aggr_bytes / P4ML_PACKET_SIZE)); //smooth aggregator congestion factor


            
            double thre = 0.1; //threshold for aggregator congestion control
            if(isCollision && beta > thre){ //adjust aggregator congestion window
                aggr_bytes = aggr_bytes * (1 - pow(beta-thre, gam) / (2-thre));
            }else{
                aggr_bytes = aggr_bytes + P4ML_PACKET_SIZE; // P4ML_PACKET_SIZE1500
            }

            if (ecn_count > 0){ //adjust link congestion window
                cwnd_bytes = cwnd_bytes*(1-alpha/2);
                //printf("reciev ecn\n");
            }
            else{
                cwnd_bytes += P4ML_PACKET_SIZE; //P4ML_PACKET_SIZE1500
                //aggr_bytes += 1500;
            }


            if (cwnd_bytes < P4ML_PACKET_SIZE)
                cwnd_bytes = P4ML_PACKET_SIZE;
            if (cwnd_bytes > max_window * P4ML_PACKET_SIZE)
                cwnd_bytes = max_window * P4ML_PACKET_SIZE;
            if (cwnd_bytes > P4ML_PACKET_SIZE)
                cwnd_bytes = (cwnd_bytes / P4ML_PACKET_SIZE) * P4ML_PACKET_SIZE;

            if (aggr_bytes < P4ML_PACKET_SIZE)
                aggr_bytes = P4ML_PACKET_SIZE;
            if (aggr_bytes > max_window * P4ML_PACKET_SIZE)
                aggr_bytes = max_window * P4ML_PACKET_SIZE;
            if (aggr_bytes > P4ML_PACKET_SIZE)
                aggr_bytes = (aggr_bytes / P4ML_PACKET_SIZE) * P4ML_PACKET_SIZE;

            if (aggr_bytes > cwnd_bytes){
                aggr_bytes = cwnd_bytes;
            }
        }else{
            if (isECN){
                cwnd_bytes = cwnd_bytes / 2;
                //aggr_bytes = aggr_bytes*(1-alpha/2);
                //printf("reciev ecn\n");
            }
            else{
                cwnd_bytes += 1500;
                //aggr_bytes += 1500;
            }
            if (cwnd_bytes < P4ML_PACKET_SIZE)
                cwnd_bytes = P4ML_PACKET_SIZE;
            if (cwnd_bytes > max_window * P4ML_PACKET_SIZE)
                cwnd_bytes = max_window * P4ML_PACKET_SIZE;
            if (cwnd_bytes > P4ML_PACKET_SIZE)
                cwnd_bytes = (cwnd_bytes / P4ML_PACKET_SIZE) * P4ML_PACKET_SIZE;

            aggr_bytes = cwnd_bytes;

        }
        
        ecn_count = 0;
        col_count = 0;
        //return cwnd_bytes / P4ML_PACKET_SIZE;
}

int GetCwndPackets(){
    return cwnd_bytes / P4ML_PACKET_SIZE;
}

int GetAggrPackets(){
    return aggr_bytes / P4ML_PACKET_SIZE;
}

    int ecn_count;
    int col_count;
    int aggr_count;
    int last_aggr_count;
    double alpha; //link congestion factor
    double beta; //aggregator congestion factor
    double urgent; //straggler degree
    double gam;
    int last_window;
    int receive_ack;
    bool update_urgent;
    bool print_gamflag;
    std::chrono::high_resolution_clock::time_point last_ts;

private:
    uint64_t cwnd_bytes; //link congestion window size
    uint64_t aggr_bytes; //aggregator congestion window size
    int max_window;
};

#endif