from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
import tflearn
import tensorflow as tf
from imblearn.over_sampling import SMOTE
import time

def Create_Classifier(name):
	if(name=='LogReg'):
		return linear_model.LogisticRegression(n_jobs=1, C=1e5)
	elif(name=='KNN'):
		return KNeighborsClassifier(n_neighbors=3, n_jobs=1, algorithm='brute', metric='cosine')
	elif(name=='NB'):
		return MultinomialNB(alpha=0.01)
	elif(name=='MLPerceptron'):
		return MLPClassifier()
	else:
		raise NameError('Classifier Unavailable')

#Tensor Flow 

def fully_connected_layer(input, n_inp, n_out, relu=True):
    
    w=tf.Variable(tf.truncated_normal([n_inp,n_out], stddev=0.05))
    b=tf.Variable(tf.constant(0.05,shape=[n_out]))
    
    layer=tf.matmul(input,w)+b
    
    if(relu):
        layer=tf.nn.relu(layer)
    return layer

class SampleGenerator:
    
    def __init__(self,features,tags):
        
        self.ex_indices=[]
        self.feat=features
        self.tags=tags
    
    def getBatch(self,batch_size):
        
        count=0
        f=[]
        t=[]
        while(count<batch_size):
            
            if(len(self.ex_indices)==len(self.tags)):
                self.ex_indices=[]
            
            i=randint(0,len(self.tags)-1)
            if(i not in self.ex_indices):
                self.ex_indices.append(i)
                f.append(self.feat[i])
                t.append(self.tags[i])
                count+=1
        
        t=np.array(t)
        zer= np.zeros((batch_size,3))
        
        for i in range(len(t)):
            aux=t[i]
            zer[i][aux]=1
            
        f=np.array(f)
        return f, zer


def optimize(num_iterations):
    
    batch_size=64
    for i in range(num_iterations):
        
        f,t=sampleGenerator.getBatch(batch_size)
        feed_dict_train={ x:f, y_true:t}
        session.run(optimizer, feed_dict=feed_dict_train)
        
        if i % 100 == 0:
            # Calculate the accuracy on the training-set.
            acc = session.run(accuracy, feed_dict=feed_dict_train)

            # Message for printing.
            msg = "Optimization Iteration: {0:>6}, Training Accuracy: {1:>6.1%}"

            # Print it.
            print(msg.format(i + 1, acc))
            if(acc>=0.80):
                break