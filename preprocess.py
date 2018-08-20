import random
def class_3(x):
    if x=='':
        return 'C'
    x = int(x)
    if x<=20:
        return 'A'
    elif x<=40:
        return 'B'
    elif x<=60:
        return 'C'
    elif x<=80:
        return 'D'
    else:
        return 'E'

def class_15(x):
    x = float(x)
    if x<50:
        return 'A'
    elif x<100:
        return 'B'
    elif x<150:
        return 'C'
    elif x<200:
        return 'D'
    else:
        return 'E'

def class_16(x):
    if x=='':
        return 'C'
    x = float(x)
    if x<20:
        return 'A'
    elif x<50:
        return 'B'
    elif x<100:
        return 'C'
    elif x<200:
        return 'D'
    elif x<300:
        return 'E'
    else:
        return 'F'

def class_18(x):
    if x=='':
        return 'C'
    x = int(x)
    if x<600:
        return 'A'
    elif x<1000:
        return 'B'
    elif x<2000:
        return 'C'
    elif x<3000:
        return 'D'
    else:
        return 'E'

def class_28(x):
    if x=='':
        return 'C'
    x = float(x)
    if x<=0:
        return 'A'
    elif x<20:
        return 'B'
    elif x<40:
        return 'C'
    else:
        return 'D'

def class_30(x):
    x = int(x)
    if x<20150000:
        return 'A'
    elif x<20170000:
        return 'B'
    else:
        return 'C'

def class_34(x):
    if x=='':
        rand = random.randint(0, 3)
        if rand==0:
            return 'C'
        else:
            return 'B'
    x = float(x)
    if x<1000:
        return 'A'
    elif x<5000:
        return 'B'
    elif x<10000:
        return 'C'
    else:
        return 'D'

def class_36(x):
    if x=='':
        rand = random.randint(0, 4)
        if rand==0:
            return 'A'
        else:
            return 'B'
    x = float(x)
    if x<100:
        return 'A'
    elif x<200:
        return 'B'
    else:
        return 'C'

f = open('data/label_data_info_201804', 'r')
counter = []
counter2 = []
count = 0
for i in range(0,36):
    counter.append({'':0})
    counter2.append({'':0})
for line in f.readlines():
    line = line.strip().split('|')
    if line[20]=='':
        continue
    count += 1
    counter[6][line[6]] = counter[6].get(line[6], 0) + 1

f.close()
print(count)

f = open('data/label_data_info_201804', 'r')
output = open('data/processed_data_201804','w')

for line in f.readlines():
    line = line.strip().split('|')
    if line[20]=='':
        continue
    res = ''
    if line[1]=='':
        line[1] = '01'
    line[2] = class_3(line[2])
    if line[4]=='':
        line[4] = '0'
    if counter[6][line[6]]<200:
        line[6] = '00000000'
    if line[10] == '':
        line[10] = '1'
    line[14] = class_15(line[14])
    line[15] = class_16(line[15])
    line[17] = class_18(line[17])
    if line[18] =='':
        line[18] = '2'
    if line[21] =='':
        line[21] = '0'
    line[27] = class_28(line[27])
    line[29] = class_30(line[29])
    line[33] = class_34(line[33])
    line[35] = class_36(line[35])
    res = line[1]
    counter2[1][line[1]] = counter2[1].get(line[1], 0) + 1
    for i in range(2,36):
        if i==3 or i==11 or i==12 or i==13 or i==16 or i==19 \
        or i==22 or i==25 or i==30 or i==32 or i==31 or i==34:
            continue
        else:
            res += '|' + line[i]
            counter2[i][line[i]] = counter2[i].get(line[i], 0) + 1
    res += '|' + line[22] + '\n'
    counter2[22][line[22]] = counter2[22].get(line[22], 0) + 1
    output.write(res)

f.close()
output.close()

for i in range(0, 36):
    print(i+1, len(counter2[i]), counter2[i])