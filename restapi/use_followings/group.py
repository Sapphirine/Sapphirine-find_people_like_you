import os
i = 0


result = open('/DIR/group.txt', 'r')
for line in result.readlines():
    i = i+1
    line = line.strip('\n')
    line = line.strip(')')
    group_id = int(line.split(' ')[-1])
    os.rename("/DIR/%d.txt" %(i), "/DIR/group%d/%d.txt" %(group_id, i))
