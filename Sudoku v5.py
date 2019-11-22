import re
import copy

# 默认模板，非标准数独 - 1000次平均耗时5ms/次
sudoku_template1 = [[1,0,0,0,0,0,0,0,0],
                    [0,2,0,0,0,0,0,0,0],
                    [0,0,3,0,0,0,0,0,0],
                    [0,0,0,4,0,0,0,0,0],
                    [0,0,0,0,5,0,0,0,0],
                    [0,0,0,0,0,6,0,0,0],
                    [0,0,0,0,0,0,7,0,0],
                    [0,0,0,0,0,0,0,8,0],
                    [0,0,0,0,0,0,0,0,9]]


# 芬兰数学家英卡拉（Arto Inkala）设计的号称“最难数独” - 1000次平均耗时320ms/次
sudoku_template2 = [[8,0,0,0,0,0,0,0,0],
                    [0,0,3,6,0,0,0,0,0],
                    [0,7,0,0,9,0,2,0,0],
                    [0,5,0,0,0,7,0,0,0],
                    [0,0,0,0,4,5,7,0,0],
                    [0,0,0,1,0,0,0,3,0],
                    [0,0,1,0,0,0,0,6,8],
                    [0,0,8,5,0,0,0,1,0],
                    [0,9,0,0,0,0,4,0,0]]

def crack_it(sudoku=sudoku_template1):
    '''主函数，输入数独进行运算，如未输入则调用默认数独，格式为9x9的二维列表'''
    init_sudoku = str_to_num(copy.deepcopy(sudoku))   # Python的坑！列表或字典等对象作为函数参数时，函数可能修改其元素的指针，导致外部列表也会改变
    if is_valid_sudoku(sudoku):   # 判断输入的Sudoku是否合理（是否冲突）
        candidate_list = filter_candidate_list(init_sudoku, init_candidate_list(init_sudoku), start=0)   # 针对Sudoku中的每一个空格（空格都默认填入数字0），都算出其可能的备选数，存入data_list中；每当空格被确认唯一值时，剩余data_list都需要再被刷新
        cracked_sudoku = fill_blank(init_sudoku, candidate_list, start=0)   # 破解数独
        print_sudoku(cracked_sudoku)   # 在控制台显示已破解的数独，默认开启
        return cracked_sudoku
    else:
        return '请检查一下输入是否有误- -0'

def str_to_num(data):
    '''初步校验+统一格式，空字符转0，无效字符转0'''
    for i in range(9):
        for j in range(9):
            if re.match('[1-9]', str(data[i][j])):   # 1-9字符转int 1-9
                data[i][j] = int(data[i][j])
            elif re.match('', str(data[i][j])):   # 空位转int 0
                data[i][j] = 0
            else:   # 无效字符转int 0，或者也可以return False，拒绝服务
                data[i][j] = 0
    return data
                

def is_valid_sudoku(data):
    '''判断整个数独是否有效'''
    for y in range(9):
        for x in range(9):
            if data[y][x] > 9:
                return False

            if data[y][x] != 0 and data[y].count(data[y][x]) > 1:
                return False

            for col in range(9):
                if data[y][x] != 0 and col != y:
                    if data[col][x] == data[y][x]:
                        return False

            for i in range(3):
                for j in range(3):
                    if data[y][x] != 0 and (i+3*(y//3), j+3*(x//3)) != (y, x):
                        if data[i+3*(y//3)][j+3*(x//3)] == data[y][x]:
                            return False
    return True

def init_candidate_list(data):
    '''初始化建立一个数独的备选数列表，一个空格就对应其坐标以及填上1~9的备选数字，格式为81x9的二维列表'''
    data_list = []
    for y in range(9):
        for x in range(9):
            if data[y][x] == 0:
                data_list.append([(x, y), [1, 2, 3, 4, 5, 6, 7, 8, 9]])
    return data_list

def filter_candidate_list(data, data_list, start):
    '''对数独的备选数表进行过滤，删除无效的备选数'''
    for blank_index in range(start, len(data_list)):
        data_list[blank_index][1] = []
        for num in range(1,10):
            if is_valid_num(data, data_list[blank_index][0][0], data_list[blank_index][0][1], num):
                data_list[blank_index][1].append(num)
    return data_list

def is_valid_num(data, x, y, num):
    '''输入数独、坐标、数字，判断该位置填入该数字是否合理'''
    if data[y].count(num) > 0:   # 行判断
        return False

    for col in range(9):   # 列判断
        if data[col][x] == num:
            return False

    for a in range(3):   # 九宫格判断
        for b in range(3):
            if data[a+3*(y//3)][b+3*(x//3)] == num:
                return False
    return True

def fill_blank(data, data_list, start):
    '''
    核心函数，递归尝试代入备选数，类似深度优先遍历算法。
    一旦某位置填入为True（由is_valid_num函数判断），则开始下一位置的填入；若某位置填入为False，则return回上一级。
    参数解释：
    data: 数独矩阵，二维列表
    data_list: 备选数表，二维列表
    start: 递归进行的位置，对应data_list的下标
    '''
    all_data = []
    if start < len(data_list):
        one = data_list[start]
        for num in one[1]:
            if is_valid_num(data, one[0][0], one[0][1], num):
                data[one[0][1]][one[0][0]] = num   # 赋值，如果能给每一格成功赋值，则意味破解成功；如果出现失败，则需要将错误赋值清零
                # data_list = filter_candidate_list(data, data_list, start)   # 每一步赋值都会改变备选数表，但刷新备选数表的操作非常耗时，若加上这句，速度会慢100倍
                tem_data = fill_blank(data, data_list, start+1)   # start+1，使递归进入下一格点
                if tem_data:   # 注意！如果下一格点return，分两种情况：1.成功破解所有格点；2.发生错误，for loop结束也会return，此时返回值为None
                    return tem_data
        data[one[0][1]][one[0][0]] = 0   # 注意！可能向下递归了若干格才发现前面是错误的（即for loop结束，return None），此时需要将所有错误的赋值清零。
    else:
        return data

def print_sudoku(data):
    '''打印数独到控制台'''
    print('>>> 破解结果:')
    for i in range(9):
        for j in range(9):
            print('{:^3}'.format(data[i][j]), end='')
        print('')
    print('')

if __name__ == '__main__':
    crack_it()