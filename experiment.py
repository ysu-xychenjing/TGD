import json
import time
import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from sklearn.metrics.pairwise import cosine_similarity


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


"""
对比模型
SI模型
"""


def initialize_node(graph, folder):
    """
    初始化网络
    :param graph: 图
    """
    # 获取初始化节点集
    node_list = []
    with open(folder + "/initial_nodes.txt", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            node_list.append(int(file.strip()))
    for node in graph:
        if node in node_list:
            graph.nodes[node]["status"] = 'I'
        else:
            graph.nodes[node]["status"] = 'S'
    print("初始节点为：", len(node_list))


def update_graph(graph, beta):
    """
    更新网络
    :param graph: 图
    :param beta: 感染率
    :return:
    """
    for node in graph:
        if graph.nodes[node]["status"] == 'S':
            i_num = 0
            for ad_node in graph[node]:
                if graph.nodes[ad_node]["status"] == 'I':
                    i_num += 1
            if random.random() < 1 - (1 - beta) ** i_num:
                graph.nodes[node]["status"] = 'I'


def count_node(graph):
    """
    计算网络中的节点
    :param graph: 图
    :return: 感染节点数
    """
    i_list = []
    for node in graph:
        if graph.nodes[node]["status"] == "I":
            i_list.append(node)
    return i_list


def mape_value(y_true, y_pred):
    """
    计算mape值
    :param y_true: 真实值
    :param y_pred: 预测值
    :return: MAPE误差
    """
    return np.mean(np.abs((y_pred - y_true) / y_true)) * 100


def calculate_error(predictValue, folder):
    """
    计算误差
    :param predictValue: 预测值列表
    """
    realValue = []
    node_set = set()
    with open(folder + "/content_dict.json", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            content = json.loads(file)
            cur_set = set()
            for value in content["value"]:
                con = json.loads(value)
                if con["user_A"] not in node_set:
                    node_set.add(con["user_A"])
                    cur_set.add(con["user_A"])
                if con["user_B"] not in node_set:
                    node_set.add(con["user_B"])
                    cur_set.add(con["user_B"])
            realValue.append(len(cur_set))
    num1 = 0
    plot_list1 = []
    plot_list2 = predictValue
    for i in range(len(realValue)):
        num1 += realValue[i]
        plot_list1.append(num1)
    # 准确值
    accuracy = []
    for i in range(len(plot_list1)):
        accuracy.append(1 - abs(plot_list1[i] - plot_list2[i]) / plot_list1[i])
    print("准确率：", format(sum(accuracy) / len(accuracy) * 100, ".2f"), "%")
    plot_list1 = np.array(plot_list1)
    plot_list2 = np.array(plot_list2)
    print("余弦相似度：", cosine_similarity([plot_list1], [plot_list2])[0][0])
    mse = metrics.mean_squared_error(plot_list1, plot_list2)  # 均方误差MSE
    rmse = np.sqrt(mse)  # 均方根误差
    mae = metrics.mean_absolute_error(plot_list1, plot_list2)  # 平均绝对误差
    print("RMSE = ", format(rmse, ".2f"))
    print("MAE = ", format(mae, ".2f"))
    r2_score = metrics.r2_score(plot_list1, plot_list2)
    print("R2_score = ", format(r2_score, ".4f"))
    mape = mape_value(plot_list1, plot_list2)
    print("MAPE = ", format(mape, ".2f"), "%")
    x = [i for i in range(36)]
    plt.plot(x, plot_list1, "b-", label="Real Value")
    plt.plot(x, plot_list2, "r-", label="Predict Value")
    plt.fill_between(x, plot_list1, plot_list2, facecolor='yellow', alpha=0.6)
    plt.xlabel("Time")
    plt.ylabel("Number of diffusion")
    plt.legend(loc=0)
    plt.savefig("SI-model.png", dpi=600, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    print("开始读取节点信息...")
    # 文件夹
    folder = "rt_bahrain"
    # 节点集 nodes_list
    nodes_list = []
    with open(folder + "/rt_node.txt", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            nodes_list.append(int(file.strip()))
    print("读取完成！")
    print("开始读取边信息...")
    # 边集 edges_list
    edges_list = []
    with open(folder + "/rt_edge.txt", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            edges_list.append((int(file.strip().split(" ")[0]), int(file.strip().split(" ")[1])))
    print("读取完成！")
    print("开始导入图...")
    graph = nx.Graph()
    graph.add_nodes_from(nodes_list)
    graph.add_edges_from(edges_list)
    print("导入完成！")
    print("开始模拟信息传播...")
    beta_list = np.linspace(0.05, 0.15, 11)
    # 感染节点列表
    i_list = []
    # 记录每轮节点
    nodes_list = []
    # 初始化节点
    initialize_node(graph, folder)
    # 记录前一轮节点数
    before_node = count_node(graph)
    # 记录新增节点数
    new_node_list = []
    for i in range(36):
        update_graph(graph, 0.09)
        i_list = count_node(graph)
        # 记录每轮节点
        nodes_list.append(i_list)
        # 新增节点数
        new_node = list(set(i_list) - set(before_node))
        new_node_list.append(new_node)
        # 更新前一轮节点
        before_node = i_list
        print("第", i + 1, "轮传播结束,共影响节点", len(i_list), "个,新增影响节点,", len(new_node), "个")
    # 存储节点
    with open(folder + "/experiment1.json", "w+", encoding="UTF-8") as file:
        for new_node in new_node_list:
            item = {
                "nodes": new_node
            }
            file.write(json.dumps(item, ensure_ascii=False) + "\n")
    # 画图列表
    plot_list = [len(nodes) for nodes in nodes_list]
    calculate_error(plot_list, folder)
    # for j in range(10):
    #     # 感染节点列表
    #     i_list = []
    #     # 记录每轮节点
    #     nodes_list = []
    #     # 初始化节点
    #     initialize_node(graph)
    #     # 记录前一轮节点数
    #     before_node = count_node(graph)
    #     for i in range(36):
    #         update_graph(graph, 0.08)
    #         i_list = count_node(graph)
    #         # 记录每轮节点
    #         nodes_list.append(i_list)
    #         # 新增节点数
    #         new_node = list(set(i_list) - set(before_node))
    #         # 更新前一轮节点
    #         before_node = i_list
    #         # print("第", i + 1, "轮传播结束,共影响节点", len(i_list), "个,新增影响节点,", len(new_node), "个")
    #     # 画图列表
    #     plot_list = [len(nodes) for nodes in nodes_list]
    #     print("第", j + 1, "轮测试, 当前β值为", beta_list[j])
    #     calculate_error(plot_list)











