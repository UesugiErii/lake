import numpy as np
import matplotlib.pyplot as plt

user_n = 943
movie_n = 1682
fold_n = 1  # 5 fold


def invert_f(count):
    """
    逆向云模型计算参数

    example:

     1 2 3 4 5
    (6,4,0,0,0)
    (0,0,0,5,5)
    (0,0,2,4,4)
    (4,6,0,0,0)

    [1.4        0.6015908  0.30861762]
    [4.5        0.62665707 0.33900043]
    [4.2        0.80212104 0.14551957]
    [1.6        0.6015908  0.30861762]

    论文中逆向云公式与上课PPT不同, 这里使用课件PPT上的公式

    :param count:

    count is a np.array with shape (5,)
    count[0] 代表用户给多少个电影打了1分
    count[1] 代表用户给多少个电影打了2分
    ....
    count[4] 代表用户给多少个电影打了5分

    :return:

    a np.array with shape (3,)

    ret[0] is Ex
    ret[1] is En
    ret[2] is He

    """

    N = np.sum(count)  # 评分总个数

    # 平均分
    sum_ = 0
    for i in range(1, 6):
        sum_ += count[i - 1] * i
    mean = sum_ / N

    # 一阶样本绝对中心矩
    sum_ = 0
    for i in range(1, 6):
        sum_ += np.abs(i - mean) * count[i - 1]
    diff1 = sum_ / N

    # 样本方差
    sum_ = 0
    for i in range(1, 6):
        sum_ += (i - mean) ** 2 * count[i - 1]
    diff2 = sum_ / (N - 1)

    ret = np.empty((3,), dtype=np.float32)
    ret[0] = mean
    ret[1] = (np.pi / 2) ** 0.5 * diff1
    ret[2] = abs(diff2 - ret[1] ** 2) ** 0.5

    return ret


def load_data():
    # MovieLens 100K
    # 由943个用户对1682个电影的10万条评分组成
    # 用户和电影从1号开始连续编号
    data = np.loadtxt(
        "./u.data",
        delimiter="\t",
        skiprows=1,
        dtype=np.int
    )[:, :3]

    #       train           test
    return data[:80000], data[80000:]


def process_data(train_data):
    # 统计各个用户的评分频度向量
    U = np.zeros((user_n, 5), dtype=np.float32)
    ratings = np.zeros((user_n, movie_n), dtype=np.int32)
    # dont use float32
    # it will make cpu 100%, int is faster
    for i in range(train_data.shape[0]):
        uid = train_data[i][0]
        mid = train_data[i][1]
        score = train_data[i][2]
        uid -= 1
        mid -= 1
        U[uid][score - 1] += 1
        ratings[uid][mid] = score

    # 将频度向量转为评分特征向量
    V = np.empty((user_n, 3), dtype=np.float32)
    for i in range(user_n):
        V[i] = invert_f(U[i])

    return ratings, V


def calc_loss(ratings, V, test_data, candidates_n=10):
    # 基于云模型的方法
    def find_similar_user(V, uid):
        uv = V[uid]  # user vector

        similarity = np.dot(uv, V.T) * -1  # -1 用来实现从大到小排序
        v_size = np.sum(V ** 2, axis=1) ** 0.5
        similarity /= v_size
        similarity /= np.sum(uv ** 2) ** 0.5
        candidates = similarity.argsort()
        return similarity * (-1), candidates

    def predict(ratings, V, uid, mid, candidates_n=10):
        uid -= 1
        mid -= 1
        # candidates_n  ->  Number of nearest-neighbours

        similarity, candidates = find_similar_user(V, uid)
        i = 1  # find index, 0 is uid self, so start from 1
        sum_ = 0  # (5)式分数的上半部分
        similarity_sum = 0
        while candidates_n and i < candidates.shape[0]:
            neighbor_uid = candidates[i]
            if ratings[neighbor_uid][mid]:  # 相似用户有评分
                sum_ += similarity[neighbor_uid] * (ratings[neighbor_uid][mid] - V[neighbor_uid][0])
                similarity_sum += abs(similarity[neighbor_uid])
                candidates_n -= 1
            i += 1

        if similarity_sum:
            return V[uid][0] + sum_ / similarity_sum
        else:
            # similarity_sum = 0, 即没有相似用户对此电影有评分
            return V[uid][0]

    loss = 0
    for i in range(test_data.shape[0]):
        uid = test_data[i][0]
        mid = test_data[i][1]
        score = test_data[i][2]
        loss += abs(score - predict(ratings, V, uid, mid, candidates_n))
    return loss / test_data.shape[0]


def calc_loss2(ratings, V, test_data, candidates_n=10):
    # 传统cosine方法(1)

    def find_similar_user(ratings, uid):
        # dont use this
        # ratings = ratings.astype(np.float32)

        uv = ratings[uid]  # user vector

        similarity = np.dot(uv, ratings.T).astype(np.float32) * -1  # -1 用来实现从大到小排序
        v_size = np.sum(ratings ** 2, axis=1).astype(np.float32) ** 0.5
        similarity /= v_size
        similarity /= np.sum(uv ** 2).astype(np.float32) ** 0.5
        candidates = similarity.argsort()
        return similarity * (-1), candidates

    def predict(ratings, V, uid, mid, candidates_n=10):
        uid -= 1
        mid -= 1
        # candidates_n  ->  Number of nearest-neighbours

        similarity, candidates = find_similar_user(ratings, uid)
        i = 1  # find index, 0 is uid self, so start from 1
        sum_ = 0  # (5)式分数的上半部分
        similarity_sum = 0
        while candidates_n and i < candidates.shape[0]:
            neighbor_uid = candidates[i]
            if ratings[neighbor_uid][mid]:  # 相似用户有评分
                sum_ += similarity[neighbor_uid] * (ratings[neighbor_uid][mid])
                similarity_sum += abs(similarity[neighbor_uid])
                candidates_n -= 1
            i += 1

        if similarity_sum:
            return sum_ / similarity_sum
        else:
            # similarity_sum = 0, 即没有相似用户对此电影有评分
            return 0

    loss = 0
    for i in range(test_data.shape[0]):
        uid = test_data[i][0]
        mid = test_data[i][1]
        score = test_data[i][2]
        loss += abs(score - predict(ratings, V, uid, mid, candidates_n))
    return loss / test_data.shape[0]


def calc_loss3(ratings, V, test_data, candidates_n=10):
    # 修正的余弦相似性(2)

    def find_similar_user(ratings, V, uid):
        ratings = ratings.astype(np.float32)
        for i in range(user_n):
            ratings[i][np.where(ratings[i] != 0)] -= V[i][0]
        uv = ratings[uid]  # user vector

        similarity = np.dot(uv, ratings.T) * -1  # -1 用来实现从大到小排序
        v_size = np.sum(ratings ** 2, axis=1) ** 0.5
        similarity /= v_size
        similarity /= np.sum(uv ** 2) ** 0.5
        candidates = similarity.argsort()
        return similarity * (-1), candidates

    def predict(ratings, V, uid, mid, candidates_n=10):
        uid -= 1
        mid -= 1
        # candidates_n  ->  Number of nearest-neighbours

        similarity, candidates = find_similar_user(ratings, V, uid)
        i = 1  # find index, 0 is uid self, so start from 1
        sum_ = 0  # (5)式分数的上半部分
        similarity_sum = 0
        while candidates_n and i < candidates.shape[0]:
            neighbor_uid = candidates[i]
            if ratings[neighbor_uid][mid]:  # 相似用户有评分
                sum_ += similarity[neighbor_uid] * (ratings[neighbor_uid][mid] - V[neighbor_uid][0])
                similarity_sum += abs(similarity[neighbor_uid])
                candidates_n -= 1
            i += 1

        if similarity_sum:
            return V[uid][0] + sum_ / similarity_sum
        else:
            # similarity_sum = 0, 即没有相似用户对此电影有评分
            return V[uid][0]

    loss = 0
    for i in range(test_data.shape[0]):
        uid = test_data[i][0]
        mid = test_data[i][1]
        score = test_data[i][2]
        loss += abs(score - predict(ratings, V, uid, mid, candidates_n))
    return loss / test_data.shape[0]


def main():
    plt_data_x = [i for i in range(10, 70, 10)]
    plt_data_y_LICM = [0] * len(plt_data_x)
    plt_data_y_cosine = [0] * len(plt_data_x)
    plt_data_y_adj_cos = [0] * len(plt_data_x)

    for i, neighbour_n in enumerate(plt_data_x):
        train_data, test_data = load_data()
        ratings, V = process_data(train_data)

        plt_data_y_LICM[i] += calc_loss(ratings, V, test_data, neighbour_n)
        plt_data_y_cosine[i] += calc_loss2(ratings, V, test_data, neighbour_n)
        plt_data_y_adj_cos[i] += calc_loss3(ratings, V, test_data, neighbour_n)

    for i in range(len(plt_data_x)):
        plt_data_y_LICM[i] /= fold_n
        plt_data_y_cosine[i] /= fold_n
        plt_data_y_adj_cos[i] /= fold_n

    print(plt_data_y_LICM)
    print(plt_data_y_cosine)
    print(plt_data_y_adj_cos)

    # BP-CF data is copy from paper
    plt_data_y_4 = [0.809, 0.792, 0.786, 0.787, 0.788, 0.789]

    plt.plot(plt_data_x, plt_data_y_LICM, c='r', marker="o", label='LICM-Based CF')
    plt.plot(plt_data_x, plt_data_y_cosine, c='b', marker="s", label='Cosine-Based CF')
    plt.plot(plt_data_x, plt_data_y_adj_cos, c='g', marker="^", label='Adjust Cosine-Based CF')
    plt.plot(plt_data_x, plt_data_y_4, c='c', marker="x", label='BP-CF')

    plt.legend()
    plt.savefig("result.png")


if __name__ == '__main__':
    main()


# 云模型
# [0.7777242985245753, 0.7649019271629508, 0.759399977005078, 0.7584570767348644, 0.7574269144956333, 0.7568756938455794]
# cosine
# [0.8214342388634586, 0.8086946549647708, 0.8065888937817799, 0.8073106732944716, 0.8075673566820236, 0.8079365110211246]
# adjust cosine
# [0.8308358509431902, 0.8293916974620071, 0.8353140441658793, 0.8417051565196165, 0.8481927012337407, 0.8543324226983553]
