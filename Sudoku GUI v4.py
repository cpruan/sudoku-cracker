import tkinter as tk
import re

def isRightSudoku(board):   #判断Sudoku数据是否有效
    for y in range(9):
        for x in range(9):
            if board[y][x] > 9:
                return False

            if board[y][x] != 0 and board[y].count(board[y][x]) > 1:
                return False

            for col in range(9):
                if board[y][x] != 0 and col != y:
                    if board[col][x] == board[y][x]:
                        return False

            for i in range(3):
                for j in range(3):
                    if board[y][x] != 0 and (i+3*(y//3), j+3*(x//3)) != (y, x):
                        if board[i+3*(y//3)][j+3*(x//3)] == board[y][x]:
                            return False
    return True

def get_sudoku():   #主程序
    window = tk.Tk()
    window.title('Solve a Sudoku')
    window.geometry('600x450')

    width = 3
    height = 1
    labels = []
    entrys = []
    sudoku = [[0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0]]

    for i in range(81):
        entrys.append(tk.Entry(window, width=width))   #初始化entrys
        labels.append(tk.Label(window, width=3, height=1, bg='yellow'))   #初始化labels

    l1 = tk.Label(window, text='How to solve a SUDOKU?', bg='yellow', font=('Arial',15))   #设计标题
    l1.place(x='170', y='15')
    b1 = tk.Button(window, text='Just click here', bg='white', activebackground='orange', font=('Arial',12), command=lambda: get_data())   #“运行”按钮
    b1.place(x='230', y='320')
    b2 = tk.Button(window, text='Clean up', bg='white', activebackground='orange', font=('Arial',12), command=lambda: clean_data())   #“清空”按钮
    b2.place(x='20', y='320')
    l0 = tk.Label(window, text='请检查输入是否过分...', font=('Arial',20))   #设计错误提示

    for e in entrys:
        e.place(x=str(entrys.index(e)%9*28+entrys.index(e)//3%3*6+20),
                y=str(entrys.index(e)//9*24+entrys.index(e)//27*6+70))   #GUI中用来将数独矩阵分割成9个九宫格

    def get_data(): #获取数独矩阵的值，并进行运算
        for e in entrys:
            sudoku[entrys.index(e)//9][entrys.index(e)%9] = int(e.get()) if re.match('\d+', e.get()) else 0   #获取你输入的数字，不合理数字或空白位置记为0
        if isRightSudoku(sudoku):   #判断输入的Sudoku是否合理（是否冲突）
            data = sudoku   #将输入的数独代入算法中计算
            data_list = data_list_filter(data, build_data_list(data), 0)   #针对Sudoku中的每一个空格子，都算出其可能的备选数字，存入data_list中；每当空格被确认唯一值时，剩余data_list都需要再被刷新
            newdata = fill_num(data, data_list, 0)   #计算得到完整数独newdata
            print_sudoku(newdata)   #程序输出数独newdata
            l0.place(x='-350', y='-150')
            for l in labels:
                labels[labels.index(l)]['text']= newdata[labels.index(l)//9][labels.index(l)%9]    #将完整数独的值代入label中
                l.place(x=str(labels.index(l)%9*28+labels.index(l)//3%3*6+300),
                        y=str(labels.index(l)//9*24+labels.index(l)//27*6+70))    #用labels将数独输出到GUI界面
        else:
            print('Input Error! 请检查输入是否过分...')
            for l in labels:
                l.place(x='-100', y='-100')
            l0.place(x='310', y='160')

    def clean_data():  #清空所有输入框
        for e in entrys:
            e.delete(0, 10)

    window.mainloop()

def print_sudoku(data): #打印最终数独破解结果
    for i in range(9):
        for j in range(9):
            print('{:^3}'.format(data[i][j]),end='')
        print('')
    print('')

def build_data_list(data): #初始化，未每个空位建立备选数字列表data_list
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

def data_list_filter(data, data_list, start):    #用来再次刷新备选数字
    for blank_index in range(start, len(data_list)):
        data_list[blank_index][1] = []
        for num in range(1,10):
            if judge(data, data_list[blank_index][0][0], data_list[blank_index][0][1], num):
                data_list[blank_index][1].append(num)
    return data_list

def fill_num(data, data_list, start):  #关键函数二，对具有多个备选数字的位置依次尝试。类似深度优先遍历算法，一旦某位置的数字judge为True，则允许开始下一位置的猜测；若某位置为False，则忽略。
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

if __name__ == '__main__':
    try:
        get_sudoku()
    except:
        print('Error occurred! please check your data~')
