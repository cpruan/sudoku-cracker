# sudoku-cracker

Use Python to crack sudoku.

2019/11/23: Update to v4 version (with GUI) and v5 version (without GUI, suitable for being called).

2019/11/23: 更新到v4和v5版本，前者带GUI，后者不带GUI适合被调用。

## 2018/01/17

版本V2，可破解中等难度数独（耗时约50~200ms），但对于超难数独不能短时破解，算法有待改善。
此外缺乏图形界面，输入有点麻烦（目前支持input手动输入数独的每一行，一共9行；或者直接修改程序中的default_data）。
以后可能会改成图形界面的...

## 2018/06/07

版本GUI v3，简单学习了tkinter库，做了个丑不拉几的GUI，不过重在实用吧。
注意哦，我还没有加入错误判断语句，以及对于超难的数独解题速度极慢，总之碰到这两种情况很可能会卡死、无响应，默默关掉重来就好...

## 2019/08/01

版本GUI v4，

1. 在v3基础上增加了错误判断，如果输入不合法会在右侧显示错误信息。

   ![image.png](https://i.loli.net/2019/11/23/iqBMGALoX2baIPs.png)

    

2. GUI方面增加了“Clean up”按钮，便于清除数字

   ![image.png](https://i.loli.net/2019/11/23/PqVs6lno7fT2LKZ.png)

## 2019/11/23

版本v5，

1. 修改了一些函数名，使其看起来更直观易懂。

例如：

v4中的**get_sudoku**函数：

```python
  def crack_it(sudoku=sudoku_template1):
      '''主函数，输入数独进行运算，如未输入则调用默认数独，格式为9x9的二维列表'''
```

  v4中的**fill_num**函数：

```python
  def fill_blank(data, data_list, start): 
      '''核心函数，递归尝试代入备选数'''
```

  

2. 取消了GUI，便于被其他程序调用，我的Django小站使用了这个版本。

   ![image.png](https://i.loli.net/2019/11/23/Y6myZhAKTXHgNf3.png)

   可以在线尝试一下：[暴力破解数独 - Pp's blog](https://cpruan.com/projects/script/cracking-sudoku/)

   大家若有需求，我可以在未来的Django Web仓库里讲解（咕咕咕...）
