"""
热传导过程
"""
# 程序用的包
import json
import math
import random
import networkx as nx
import matplotlib.pyplot as plt


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
        if heat < 0.0001:
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
    with open("initial_nodes.txt", "r+", encoding="UTF-8") as file_list:
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
    :param t: 输入在线时间概率索引
    """
    # 输入在线时间概率索引列表
    t_list = [0.12192357870440063, 0.14645261511699867, 0.08067790656831753, 0.09861211467375851,
              0.04384364493953535, 0.08471155936909362, 0.09068112633181126, 0.08462312041079163,
              0.09701038687340058, 0.07652265542676501, 0.03866538712429123, 0.036275904460835964]
    for node in input_list:
        dh_list = []  # 定义暂存列表
        for ad_node in graph[node]:
            # 定义比较值
            # compare =
            # graph.nodes[ad_node]['compare'] / (graph.nodes[node]['compare'] + graph.nodes[ad_node]['compare'])
            # compare_pro = random.uniform(0, 1)
            online_pro = random.uniform(0, 1)
            # if online_pro < t_list[int(t % len(t_list))] and compare_pro > compare \
            #         and graph.nodes[node]['heat'] > graph.nodes[ad_node]['heat']:
            if online_pro < t_list[int(t % len(t_list))] and graph.nodes[node]['heat'] > graph.nodes[ad_node]['heat']:
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
    print("开始读取节点信息...")
    # 节点集 nodes_list
    nodes_list = []
    with open("rt_node.txt", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            nodes_list.append(int(file.strip()))
    print("读取完成！")
    print("开始读取边信息...")
    # 边集 edges_list
    edges_list = []
    with open("rt_edge.txt", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            edges_list.append((int(file.strip().split(" ")[0]), int(file.strip().split(" ")[1])))
    print("读取完成！")
    print("开始导入图...")
    graph = nx.Graph()
    graph.add_nodes_from(nodes_list)
    graph.add_edges_from(edges_list)
    print("导入完成！")
    print("开始模拟信息传播...")
    activate_node = []  # 被激活节点集
    result_list_1 = []
    result_list_2 = []
    result_list_3 = []
    for epoch in range(0, 10):
        with open("heat_node3.json", "w+", encoding="UTF-8") as file:
            node_list = initialize_node(graph)
            print("初始种子节点为：", len(node_list))
            nodes = [node_list]
            for i in range(1, 37):
                # 扩散过程
                diffusion_heat(graph, node_list, i)
                receive_heat(graph, node_list, i - 1)
                node_list = update_node(graph)
                item_node = list(set(node_list) - set(activate_node))
                # 更新被激活节点集
                activate_node += node_list
                item = {
                    "nodes": item_node
                }
                file.write(json.dumps(item, ensure_ascii=False) + "\n")
                nodes.append(item_node)
                #print("第" + str(i) + "轮传播结束，有温节点数共", len(node_list), "个，新增", len(item_node), "个")
                if i == 10:
                    result_list_1.append(len(node_list))
                    print("第" + str(i) + "轮传播结束，有温节点数共", len(node_list), "个，新增", len(item_node), "个")
                if i == 20:
                    result_list_2.append(len(node_list))
                    print("第" + str(i) + "轮传播结束，有温节点数共", len(node_list), "个，新增", len(item_node), "个")
                if i == 30:
                    result_list_3.append(len(node_list))
                    print("第" + str(i) + "轮传播结束，有温节点数共", len(node_list), "个，新增", len(item_node), "个")

    result_1 = 0
    for x in result_list_1:
        result_1 += x
    print(result_1, result_1/10)
    result_2 = 0
    for x in result_list_2:
        result_2 += x
    print(result_2, result_2/10)

    result_3 = 0
    for x in result_list_3:
        result_3 += x
    print(result_3, result_3/10)




