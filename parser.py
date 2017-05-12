# you can write to stdout for debugging purposes, e.g.
# print "this is a debug message"

def solution(S):
    strs = S.split('\n')
    num_money={}
    num_time ={}
    max_time = 0
    max_num =""
    res = 0
    for str in strs:
        time_and_num = str.split(",")
        time = time_and_num[0].split(":")
        money = 0
        time_tmp = 0
        if (not time_and_num[1] in num_money.keys()):
            num_money[time_and_num[1]] = 0
            num_time[time_and_num[1]] = 0
        if (int(time[0])*3600+int(time[1])*60 + int(time[2]) <= 300):
            money += (int(time[1])*60+int(time[2]))*3
        else :
            money += (int(time[0])*60+int(time[1]))*150
            if (int(time[2]) > 0):
                money += 150
        time_tmp = (int(time[0])*3600+int(time[1])*60+int(time[2]))
        res += money
        tmp = num_money[time_and_num[1]]
        tmp += money
        num_money[time_and_num[1]] = tmp
        tmp = num_time[time_and_num[1]]
        tmp += time_tmp
        num_time[time_and_num[1]] = tmp
        if (tmp > max_time):
            max_time = tmp
            max_num += "a"
            max_num = time_and_num[1]
    res -= num_money[max_num]
    return res






def main():
    str = "00:01:07,400-234-090\n\
00:05:01,701-080-080\n\
00:05:00,400-234-090"
    print(solution(str))
main()
