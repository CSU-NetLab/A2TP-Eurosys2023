clear_all()

p4_pd.register_reset_all_agtr_time()
p4_pd.register_reset_all_appID_and_Seq()
p4_pd.register_reset_all_bitmap()
p4_pd.register_reset_all_register1()
p4_pd.register_reset_all_register2()
p4_pd.register_reset_all_register3()
p4_pd.register_reset_all_register4()
p4_pd.register_reset_all_register5()
p4_pd.register_reset_all_register6()
p4_pd.register_reset_all_register7()
p4_pd.register_reset_all_register8()
p4_pd.register_reset_all_register9()
p4_pd.register_reset_all_register10()
p4_pd.register_reset_all_register11()
p4_pd.register_reset_all_register12()
p4_pd.register_reset_all_register13()
p4_pd.register_reset_all_register14()
p4_pd.register_reset_all_register15()
p4_pd.register_reset_all_register16()
p4_pd.register_reset_all_register17()
p4_pd.register_reset_all_register18()
p4_pd.register_reset_all_register19()
p4_pd.register_reset_all_register20()
p4_pd.register_reset_all_register21()
p4_pd.register_reset_all_register22()
p4_pd.register_reset_all_register23()
p4_pd.register_reset_all_register24()
p4_pd.register_reset_all_register25()
p4_pd.register_reset_all_register26()
p4_pd.register_reset_all_register27()
p4_pd.register_reset_all_register28()
p4_pd.register_reset_all_register29()
p4_pd.register_reset_all_register30()
p4_pd.register_reset_all_register31()
# p4_pd.register_reset_all_register32()


# These are background traffic
# p4_pd.bg_outPort_table_table_add_with_set_egr(
#     p4_pd.bg_outPort_table_match_spec_t(0), 
#     p4_pd.set_egr_action_spec_t(4)
# )

# p4_pd.bg_outPort_table_table_add_with_set_egr(
#     p4_pd.bg_outPort_table_match_spec_t(1), 
#     p4_pd.set_egr_action_spec_t(0)
# )

# first Zero for pending
#port_of_worker = [0, 56, 48, 40, 32, 24, 16, 8, 0, 4]
#port_of_worker = [0, 8, 0, 4]
port_of_worker = [0, 60, 52, 44, 36, 28, 0, 8, 16, 24, 32, 40]
single_loopback_port = [0, 20, 12] #20 12

MAC_address_of_worker = [ "0"
                        , "0c:42:a1:5a:5b:c1"
                        , "0c:42:a1:5a:5b:d9"
                        , "0c:42:a1:5a:5b:b9"
                        , "0c:42:a1:5a:53:01"
                        , "b8:59:9f:e2:0c:17"
                        , "b8:59:9f:e2:0c:16"
                        , "0c:42:a1:5a:5b:e1"
                        , "b8:59:9f:e2:25:f7"
                        , "b8:59:9f:e2:09:47"
                        , "0c:42:a1:5a:53:81"
                        , "b8:59:9f:e2:26:0e"]

# host0   24  60  0c:42:a1:5a:5b:c1
# host1   23  52  0c:42:a1:5a:5b:d9
# host2  22  44  0c:42:a1:5a:5b:b9
# host3   21  36  0c:42:a1:5a:53:01
##host4   20  28  b8:59:9f:e2:0c:17
# loop1     19  20
# loop2     18  12
#           17  
##host5   16  0   b8:59:9f:e2:0c:16
# host6   15  8   0c:42:a1:5a:5b:e1
# host7   14  16  b8:59:9f:e2:25:f7
# host8   13  24  b8:59:9f:e2:09:47
# host9   12  32  0c:42:a1:5a:53:81
# host10   11  40  b8:59:9f:e2:26:0e





# first Zero for pending
# PSs = [0, 9, 8]
PSs = [0, 5, 6]

len_workers = len(port_of_worker)
len_PS = len(PSs)

# Normal Switch traffic
for i in range(1, len_workers):
    p4_pd.forward_table_add_with_set_egr(
        p4_pd.forward_match_spec_t(macAddr_to_string(MAC_address_of_worker[i])),
        p4_pd.set_egr_action_spec_t(port_of_worker[i])
    )


# P4ML Traffic

# No Pending packet, First time enter switch
for i in range(1, len_workers - 1): 
    for j in range(1, len_PS): #appIDandseqnum,loopport,dataIndex,PSIndex PSIndex=key%num_PS
        p4_pd.outPort_table_table_add_with_set_egr_and_set_index(
        p4_pd.outPort_table_match_spec_t(
            j << 16,
            port_of_worker[i],
            0,
            0), 
        
        p4_pd.set_egr_and_set_index_action_spec_t(single_loopback_port[j]))

# Not Pending packet, Second time enter switch
for j in range(1, len_PS): 
    print(j, PSs[j]) #appIDandseqnum,loopport,dataIndex,PSIndex
    p4_pd.outPort_table_table_add_with_set_egr(
    p4_pd.outPort_table_match_spec_t(
        j << 16,
        single_loopback_port[j],
        1,
        0), 
    # app1 -> worker3
    p4_pd.set_egr_action_spec_t(port_of_worker[PSs[j]]))

# INGRESSPORT, Index

for i in range(1, len_workers - 1):#ingressport,dataindex
    p4_pd.drop_table_table_add_with_drop_pkt(
        p4_pd.drop_table_match_spec_t(
            port_of_worker[i],
            1)
    )

####### Server ########
'''
for j in range(1, len_PS):
    p4_pd.multicast_table_table_add_with_multicast(
        p4_pd.multicast_table_match_spec_t(
            1,
            1 << 16,
            port_of_worker[PSs[j]],
            0),
        # multicast app1 -> worker1, 2
        p4_pd.multicast_action_spec_t(999)
    )
'''
for j in range(1, len_PS): #isAck, appIDandseqnum, IngressPort, dataIndex; aciton(multicast_group)
    p4_pd.multicast_table_table_add_with_multicast(
        p4_pd.multicast_table_match_spec_t(
            1,
            j << 16,
            port_of_worker[PSs[j]],
            0),
        # multicast app1 -> worker1, 2
        p4_pd.multicast_action_spec_t(1000-j)
    )

p4_pd.modify_packet_bitmap_table_table_add_with_modify_packet_bitmap(
    p4_pd.modify_packet_bitmap_table_match_spec_t(1)
)

p4_pd.modify_packet_bitmap_table_table_add_with_nop(
    p4_pd.modify_packet_bitmap_table_match_spec_t(0)
)

p4_pd.processEntry1_table_add_with_processentry1(
    p4_pd.processEntry1_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry1_table_add_with_noequ0_processentry1(
    p4_pd.processEntry1_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1,
)
p4_pd.processEntry2_table_add_with_processentry2(
    p4_pd.processEntry2_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry2_table_add_with_noequ0_processentry2(
    p4_pd.processEntry2_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry3_table_add_with_processentry3(
    p4_pd.processEntry3_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry3_table_add_with_noequ0_processentry3(
    p4_pd.processEntry3_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry4_table_add_with_processentry4(
    p4_pd.processEntry4_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry4_table_add_with_noequ0_processentry4(
    p4_pd.processEntry4_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry5_table_add_with_processentry5(
    p4_pd.processEntry5_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry5_table_add_with_noequ0_processentry5(
    p4_pd.processEntry5_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry6_table_add_with_processentry6(
    p4_pd.processEntry6_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry6_table_add_with_noequ0_processentry6(
    p4_pd.processEntry6_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry7_table_add_with_processentry7(
    p4_pd.processEntry7_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry7_table_add_with_noequ0_processentry7(
    p4_pd.processEntry7_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry8_table_add_with_processentry8(
    p4_pd.processEntry8_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry8_table_add_with_noequ0_processentry8(
    p4_pd.processEntry8_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry9_table_add_with_processentry9(
    p4_pd.processEntry9_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry9_table_add_with_noequ0_processentry9(
    p4_pd.processEntry9_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry10_table_add_with_processentry10(
    p4_pd.processEntry10_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry10_table_add_with_noequ0_processentry10(
    p4_pd.processEntry10_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry11_table_add_with_processentry11(
    p4_pd.processEntry11_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry11_table_add_with_noequ0_processentry11(
    p4_pd.processEntry11_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry12_table_add_with_processentry12(
    p4_pd.processEntry12_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry12_table_add_with_noequ0_processentry12(
    p4_pd.processEntry12_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry13_table_add_with_processentry13(
    p4_pd.processEntry13_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry13_table_add_with_noequ0_processentry13(
    p4_pd.processEntry13_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry14_table_add_with_processentry14(
    p4_pd.processEntry14_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry14_table_add_with_noequ0_processentry14(
    p4_pd.processEntry14_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry15_table_add_with_processentry15(
    p4_pd.processEntry15_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry15_table_add_with_noequ0_processentry15(
    p4_pd.processEntry15_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry16_table_add_with_processentry16(
    p4_pd.processEntry16_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry16_table_add_with_noequ0_processentry16(
    p4_pd.processEntry16_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry17_table_add_with_processentry17(
    p4_pd.processEntry17_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry17_table_add_with_noequ0_processentry17(
    p4_pd.processEntry17_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry18_table_add_with_processentry18(
    p4_pd.processEntry18_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry18_table_add_with_noequ0_processentry18(
    p4_pd.processEntry18_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry19_table_add_with_processentry19(
    p4_pd.processEntry19_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry19_table_add_with_noequ0_processentry19(
    p4_pd.processEntry19_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry20_table_add_with_processentry20(
    p4_pd.processEntry20_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry20_table_add_with_noequ0_processentry20(
    p4_pd.processEntry20_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry21_table_add_with_processentry21(
    p4_pd.processEntry21_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry21_table_add_with_noequ0_processentry21(
    p4_pd.processEntry21_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry22_table_add_with_processentry22(
    p4_pd.processEntry22_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry22_table_add_with_noequ0_processentry22(
    p4_pd.processEntry22_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry23_table_add_with_processentry23(
    p4_pd.processEntry23_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry23_table_add_with_noequ0_processentry23(
    p4_pd.processEntry23_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry24_table_add_with_processentry24(
    p4_pd.processEntry24_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry24_table_add_with_noequ0_processentry24(
    p4_pd.processEntry24_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry25_table_add_with_processentry25(
    p4_pd.processEntry25_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry25_table_add_with_noequ0_processentry25(
    p4_pd.processEntry25_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry26_table_add_with_processentry26(
    p4_pd.processEntry26_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry26_table_add_with_noequ0_processentry26(
    p4_pd.processEntry26_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry27_table_add_with_processentry27(
    p4_pd.processEntry27_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry27_table_add_with_noequ0_processentry27(
    p4_pd.processEntry27_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry28_table_add_with_processentry28(
    p4_pd.processEntry28_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry28_table_add_with_noequ0_processentry28(
    p4_pd.processEntry28_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry29_table_add_with_processentry29(
    p4_pd.processEntry29_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry29_table_add_with_noequ0_processentry29(
    p4_pd.processEntry29_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry30_table_add_with_processentry30(
    p4_pd.processEntry30_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry30_table_add_with_noequ0_processentry30(
    p4_pd.processEntry30_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
p4_pd.processEntry31_table_add_with_processentry31(
    p4_pd.processEntry31_match_spec_t(hex_to_i32(0), hex_to_i32(0xFFFFFFFF)), 1,
)
p4_pd.processEntry31_table_add_with_noequ0_processentry31(
    p4_pd.processEntry31_match_spec_t(hex_to_i32(0), hex_to_i32(0x00000000)), 1
)
try:
    # TODO: understand it
    # dont know why, but if group = input port,
    # then the packet followed by that packet will execute multicast
    # therefore make it 20, no 20th port is used.
    mcg_all  = mc.mgrp_create(999)
    mcg1  = mc.mgrp_create(998)
    # mcg2  = mc.mgrp_create(997)
    # mcg3  = mc.mgrp_create(996)
except:
    print """
clean_all() does not yet support cleaning the PRE programming.
You need to restart the driver before running this script for the second time
"""
    quit()

node_all = mc.node_create(
    rid=999,
    #port_map=devports_to_mcbitmap([56,48,40,32,24,16,8,0]),
    # port_map=devports_to_mcbitmap([port_of_worker[2], port_of_worker[3], port_of_worker[4],]),
    #port_map=devports_to_mcbitmap([36,44]),
    port_map=devports_to_mcbitmap([60,52,44,36]),
    lag_map=lags_to_mcbitmap(([]))
)
mc.associate_node(mcg_all, node_all, xid=0, xid_valid=False)

#[52, 60, 36, 44, 12, 4, 20]

node1 = mc.node_create(
    rid=998,
    # Not multicast to "0" ( 0 as bg traffic )
    #port_map=devports_to_mcbitmap([56,48,40,32,24,16,8]),
    port_map=devports_to_mcbitmap([8,16,24,32]),
    #port_map=devports_to_mcbitmap([52,60,0]),
    lag_map=lags_to_mcbitmap(([]))
)
mc.associate_node(mcg1, node1, xid=0, xid_valid=False)


# node2 = mc.node_create(
#     rid=997,
#     # Not multicast to "0" ( 0 as bg traffic )
#     #port_map=devports_to_mcbitmap([56,48,40,32,24,16,8]),
#     #port_map=devports_to_mcbitmap([56,48,40]),
#     port_map=devports_to_mcbitmap([60,0]),
#     lag_map=lags_to_mcbitmap(([]))
# )
# mc.associate_node(mcg2, node2, xid=0, xid_valid=False)

'''
node2 = mc.node_create(
    rid=997,
    # Not multicast to "0" ( 0 as bg traffic )
    # port_map=devports_to_mcbitmap([56,48,40,32,24,16,8]),
    port_map=devports_to_mcbitmap([24,16,8]),
    lag_map=lags_to_mcbitmap(([]))
)
mc.associate_node(mcg2, node2, xid=0, xid_valid=False)
'''

conn_mgr.complete_operations()

def hex_to_i32(h):
    x = int(h, 0)
    if (x > 0xFFFFFFFF):
        raise UIn_Error("Integer cannot fit within 32 bits")
    if (x > 0x7FFFFFFF): x-= 0x100000000
    return x

import time


used_aggr = 450
all_start = time.time()
last_time1 = all_start
last_time2 = all_start

num_com = 0
average_total = 0
average_appID_map = {}

tmp = []
appID_map = {}

while (1):

    now = time.time()
    time_count1 = now - last_time1
    time_count2 = now - last_time2
    if (time_count1 > 0.01):
        lasttime1=now
        num_com += 1

        del tmp[:]
        appID_map.clear()
        total_used = 0
        #timetmp1 = time.time()
        p4_pd.register_hw_sync_appID_and_Seq()

        for i in range(used_aggr):
            tmp.append(p4_pd.register_read_appID_and_Seq(i , p4_pd.register_flags_t(False)))
        #timetmp2 = time.time()
        #print timetmp2-timetmp1
        #print "hello"
        for appID_and_Seq in tmp:
            appID = (appID_and_Seq[0]>>16)
            #print "appID", appID
            if appID != 0:
                if appID in appID_map:
                    appID_map[appID] += 1    
                else:
                    appID_map[appID] = 1

                if appID in average_appID_map:
                    average_appID_map[appID] += 1    
                else:
                    average_appID_map[appID] = 1
                                                
        for key, value in appID_map.items():
            total_used += value
            #print "appID{0} {1}/{2} {3}".format(key, value, used_aggr, 1.0*value/used_aggr)
        average_total += total_used

        #if total_used != 0:
        #print "total_used {0}/{1} {2}".format(total_used, used_aggr, 1.0*total_used/used_aggr)
        time.sleep(0.09)
    
    if (time_count2 > 0.5):
        last_time2 = now 
        for key, value in average_appID_map.items():
            print "appID[{0}] {1}/{2} {3:.2f} %".format(key, value/num_com, used_aggr, 100.0*value/num_com/used_aggr)

        if average_total > 0:
            print "time {3:.1f} total_used {0}/{1} {2:.1f} %".format(average_total/num_com, used_aggr, 100.0*average_total/num_com/used_aggr, now - all_start)

        num_com = 0
        average_total = 0
        average_appID_map.clear()

'''
while (1):

    now = time.time()
    time_count1 = now - last_time1
    time_count2 = now - last_time2
    if (time_count1 > 0.01):
        lasttime1=now
        num_com += 1

        del tmp[:]
        appID_map.clear()
        total_used = 0
        timetmp1 = time.time()
        p4_pd.register_hw_sync_appID_and_Seq()

        for i in range(used_aggr):
            tmp.append(p4_pd.register_read_appID_and_Seq(i , p4_pd.register_flags_t(False)))
        timetmp2 = time.time()
        time.sleep(0.5 - (timetmp2-timetmp1))
        #print timetmp2-timetmp1
        #print "hello"
        for appID_and_Seq in tmp:
            appID = (appID_and_Seq[0]>>16)
            #print "appID", appID
            if appID != 0:
                if appID in appID_map:
                    appID_map[appID] += 1    
                else:
                    appID_map[appID] = 1

                if appID in average_appID_map:
                    average_appID_map[appID] += 1    
                else:
                    average_appID_map[appID] = 1
                                                
        for key, value in appID_map.items():
            total_used += value
            #print "appID{0} {1}/{2} {3}".format(key, value, used_aggr, 1.0*value/used_aggr)
        average_total += total_used

        #if total_used != 0:
        #print "total_used {0}/{1} {2}".format(total_used, used_aggr, 1.0*total_used/used_aggr)
        #time.sleep(0.1)
    
    if (time_count2 > 1.0):
        last_time2 = now 
        for key, value in average_appID_map.items():
            print "appID[{0}] {1}/{2} {3:.2f} %".format(key, value/num_com, used_aggr, 100.0*value/num_com/used_aggr)

        if average_total > 0:
            print "time {3:.0f} total_used {0}/{1} {2:.1f} %".format(average_total/num_com, used_aggr, 100.0*average_total/num_com/used_aggr, now - all_start)

        num_com = 0
        average_total = 0
        average_appID_map.clear()

'''

    

