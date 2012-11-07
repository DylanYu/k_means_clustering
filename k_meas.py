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
    file_data.close()
    return data

def data_extraction(data, combination):
    new_instance_number = len(data[0]) / combination
    new_data = [[0 for x in range(0, new_instance_number)] for y in range(0, len(data))]
    for i in range(0, len(data)):
        for j in range(0, new_instance_number):
            for k in range(0, combination):
                new_data[i][j] += data[i][j * combination + k]
    """
    ?????why can't print
    """
    return new_data

def cal_dist(data1, data2):
    if len(data1) != len(data2):
        print 'error len in cal_dist'
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

def cal_E_auto(data, cluster_no, k):
    means = cal_k_means(data, cluster_no, k)
    E = cal_E(data, means, cluster_no)
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

def get_random_k_means(data, num_of_instances, k):
    k_means = []
    for i in range(0, k):
        random_num = random.randrange(0, num_of_instances)
        k_means.append(data[random_num])
    return k_means

def cal_k_means(data, cluster_no, k):
    k_means = [[0 for x in range(0, len(data[0]))] for y in range(0, k)]
    tmp_sum = [[0 for x in range(0, len(data[0]))] for y in range(0, k)]
    #avoid count[i] == 0
    count = [1 for x in range(0, k)]
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
    k_means = get_random_k_means(data, num_of_instances, k)
    i = 0
    while(math.fabs(E - next_E) > 1e-5):
    #while(E != next_E):
        i += 1
        cluster_no = cal_cluster_no(data, k_means)
        E = next_E
        next_E = cal_E(data, k_means, cluster_no)
        k_means = cal_k_means(data, cluster_no, k)
    print 'k = ', k, ', round used= ' , i, ', E = ', E
    return cluster_no

def cal_cluster_optimally(data, k, candidate_number):
    cluster_s = []
    for i in range(0, candidate_number):
        cluster_s.append(cluster(data, k))
    min_E = 10000000;
    min_i = 0;
    for i in range(0, candidate_number):
        means = cal_k_means(data, cluster_s[i], k)
        E = cal_E(data, means, cluster_s[i])
        if E < min_E:
            min_E = E
            min_i = i
    print "min: ", min_i, " ", min_E
    return cluster_s[min_i]

def generate_cluster_s(data, start_k, end_k, candidate_number):
    cluster_s = []
    for i in range(start_k, end_k + 1):
        file_generated_cluster = open('result_k_' + str(i), 'w')
        cluster = cal_cluster_optimally(data, i, candidate_number)
        cluster_s.append(cluster)
        for no in cluster:
            file_generated_cluster.write(str(no) + ' ')
        file_generated_cluster.write('\n')
        file_generated_cluster.flush()
        file_generated_cluster.close()
    return cluster_s

def read_assess_data():
    filename = "assess_data"
    file_data = open(filename)
    assess_data = []
    while True:
        str_numbers = file_data.readline().split()
        if not str_numbers: break
        numeric_number = []
        for num in str_numbers:
            int_num = int(num)
            numeric_number.append(int_num)
        assess_data.append(numeric_number)
    return assess_data

def assess(data):
    assess_data = read_assess_data()
    all_E = []
    min_E = 100000
    min_i = -1;
    for i in range(MIN_NUMBER_OF_CLUSTER, len(assess_data) + 1):
        E = cal_E_auto(data, assess_data[i - 1], i)
        if E < min_E:
            min_E = E
            min_i = i
        all_E.append(E)
        print "i = ", i, ", E = ", E
    print "best k is: ", min_i
    

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
new_data = data_extraction(data, 8)
generate_cluster_s(new_data, 2, 20, 20)
#assess(data)
