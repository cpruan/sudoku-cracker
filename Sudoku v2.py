
default_data = [[1 ,0 ,6 ,2 ,0 ,0 ,0 ,0 ,0 ],  #默认赠送一个数独.游戏模式选择“1”时，可修改此数独进行游戏（数独空处请填0）。
                [0 ,0 ,0 ,4 ,0 ,0 ,8 ,2 ,0 ],
                [2 ,0 ,0 ,0 ,0 ,5 ,0 ,0 ,0 ],
                [0 ,8 ,0 ,0 ,4 ,0 ,0 ,0 ,7 ],
                [0 ,0 ,0 ,6 ,0 ,3 ,0 ,0 ,0 ],
                [5 ,0 ,0 ,0 ,1 ,0 ,0 ,4 ,0 ],
                [0 ,0 ,0 ,9 ,0 ,0 ,0 ,0 ,0 ],
                [0 ,3 ,9 ,0 ,0 ,4 ,0 ,0 ,0 ],
                [0 ,0 ,0 ,0 ,0 ,2 ,9 ,0 ,5 ]]

def get_data():  #初始化，输入数独数据data
    data = []
    for n in range(9):
        data.append(list(map(int, input('Enter {}th line:'.format(n+1)).split())))
    print('Your data:')
    print_sudoku(data)
    return data

def interface():  #提高用户体验
    print('***Method 1: Modify the default sudoku***')
    print('***Method 2: Through input method***\n')
    while True:
        choice = input('Please select the data input method：1 or 2\n')
        if choice == '1':
            data = default_data
            break
        elif choice == '2':
            while True:
                data = get_data()
                check = input('Confirm? Y or N\n')
                if check == 'Y' or check == 'y':
                    break
            break
        else:
            print('Error, chooce again~')
    return data

def print_sudoku(data): #打印最终数独破解结果
    for i in range(9):
        for j in range(9):
            print('{:^3}'.format(data[i][j]),end='')
        print('')

def build_data_list(data): #初始化，未每个空位建立备选数字列表
    data_list = []
    for y in range(9):
        for x in range(9):
            if data[y][x] == 0:
                data_list.append([(x, y), [1, 2, 3, 4, 5, 6, 7, 8, 9]])
    return data_list

def judge(data, x, y, num): #关键函数一，判断数字是否重复，是否允许填入
    if data[y].count(num) > 0: #行判断
        #print('error1')
        return False

    for col in range(9): #列判断
        if data[col][x] == num:
            #print('error2')
            return False

    for a in range(3): #九宫格判断
        for b in range(3):
            if data[a+3*(y//3)][b+3*(x//3)] == num:
                #print('error3')
                return False
    return True

def data_list_filter(data, data_list, start):
    for blank_index in range(start, len(data_list)):
        data_list[blank_index][1] = []
        for num in range(1,10):
            if judge(data, data_list[blank_index][0][0], data_list[blank_index][0][1], num):
                data_list[blank_index][1].append(num)
    return data_list

def fill_num(data, data_list, start):  #关键函数二，对有多个备选数字的位置循环猜数字。类似深度优先遍历算法，一旦某位置的数字judge为True，则允许开始下一位置的猜测；若某位置为False，则忽略。
    if start < len(data_list):
        one = data_list[start]
        for num in one[1]:
            if judge(data, one[0][0], one[0][1], num):
                data[one[0][1]][one[0][0]] = num
                tem_data = fill_num(data, data_list, start+1)
                if tem_data != None:
                    return tem_data
        data[one[0][1]][one[0][0]] = 0  #有可能再往后猜了好几步后才发现前面错误，此时需要将过程中的所有赋值操作清零。
    else:
        return data

def main(): #主函数
    try:
        data = interface()
        data_list = data_list_filter(data, build_data_list(data), 0)
        newdata = fill_num(data, data_list, 0)
        print('Answer:')
        print_sudoku(newdata)
    except:
        print('Error occurred! please check your data~')

main()
