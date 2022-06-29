"""
热传导过程
"""
# 程序用的包
import json
import math
import random
import networkx as nx
import matplotlib.pyplot as plt

from Networkx.heat.experiment2 import calculate_error


def node_threshold(heat):
    """
    判断当前节点阈值
    :param heat: 当前节点应有热值
    :return: 返回节点阈值
    """
    heat_list = [heat]
    t = 1  # 次数
    while True:
        # 冷却系数
        k = 1 - 0.56 * (t ** 0.06)
        # 发散系数
        r = math.e ** (-k * t)
        heat *= r
        if heat < 0.01:
            break
        heat_list.append(heat)
        t += 1
    return heat_list[-1]


def initialize_node(graph):
    """
    初始化图内节点属性
    :param graph: 输入图
    :return: 带有热值的节点列表
    """
    # node_list = random.sample(graph.nodes, 5)  # 带有热值的节点列表
    node_list = []
    with open("higgs_twitter/RT_initial_nodes.txt", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            node_list.append(int(file))
    for node in graph:
        if node in node_list:
            graph.nodes[node]['heat'] = len(graph[node])  # 节点热值
            graph.nodes[node]['rh_flag'] = True  # 接收热量标志
        else:
            graph.nodes[node]['heat'] = 0  # 节点热值
            graph.nodes[node]['rh_flag'] = False  # 接收热量标志
        # 节点比较值
        graph.nodes[node]['compare'] = len(graph[node])
        # 传递热量dh  接收热量rh 扩散系数alpha
        graph.nodes[node]['dh'] = graph.nodes[node]['rh'] = 0
        # 传热邻接节点列表
        graph.nodes[node]['dh_list'] = []
        # 节点阈值
        graph.nodes[node]['threshold'] = node_threshold(len(graph[node]))
    return node_list


def diffusion_heat(graph, input_list, t):
    """
    发散热量
    :param graph: 输入图
    :param input_list: 输入有温节点列表
    :param t: 时间
    """
    # 冷却系数
    k = 1 - 0.56 * (t ** 0.06)
    # 发散系数
    r = math.e ** (-k * t)
    for node in input_list:
        graph.nodes[node]['dh'] = graph.nodes[node]['heat'] * (1 - r)
        graph.nodes[node]['heat'] *= r


def receive_heat(graph, input_list, t):
    """
    接收热量
    :param graph: 输入图
    :param input_list: 输入有温节点列表
    """
    # t_list = [0.056298142564320364, 0.06580432065955305, 0.05602225811433192, 0.060508627092418825,
    #           0.03990754102435458, 0.027749906328666866, 0.024543515242138794, 0.02517665968133934,
    #           0.021727368183861118, 0.022524453228036288, 0.020487798074904386, 0.02744039214969867,
    #           0.04333582387387297, 0.04896559934584039, 0.04384453988579808, 0.03673341453107649,
    #           0.03704855112714843, 0.034788296809611756, 0.039029552482305864, 0.043668466501782535,
    #           0.0549634674349343, 0.051372281264985734, 0.060192278119275314, 0.05786674627974397]
    # 确定接收热值节点列表
    t_list = [0.006018088073704674, 0.026055841997013496, 0.05473191896993773, 0.6574000507142254, 0.17550502916067956,
              0.05502775195108895, 0.025261319133350238]
    for node in input_list:
        dh_list = []  # 定义暂存列表
        for ad_node in graph[node]:
            # 定义比较值
            compare = graph.nodes[ad_node]['compare'] / (graph.nodes[node]['compare'] + graph.nodes[ad_node]['compare'])
            compare_pro = random.uniform(0, 1)
            online_pro = random.uniform(0, 1)
            if online_pro < t_list[t % len(t_list)] and compare_pro > compare and\
                    graph.nodes[node]['heat'] > graph.nodes[ad_node]['heat'] and not graph.nodes[ad_node]['rh_flag']:
                dh_list.append(ad_node)
                graph.nodes[ad_node]['rh_flag'] = True
        graph.nodes[node]['dh_list'] = dh_list
    # 确定扩散系数alpha 并 更新值rh
    for node in input_list:
        alpha = 1 / len(graph.nodes[node]['dh_list']) if graph.nodes[node]['dh_list'] else 0
        for dh_node in graph.nodes[node]['dh_list']:
            graph.nodes[dh_node]['rh'] = graph.nodes[node]['dh'] * alpha


def update_node(graph):
    """
    更新图中节点热值
    :param graph: 输入图
    :return: 返回有温节点列表
    """
    node_list = []
    for node in graph:
        graph.nodes[node]['heat'] += graph.nodes[node]['rh']
        # 清零
        graph.nodes[node]['rh'] = graph.nodes[node]['dh'] = 0
        # 超过阈值就清零
        # if graph.nodes[node]['heat'] <= graph.nodes[node]['threshold']:
        #     graph.nodes[node]['heat'] = 0
        # else:
        #     node_list.append(node)
        if graph.nodes[node]['heat'] > 0:
            node_list.append(node)
    return node_list


if __name__ == "__main__":
    # 定义网络
    # ba = nx.barabasi_albert_graph(150, 15)
    # # 网络节点初始化
    # node_list = initialize_node(ba)
    # nodes = [len(node_list)]
    # print(len(node_list), [ba.nodes[node]['heat'] for node in node_list])
    # for i in range(1, 8):
    #     # 扩散过程
    #     diffusion_heat(ba, node_list, i)
    #     receive_heat(ba, node_list)
    #     node_list = update_node(ba)
    #     nodes.append(len(node_list))
    #     print(len(node_list), [ba.nodes[node]['heat'] for node in node_list])
    # plt.plot(nodes)
    # plt.show()

    # nodes_list = [i for i in range(1, 31)]
    # edges_list = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 10), (2, 19), (2, 18), (5, 7), (5, 6), (4, 11), (4, 24),
    #               (3, 14), (10, 23), (10, 22), (18, 21), (18, 20), (20, 26), (6, 8), (8, 25), (8, 9), (7, 29),
    #               (7, 30), (11, 12), (11, 13), (12, 28), (24, 27), (14, 16), (14, 17), (14, 15)]

    # origin_nodes = []
    # with open("higgs_twitter/RT_time_stamp.json", "r+", encoding="UTF-8") as file_list:
    #     for file in file_list:
    #         content = json.loads(file)
    #         origin_nodes.append(content["nodes"])
    print("开始读取节点信息...")
    # 节点集 nodes_list
    nodes_list = []
    with open("higgs_twitter/RT_node_set.txt", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            nodes_list.append(int(file.strip()))
    print("读取完成！")
    print("开始读取边信息...")
    # 边集 edges_list
    edges_list = []
    with open("higgs_twitter/RT_edge_set.txt", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            edges_list.append((int(file.strip().split(" ")[0]), int(file.strip().split(" ")[1])))
    print("读取完成！")
    print("开始导入图...")
    ba = nx.Graph()
    ba.add_nodes_from(nodes_list)
    ba.add_edges_from(edges_list)
    print("导入完成！")
    print("开始模拟信息传播...")
    # 被激活节点集
    activate_node = []
    with open("higgs_twitter/heat_node.json", "w+", encoding="UTF-8") as file:
        node_list = initialize_node(ba)
        print("初始种子节点为：", len(node_list))
        nodes = [node_list]
        for i in range(1, 49):
            # 扩散过程
            diffusion_heat(ba, node_list, i)
            receive_heat(ba, node_list, i - 1)
            node_list = update_node(ba)
            item_node = list(set(node_list) - set(activate_node))
            # 更新被激活节点集
            activate_node += node_list
            item = {
                "nodes": item_node
            }
            file.write(json.dumps(item, ensure_ascii=False) + "\n")
            nodes.append(item_node)
            print("第" + str(i) + "轮传播结束，有温节点数共", len(node_list), "个，新增", len(item_node), "个")
        # nx.draw(ba, node_size=200, with_labels=True)
        plot_node = [len(node) for node in nodes]
        #plot_list = [len(nodes) for nodes in nodes_list]
        #calculate_error(plot_list, folder)
        plt.plot(plot_node, 'ro-')
        plt.show()







