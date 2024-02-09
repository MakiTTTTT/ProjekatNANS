import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

data_dict = pickle.load(open('./data.pickle', 'rb'))

labels = np.asarray(data_dict['labels'])
data = np.asarray(data_dict['data'])

x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

model = RandomForestClassifier()

model.fit(x_train, y_train)

f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()
