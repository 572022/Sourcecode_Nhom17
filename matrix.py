
from random import randint
from copy import deepcopy
import numpy as np

class Matrix():

    def __init__(self, lins, cols):
        self.matrix = np.zeros((lins,cols), dtype=int)
        self.dist = 0
        self.previous = None
        self.move = ""
        self.cost = 0
    #khởi tao ma trận với số số dòng và số cột được chỉ định. vaf các tham số như dist,previous,move,cost được khỏi tảo ban đầu
    def validNumbers(self, numbers):
        valid = False
        if len(numbers) == 9:
            ref = list(range(9))
            valid = True
            for i in numbers:
                if int(i) not in ref:
                    valid = False
                else: 
                    ref.remove(int(i))
        return valid
# Kiểm tra tính hợp lệ của dãy số nhập vào cho ma trận.
    def buildMatrix(self, str):
        numbers = str.split(",")
        if self.validNumbers(numbers):
            #kiểm tra chuỗi c hop le không
            i=0
            for k in range(3):
                for j in range(3):
                    self.matrix[k][j] = int(numbers[i])
                    i += 1
#Xây dựng ma trận từ một chuỗi dãy số đã cho.gán giá trị vào ma trận
    def searchBlock(self, value):
        for k in range(3):
            for j in range(3):
                if self.matrix[k][j] == value:
                    return (k,j)
                #tìm vị trí của ma trận sau đso in ra vị trí hg cột
    def moveup(self, zero):
        self.matrix[zero[0]][zero[1]] = self.matrix[zero[0]-1][zero[1]]
        self.matrix[zero[0]-1][zero[1]] = 0
    def movedown(self, zero):
        self.matrix[zero[0]][zero[1]] = self.matrix[zero[0]+1][zero[1]]
        self.matrix[zero[0]+1][zero[1]] = 0
    def moveright(self, zero):
        self.matrix[zero[0]][zero[1]] = self.matrix[zero[0]][zero[1]+1]
        self.matrix[zero[0]][zero[1]+1] = 0
    def moveleft(self, zero):
        self.matrix[zero[0]][zero[1]] = self.matrix[zero[0]][zero[1]-1]
        self.matrix[zero[0]][zero[1]-1] = 0
#di chuyển ô trong ma trận
    def getPossibleNodes(self, moves):
        zero = self.searchBlock(0)
        #tìm vị trí ô trống trong ma trận
        possibleNodes = []
        if zero[0] > 0:
            self.moveup(zero)
            moves.append("up")
            possibleNodes.append(deepcopy(self))
            #thêm vào danh node
            zero = self.searchBlock(0)
            self.movedown(zero)
            zero = self.searchBlock(0)
        if zero[0] < 2:
            self.movedown(zero)
            moves.append("down")
            possibleNodes.append(deepcopy(self))
            zero = self.searchBlock(0)
            self.moveup(zero)
            zero = self.searchBlock(0)
        if zero[1] > 0:
            self.moveleft(zero)
            moves.append("left")
            possibleNodes.append(deepcopy(self))
            zero = self.searchBlock(0)
            self.moveright(zero)
            zero = self.searchBlock(0)
        if zero[1] < 2:
            self.moveright(zero)
            moves.append("right")
            possibleNodes.append(deepcopy(self))
            zero = self.searchBlock(0)
            self.moveleft(zero)
            zero = self.searchBlock(0)
        return possibleNodes

    def getXY(self, value, matFinal = [[1,2,3],[4,5,6],[7,8,0]]):
        for x in range(3):
            for y in range(3):
                if value == matFinal[x][y]:
                    return (x,y)
# if giá trị bằng với ma trận mục tiêu thì trả về vị trí của value tương ứng
    
    def manhattanDist(self):
        res = 0
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] != 0:
                    fi, fj = self.getXY(self.matrix[i][j])
                    res += abs(fi - i) + abs(fj - j)
        self.dist = res
        return res
    #số bước di chuyển tối thiểu cần thiết để đưa mỗi ô về vị trí của nó trong trạng thái mục tiêu.
    # nếu ô hiện tại !0 thì lấy tọa độ của giá trị hiện tại.
    # manhattan tính ước lựng chi phí từ trạng thái hiện tại đến trạng thái mục tiêu

    def manhattanDistCost(self, Final):
        res = 0
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] != 0:
                    fi, fj = self.getXY(self.matrix[i][j], Final.matrix)
                    res += abs(fi - i) + abs(fj - j)
        return res
#được sử dụng khi cần phải tính toán ước lượng chi phí dựa trên.
    #Các khoảng cách này được tính bằng cách lấy hiệu giữa các chỉ số hàng và cột của ô trên hai ma trận và lấy giá trị
    # tuyệt đối của chúng, sau đó cộng tất cả các khoảng cách lại với nhau để đưa ra tổng chi phí ước lượng.
    # trạng thái mục tiêu mà không thay đổi trạng thái hiện tại.
    def getMatrix(self):
        return self.matrix
#ma trận hiện tại
    def isEqual(self, matrix):
        return (self.matrix == matrix).all()
#Phương thức này so sánh ma trận hiện tại với một ma trận khác được đưa vào dưới dạng tham số matrix.
    # Nó trả về True nếu hai ma trận bằng nhau và False nếu không.
    def setPrevious(self, p):
        self.previous = p
# Phương thức này so sánh hai đối tượng Matrix dựa trên giá trị dist. Trong trường hợp này,
    # nó so sánh hai đối tượng dựa trên giá trị dist của chúng.
    def __cmp__(self, other):
        return self.dist == other.dist

    def __lt__(self, other):
        return self.dist < other.dist
# xác định thứ tự và  so sánh các trạng thái của ma trận, trạng thái nho nhat thì dược xử lý đầu tiên