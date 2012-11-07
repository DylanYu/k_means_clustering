import math
import random

MIN_NUMBER_OF_CLUSTER = 1

def read_file(file_name):
    data = []
    file_data = open(file_name)
    while True:
        str_number = file_data.readline().split()
        if not str_number: break
        numeric_number = []
        for num in str_number:
            numeric_number.append(int(num))
        data.append(numeric_number)
    return data

def cal_dist(data1, data2):
    if len(data1) != len(data2):
        return None
    tmp_sum = 0
    for i in range(0, len(data1)):
        tmp_sum += math.pow(data1[i] - data2[i], 2)
    return math.pow(tmp_sum, 0.5)
        
def cal_E(data, k_means, cluster_no):
    E = 0
    for i in range(0, len(data)):
        E += math.pow(cal_dist(data[i], k_means[cluster_no[i]]), 2)
    return E

def cal_cluster_no(data, k_means):
    num_of_instances = len(data)
    k = len(k_means)
    no = [0 for x in range(0, num_of_instances)]
    for i in range(0, num_of_instances):
        min_dist = 100000
        min_j = 0;
        for j in range(0, k):
            tmp_dist = cal_dist(data[i], k_means[j])
            if tmp_dist < min_dist:
                    min_dist = tmp_dist
                    min_j = j
        no[i] = min_j
    return no

def get_random_k_means(num_of_instances, k):
    k_means = []
    for i in range(0, k):
        random_num = random.randrange(0, num_of_instances)
        k_means.append(data[random_num])
    return k_means    

def cal_k_means(data, cluster_no, k):
    k_means = [[0 for x in range(0, len(data[0]))] for y in range(0, k)]
    tmp_sum = [[0 for x in range(0, len(data[0]))] for y in range(0, k)]
    count = [0 for x in range(0, k)]
    for i in range(0, len(data)):
        no = cluster_no[i]
        tmp_sum[no] = [(x + y) for x, y in zip(tmp_sum[no], data[i])]
        count[no] += 1
    for i in range(0, k):
        for j in range(0, len(data[0])):
            k_means[i][j] = float(tmp_sum[i][j]) / count[i]
    return k_means

def cluster(data, k):
    num_of_instances = len(data)
    num_of_attr = len(data[0])
    E = random.random()
    next_E = random.random()
    k_means = get_random_k_means(num_of_instances, k)
    i = 0
    while(math.fabs(E - next_E) > 1e-5):
    #while(E != next_E):
        i += 1
        cluster_no = cal_cluster_no(data, k_means)
        E = next_E
        next_E = cal_E(data, k_means, cluster_no)

        print 'k = ', k, ', round = ' , i, ', E = ', E

        k_means = cal_k_means(data, cluster_no, k)
    return cluster_no

def cal_clusters(data, max_k, every):
    cluster_results = []
    for k in range(MIN_NUMBER_OF_CLUSTER, max_k):
        result_k = []
        for i in range(0, every):
            result_k.append(cluster(data, k))
        cluster_results.append(result_k)
    return cluster_results

def cal_cluster_inner_dist(k_means):
    k = len(k_means)
    count = 0
    sum_dist = 0
    for i in range(0, k):
        for j in range(i + 1, k):
            sum_dist += cal_dist(k_means[i], k_means[j])
            count += 1
    return sum_dist / count

def cal_cluster_dist(data, cluster_results, max_k):
    k_means_s = []
    k = MIN_NUMBER_OF_CLUSTER;
    for cluster_no_i in cluster_results:
        tmp_k_means = [0 for x in range(0, len(data[0]))]
        i = 0
        for cluster_no in cluster_no_i:
            means = cal_k_means(data, cluster_no, k)
            tmp_k_means = [(x + y) for x, y in zip(tmp_k_means, means)]
            i += 1
        k_means_s.append(tmp_k_means)
        k += 1
    print k_means_s
    


data = read_file('clustering data')
clusters =  cal_clusters(data, 3, 1)
cal_cluster_dist(data, clusters, 3)
"""
cluster_no =  cluster(data, 10)
cluster_result = []
cluster_result.append(cluster_no)
k_means = cal_k_means(data, cluster_no, 10)
print cal_cluster_inner_dist(k_means)
"""
