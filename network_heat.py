# 热传播模型
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random


def initial_node_heat(G, num):
    """
    初始化图内数据
    :param G: 输入图
    :param num: 输出图
    """
    node_list = random.sample(G.nodes, num)
    for node in G:
        if node in node_list:
            # 将node的度数 赋值给 heat属性
            G.nodes[node]['heat'] = len(G[node])
        else:
            # 其他节点赋值为0
            G.nodes[node]['heat'] = 0


def update_alpha(G):
    """
    更新节点的传热率
    :param G: 输入图
    """
    # 遍历图中节点
    for node in G:
        # 记录可传播节点数
        num = 0
        # 遍历当前节点邻居
        for adj_node in G[node]:
            if G.nodes[node]['heat'] > G.nodes[adj_node]['heat']:
                num += 1
        if num != 0:
            G.nodes[node]['alpha'] = 1 / (num + 1)
        else:
            G.nodes[node]['alpha'] = 0


def receive_heat(G):
    """
    接收热量
    :param G: 输入图
    """
    # 遍历图中节点
    for node in G:
        # 节点接受热量
        node_rh = 0
        # 遍历节点的邻居节点
        for adj_node in G[node]:
            if G.nodes[node]['heat'] < G.nodes[adj_node]['heat']:
                node_rh += G.nodes[adj_node]['heat'] * G.nodes[adj_node]['alpha']
        G.nodes[node]['node_rh'] = node_rh


def diffusion_heat(G):
    """
    扩散热量
    :param G: 输入图
    """
    for node in G:
        if G.nodes[node]['alpha']:
            G.nodes[node]['node_dh'] = (1 - G.nodes[node]['alpha']) * G.nodes[node]['heat']
        else:
            G.nodes[node]['node_dh'] = 0


def update_node_heat(G, t):
    """
    更新节点热量
    :param G: 输入图
    """
    # 冷却系数
    k = 1 - 0.5 * (t ** 0.06)
    # 散发系数
    r = np.power(np.e, -k * t)
    print(r)
    for node in G:
        G.nodes[node]['heat'] += G.nodes[node]['node_rh'] - G.nodes[node]['node_dh']
        # 散发过程
        G.nodes[node]['heat'] = G.nodes[node]['heat'] * r
        if G.nodes[node]['heat'] < 0.35:
            G.nodes[node]['heat'] = 0


def count_node(G):
    """
    对网络传播节点计数
    :param G: 输入图
    :return: 传播节点数目
    """
    count = 0
    for node in G:
        if G.nodes[node]['heat'] > 0:
            count += 1
    return count


if __name__ == '__main__':
    print('热传播模型')
    # 构建BA网络模型
    ba = nx.barabasi_albert_graph(150, 15)
    initial_node_heat(ba, 5)
    node_list = []
    t_list = np.linspace(0, 1, 8)
    for t in t_list:
        node_list.append(count_node(ba))
        update_alpha(ba)
        receive_heat(ba)
        diffusion_heat(ba)
        update_node_heat(ba, t)
    plt.plot(node_list, 'r-')
    plt.show()


