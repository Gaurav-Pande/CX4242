from util import entropy, information_gain, partition_classes
import numpy as np
import ast

MAX_DEP = 20

class Node:
  def __init__(self,attr,value):
    self.left = None,
    self.right = None,
    self.split_attr = attr
    self.split_value = value
    self.isleaf = False

class LeafNode(Node):
    def __init__(self,category):
        self.category = category
        self.isleaf = True

def find_split_value(X,attr):
    ins = X[0]
    # print 'ins', ins, 'attr:', attr
    # print 'testing type', ins[attr]
    if isinstance(ins[attr], basestring):
        # print 'Categorical'
        values = {}
        # count all the possible values
        for idx in range(len(X)):
            try:
                values[ X[idx][attr] ] += 1 # increment the value
            except:
                values[ X[idx][attr] ] = 1 # initiate the value
        # get the most popular value
        occur = 0
        value = ''
        for key in values:
            if values[key] >= occur:
                occur = values[key]
                value = key
        return value

    else:
        # print 'Numerical'
        total = float(0)
        # count all the possible values
        for idx in range(len(X)):
            total += X[idx][attr]
        value = total / float(len(X))
        return value

def get_partition_para(X,y):
    best_gain = 0
    best_attr = 0
    # find possible partitions
    for split_attr in range(len(X[0])):
        split_value = find_split_value(X,split_attr)
        # print 'Split values:', split_value
        X_left, X_right, y_left, y_right = partition_classes(X,y,split_attr,split_value)
        y_curr = [y_left, y_right]
        gain = information_gain(y,y_curr)
        # print 'Information Gain:', gain
        if gain>best_gain:
            best_gain = gain
            best_attr = split_attr

    attr_split_value = find_split_value(X,best_attr)
    # print 'Best Attr:', best_attr, 'Split Value:', attr_split_value, 'Gain:', best_gain

    return best_attr, attr_split_value, best_gain

def majority(y):
    #find target attribute
    valFreq = {}
    #calculate frequency of values in target attr
    for cal in y:
        if (valFreq.has_key(cal)):
            valFreq[cal] += 1
        else:
            valFreq[cal] = 1
    max_occur = 0
    major = None
    for key in valFreq.keys():
        if valFreq[key]>max_occur:
            max_occur = valFreq[key]
            major = key
    return major

def make_tree(X,y,depth,MAX_DEP):
    # 1. when the depth already reached the max.
    if depth == MAX_DEP:
        # print 'max. depth leaf node'
        category = majority(y)
        node = LeafNode(category)
        return node

    # split the data
    split_attr, split_value, best_gain = get_partition_para(X,y)
    X_left, X_right, y_left, y_right = partition_classes(X,y,split_attr,split_value)
    # try:
    #     split_attr, split_value, best_gain = get_partition_para(X,y)
    #     X_left, X_right, y_left, y_right = partition_classes(X,y,split_attr,split_value)
    # except:
    #     # print X,y
    #     print 'error spliting the data'
    #     exit()

    # 2. when there is no left child or no right child
    if len(y_left) == 0 or len(y_right) == 0:
        # print 'leaf node'
        category = majority(y)
        node = LeafNode(category)
        return node

    # 3. when there are indeed two child nodes
    node = Node(split_attr,split_value)
    # print 'split on attr', split_attr, '>', split_value
    node.left = make_tree(X_left,y_left,depth+1,MAX_DEP)
    node.right = make_tree(X_right,y_right,depth+1,MAX_DEP)

    return node

def preorder_print(node, depth):
    if node.isleaf:
        print depth*' '+str(node.category)
    else:
        print depth*' '+'['+str(node.split_attr)+']>'+str(node.split_value)
        preorder_print(node.left,depth+1)
        preorder_print(node.right,depth+1)

def predict(node, rec):
    if (node.isleaf):
        # print 'class:', node.category
        return node.category
    if rec[node.split_attr]>node.split_value:
        # print 'right'
        return predict(node.right,rec)
    else:
        # print 'left'
        return predict(node.left,rec)

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        self.tree = []
        # self.tree = {}
        self.root = None
        # pass

    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree

        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        self.root = make_tree(X,y,0,MAX_DEP)
        # preorder_print(self.root, 0)


    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        return predict(self.root, record)

# Testing
if __name__ == '__main__':
    dt = DecisionTree()
    # X = [[3, 'aa', 10], [1, 'bb', 22], [2, 'cc', 28], [5, 'bb', 32], [4, 'cc', 32]]
    # y = [1,1,0,0,1]
    data = np.genfromtxt('hw4-data.csv', delimiter=',')
    X = data[1:,:-1]
    y = data[1:,-1]
    dt.learn(X,y)
    # preorder_print(dt.root, 0)
    y_predict = [dt.classify(rec) for rec in X]
    error = 0
    print len(y_predict), len(y)
    print X[0], y[0]
    # for idx, y_pred in enumerate(y_predict):
        # print idx, y_pred, y[idx]
        # if y_pred != y[idx]:
        #     print idx, y_pred, y[idx]
        #     error+=1
    # print 'trainning error', error
