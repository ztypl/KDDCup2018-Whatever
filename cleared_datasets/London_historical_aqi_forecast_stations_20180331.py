leastDict={'KC1': ['KF1', 'BL0', 'HR1', 'CT3', 'CR8', 'LH0', 'RB7'], 'CD1': ['MY7', 'CT2'], 'HV1': ['GN3', 'GN0', 'GB0', 'GR9', 'TH4', 'LW2', 'CD9'], 'CD9': ['LW2', 'TH4', 'GR9', 'GN0', 'GB0', 'GN3', 'HV1'], 'TD5': ['GR4', 'BX9', 'BX1'], 'GR4': ['BX9', 'BX1', 'TD5'], 'RB7': ['CT3', 'BL0', 'CR8', 'KF1', 'KC1', 'HR1', 'LH0'], 'TH4': ['LW2', 'GR9', 'GN0', 'GN3', 'GB0', 'CD9', 'HV1'], 'HR1': ['KF1', 'KC1', 'LH0', 'BL0', 'CT3', 'CR8', 'RB7'], 'BL0': ['CT3', 'KF1', 'KC1', 'CR8', 'HR1', 'RB7', 'LH0'], 'GR9': ['GB0', 'GN0', 'GN3', 'TH4', 'LW2', 'HV1', 'CD9'], 'ST5': [], 'LH0': ['HR1', 'KF1', 'KC1', 'BL0', 'CR8', 'CT3', 'RB7'], 'KF1': ['KC1', 'BL0', 'HR1', 'CT3', 'CR8', 'LH0', 'RB7'], 'MY7': ['CD1', 'CT2'], 'BX9': ['BX1', 'GR4', 'TD5'], 'GN3': ['GN0', 'GB0', 'GR9', 'TH4', 'HV1', 'LW2', 'CD9'], 'GN0': ['GN3', 'GB0', 'GR9', 'TH4', 'LW2', 'HV1', 'CD9'], 'CT2': ['MY7', 'CD1'], 'CT3': ['BL0', 'CR8', 'KF1', 'KC1', 'RB7', 'HR1', 'LH0'], 'LW2': ['TH4', 'GR9', 'CD9', 'GN0', 'GB0', 'GN3', 'HV1'], 'CR8': ['BL0', 'CT3', 'KF1', 'KC1', 'RB7', 'HR1', 'LH0'], 'BX1': ['BX9', 'GR4', 'TD5'], 'GB0': ['GN3', 'GN0', 'GR9', 'TH4', 'LW2', 'HV1', 'CD9']}
f=open('/Users/xuedi/course/ml/KDD/datasets/London_historical_aqi_forecast_stations_20180331.csv')
f2=open('/Users/xuedi/course/ml/KDD/cleared_datasets/London_historical_aqi_forecast_stations_20180331.csv','w')
cnt=0
dict={}
schema=f.readline()
f2.writelines(schema)
line=f.readline()
while line:
    tuple=line[:-2].split(',')
    if tuple[2] in dict:
        dict[tuple[2]].append(tuple)
    else:
        dict[tuple[2]]=[tuple]
    line=f.readline()

# 13*10897
# print len(dict)
# for item in dict:
#     print len(dict[item])


def getTimeApproximate(zone,i,j):
    sum=cnt=0
    if i>=3 and dict[zone][i-3][j]:
        sum+=float(dict[zone][i-3][j])
        cnt+=1
    if i>=2 and dict[zone][i-2][j]:
        sum+=float(dict[zone][i-2][j])
        cnt+=1
    if i>=1 and dict[zone][i-1][j]:
        sum+=float(dict[zone][i-1][j])
        cnt+=1
    if i+1<10897 and dict[zone][i+1][j]:
        sum+=float(dict[zone][i+1][j])
        cnt+=1
    if i+2<10897 and dict[zone][i+2][j]:
        sum+=float(dict[zone][i+2][j])
        cnt+=1
    if i+3<10897 and dict[zone][i+3][j]:
        sum+=float(dict[zone][i+3][j])
        cnt+=1
    if cnt==0:
        return 0
    return sum/cnt

def getGraphicalApproximate(zone,i,j):
    sum=cnt=0
    for nearZone in leastDict[zone]:
        if nearZone in dict and dict[nearZone][i][j]:
            sum+=float(dict[nearZone][i][j])
            cnt+=1
            if cnt==3:
                break
    if cnt==0:
        return 0
    return sum/cnt


for zone in dict:
    for i in range(10897):
        for j in range(6):
            if dict[zone][i][j]=='':
                a1=getTimeApproximate(zone,i,j)
                a2=getGraphicalApproximate(zone,i,j)
                if a1==0 and a2!=0:
                    dict[zone][i][j]=str(a2)
                elif a1!=0 and a2==0:
                    dict[zone][i][j]=str(a1)
                else:
                    dict[zone][i][j]=str((a1+a2)/2)
        f2.writelines(','.join(dict[zone][i])+'\n')

f.close()
f2.close()
