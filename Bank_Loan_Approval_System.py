#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv

training_data1 = []
with open('C:/Users/HP/Downloads/dt3.csv') as f:
    reader = csv.reader(f, delimiter=',')
    header = next(reader)
    for row in reader:
        rows = [[(row[0]),(row[1]),(row[2]), int(row[3]), (row[4]), (row[5]), int(row[6]), 
            int(row[7]), int(row[8]), int(row[9]), (row[10]), (row[11])] for row in reader]

for row in rows:
    training_data1.append(row)
    
print("Headers found in csv:")
print(header)    
print("Training data used:")    
print(training_data1) 

#header= ["Loan_ID", "Gender", "Married","Dependents","Education",
#"Self_Employed","ApplicantIncome","CoapplicantIncome","LoanAmount",
#"Loan_Amount_Term","Property_Area","Loan_Status"]


# In[3]:


def unique_vals(rows, col):
    return set([row[col] for row in rows])


# In[4]:


def class_counts(rows):
    counts = {}  
    for row in rows:
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)


# In[5]:


class Question:
    def __init__(self, column, value):
        self.column = column
        self.value = value
        
    def match(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value
    def __repr__(self):
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))


# In[6]:


def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


# In[7]:


def gini(rows):
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity = impurity - prob_of_lbl**2
    return impurity


# In[8]:


def info_gain(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)


# In[9]:


def find_best_split(rows):
    best_gain = 0  
    best_question = None  
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1  
    
    for col in range(n_features):  
        values = set([row[col] for row in rows])  
        for val in values:  
            question = Question(col, val)
            true_rows, false_rows = partition(rows, question)
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue
            gain = info_gain(true_rows, false_rows, current_uncertainty)
            if gain >= best_gain:
                best_gain, best_question = gain, question
    return best_gain, best_question


# In[10]:


from ipywidgets import widgets,Layout
from IPython.display import display

class Leaf:
    def __init__(self, rows):
        self.predictions = class_counts(rows)

class Decision_Node:
    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch

def build_tree(rows):
    gain, question = find_best_split(rows)
    if gain == 0:
        return Leaf(rows)
    true_rows, false_rows = partition(rows, question)
    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)
    return Decision_Node(question, true_branch, false_branch)

def print_tree(node, spacing=""):
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return
    print (spacing + str(node.question))
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")
    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")

def classify(row, node):
    if isinstance(node, Leaf):
        return node.predictions
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)

def print_leaf(counts):
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs

if __name__ == '__main__':
    my_tree = build_tree(training_data1)
    print_tree(my_tree)
    #following is a 2-D array
    #loan id
    text0=widgets.Text(description="Loan ID:",placeholder='Enter Loan ID')
    display(text0)
    #gender
    w0=widgets.RadioButtons(
        options=['Male', 'Female'],
        description='\nGender:\n',
        layout=Layout(width='100%', height='100%'),
        disabled=False
    )
    def on_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            print(change['new'])
    w0.observe(on_change)
    display(w0)

#marital status
    w1=widgets.RadioButtons(
        options=['Yes', 'No'],
        description='\nMarried?\n',
        disabled=False
    )
    def on_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            print(change['new'])
    w1.observe(on_change)
    display(w1)

#education
    w2= widgets.Dropdown(
        options=['0', '1', '2'],
        value='0',
        description='Dependents:',
    )
    def on_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            print(change['new'])
    w2.observe(on_change)
    display(w2)

#education
    w3=widgets.RadioButtons(
        options=['Graduate', 'Not_Graduate'],
        description='\nEducation:',
        disabled=False
    )
    def on_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            print(change['new'])
    w3.observe(on_change)
    display(w3)

#self-employed
    w4=widgets.RadioButtons(
        options=['Yes', 'No'],
        description='\nSelf-employed?\n',
        disabled=False
    )
    def on_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            print(change['new'])
    w4.observe(on_change)
    display(w4)

#text-boxes
    text1=widgets.Text(description="App. Income:",placeholder='Enter Applicant\'s income')
    display(text1)
    text2=widgets.Text(description="Co-App. Income:",placeholder='Enter the Co-Applicant\'s income')
    display(text2)
    text3=widgets.Text(description="Loan Amount:",placeholder='Enter the Loan Amount')
    display(text3)
    text4=widgets.Text(description="Loan Term:",placeholder='Enter the Loan Amount term')
    display(text4)

#property area
    w5= widgets.Dropdown(
        options=['Urban', 'Semiurban', 'Rural'],
        value='Urban',
        description='Area:',
    )
    def on_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            print(change['new'])
    w5.observe(on_change)
    display(w5)

#button
    button = widgets.Button(description="Submit")
    display(button)
    a=[]
    def on_button_clicked(b):
        a.append(text0.value)
        a.append(w0.value)
        a.append(w1.value)
        a.append(int(w2.value))
        a.append(w3.value)
        a.append(w4.value)
        a.append(int(text1.value))
        a.append(int(text2.value))
        a.append(int(text3.value))
        a.append(int(text4.value))
        a.append(w5.value)
        a.append('Y')
        testing_data=[a]
        print(testing_data)
        for row in testing_data:
            #print("Actual: %s. Predicted: %s" %
               #(row[-1], print_leaf(classify(row, my_tree))))
            print("Predicted: %s" %
               (print_leaf(classify(row, my_tree))))
            
    button.on_click(on_button_clicked)


# In[ ]:




