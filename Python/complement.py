import numpy as np
from collections import deque
import glob
from collections import deque
import pandas as pd

ENCODING = 'utf8' #ansiかutf8

files = glob.glob("CSV2/*.csv")
que = deque(maxlen=4)

for file in files:
    newdata = list()
    columns = list()
    with open(file, encoding='utf8') as f:

        while True:

            line = f.readline()

            if not line:

                if len(que)!=0:

                    comp_num = que.maxlen - len(que)
                    complines = np.empty((comp_num,4))

                    for i in range(0,4):

                        complines[:,i] = que[0][i]

                    newdata = np.vstack((newdata,np.array(que,dtype=np.float64)))
                    que.clear()


                break
            
            new_l = line.replace('\n','').split(',')

            if len(columns) == 0:
                #columns
                columns = new_l

            elif len(que)==0:
                que.append(new_l)

            elif que[0][2] != new_l[2]:
                
                comp_num = que.maxlen - len(que)
                complines = np.empty((comp_num,4))

                for i in range(0,4):

                    if i == 2 or i == 3:
                        complines[:,i] = que[0][i]

                    else:

                        if (int(que[0][2]) + 1) == (int(new_l[2])):
                            start = float(que[-1][i])
                            stop = float(new_l[i])
                            step = comp_num + 1
                            complines[:,i] = np.linspace(start, stop, step,endpoint=False,dtype=np.float64)[1:]

                        else:
                            complines[:,i] = que[0][i]

                if len(newdata) == 0:
                    newdata = np.array(que,dtype=np.float64)

                else:
                    newdata = np.vstack((newdata,np.array(que,dtype=np.float64)))

                newdata = np.vstack((newdata,complines))
                que.clear()

            if que.maxlen == len(que):

                newdata = np.vstack((newdata,np.array(que,dtype=np.float64)))
                que.clear()


df = pd.DataFrame(newdata, columns=columns)
df['temp'] = df['temp'].map('{:.6f}'.format)
df['humi'] = df['humi'].map('{:.6f}'.format)
df['weather'] = df['weather'].map('{:.6f}'.format)
df['time'] = df['time'].astype(int)

filename = file.replace('_rendered','')
filename = filename.replace('.csv','_rendered.csv')


df.to_csv(f'{filename}', index = False)
