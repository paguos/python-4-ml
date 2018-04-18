def decision(x):
    # >>>>> YOUR CODE HERE
    smoker = x[0]
    age = x[1]
    diet = x[2]
    
    if smoker == 'yes':
        if age < 29.5:
            return 'less'
        else:
            return 'more'
    else:
        if diet == 'good':
            return 'less'
        else:
            return 'more'
    # <<<<< END YOUR CODE

def gettest():
    # >>>>> YOUR CODE HERE
    with open('health-test.txt', 'r') as f:
        l = []
        for line in f:
            data = line.split(",")
            l.append((data[0], data[1], data[2].replace("\n", "")))
        return l

def evaluate_testset():
    # >>>>> YOUR CODE HERE
    data_list = gettest()
    count = 0.0
    for data in data_list:
        if decision(data) == 'more':
            count = count + 1
    return count / len(data_list)
    # <<<<< END YOUR CODE

def gettrain():
    # >>>>> YOUR CODE HERE
    with open('health-train.txt', 'r') as f:
        l = []
        for line in f:
            data = line.split(",")
            l.append([(data[0], data[1], data[2]), data[3].replace("\n", "")])
        return l
    # <<<<< END YOUR CODE

def neighbor(x, trainset):
    # >>>>> YOUR CODE HERE
    label = ''
    min_dis = float('inf')

    for data in trainset:
        y = data[0]
        dis = (y[0] != x[0]) + ((int(y[1]) - int(x[1])) / 50.0) ** 2 + (y[2] != x[2])

        if dis < min_dis:
            min_dis = dis
            label = data[1]
    return label

    # <<<<< END YOUR CODE

def compare():
    # >>>>> YOUR CODE HERE
    data_set = gettest()
    Xdisagree = []

    for data in data_set:
        d = decision(data)
        n = neighbor(data, gettrain())
        if d != n:
            Xdisagree.append(data)

    probability = (float(len(Xdisagree)) / len(data_set))

    # <<<<< END YOUR CODE
    return Xdisagree, probability

class NearestMeanClassifier:
    def train(self, dataset):
        # >>>>> YOUR CODE HERE
        more = {'smoker': 0.0, 'age' : 0.0, 'diet' : 0.0}
        less = {'smoker': 0.0, 'age' : 0.0, 'diet' : 0.0}

        count_more = 0
        count_less = 0

        for data in dataset:
            label = data[1]
            smoker = 1.0 if data[0][0] == 'yes' else 0.0
            age = float(data[0][1])
            diet = 1.0 if data[0][2] == 'good' else 0.0

            if label == 'more':
                more['smoker'] = more['smoker'] + smoker
                more['age'] = more['age'] + age
                more['diet'] = more['diet'] + diet
                count_more = count_more + 1
            elif label == 'less':
                less['smoker'] = more['smoker'] + smoker
                less['age'] = more['age'] + age
                less['diet'] = more['diet'] + diet
                count_less = count_less + 1

        l_more = count_more
        self.more = {'smoker': (more['smoker'] / l_more), 'age' : (more['age'] / l_more), 'diet' : (more['diet'] / l_more)}
        l_less = count_less
        self.less = {'smoker': (less['smoker'] / l_less), 'age' : (less['age'] / l_less), 'diet' : (less['diet'] / l_less)}    
        # <<<<< END YOUR CODE

    def predict(self, x):
        # >>>>> YOUR CODE HERE
        smoker = 1.0 if x[0] == 'yes' else 0.0
        age = float(x[1])
        diet = 1.0 if x[2] == 'good' else 0.0 

        x = [smoker, age, diet]

        a = [self.more['smoker'], self.more['age'], self.more['diet']]
        dis_more = (a[0] - x[0]) ** 2 + ((a[1] - x[1]) / 50.0) ** 2 + (a[2] - x[2]) ** 2
        a = [self.less['smoker'], self.less['age'], self.less['diet']]
        dis_less = (a[0] - x[0]) ** 2 + ((a[1] - x[1]) / 50.0) ** 2 + (a[2] - x[2]) ** 2
        
        if dis_more > dis_less:
            return 'more'
        else:
            return 'less'
        # <<<<< END YOUR CODE

def build_and_train():
    # >>>>> YOUR CODE HERE
    c = NearestMeanClassifier()
    c.train(gettrain())
    return c
    # <<<<< END YOUR CODE

def predict_test():
    # >>>>> YOUR CODE HERE
    dataset = gettest()
    agreed_samples = []
    classifier = build_and_train()

    for data in dataset:
        d = decision(data)
        n = neighbor(data, gettrain())
        c = classifier.predict(data)

        if d == n and n == c:
            agreed_samples.append(data)
    # <<<<< END YOUR CODE
    return agreed_samples