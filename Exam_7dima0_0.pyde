import math

# Settings
# Circle
# Rectangle
# Polygon
# Point
# Convex_polygon

objects = []

class Settings:
    operation = 'None'
    # pos selected figure
    pos = -1
    # current color in system RGB
    cl = {
          'R': 0, 
          'G': 0, 
          'B': 0
         }
    arr = []
    
    # count
    cnt = 0
    
    @classmethod
    def null(cls):
        cls.operation = 'None'
        cls.arr = []


class Circle:
    active = False
    name = 'Circle'
    def __init__(self, cl, x, y, r):
        self.cl = cl
        self.x = x
        self.y = y
        self.r = r
    
    def draw(self):
        fill(*self.cl)
        if self.active == True and Settings.cnt % 10 <= 4:
            stroke(255, 255, 255)
        else:
            stroke(0, 0, 0)
        circle(self.x, self.y, self.r)
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class Rectangle:
    active = False
    name = 'Rectangle'
    def __init__(self, cl, x, y, w, h):
        self.cl = cl
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def draw(self):
        fill(*self.cl)
        if self.active == True and Settings.cnt % 10 <= 4:
            stroke(255, 255, 255)
        else:
            stroke(0, 0, 0)
        rect(self.x, self.y, self.w, self.h)
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class Polygon:
    active = False
    name = 'Polygon'
    def __init__(self, cl, arr):
        self.cl = cl
        self.arr = arr
    
    def draw(self):
        fill(*self.cl)
        stroke(0, 0, 0)
        beginShape();
        for x, y in self.arr:
            vertex(x, y)
            circle(x, y, 5)
        vertex(self.arr[0][0], self.arr[0][1])
        endShape()

    def move(self, dx, dy):
        for i in range(len(self.arr)):
            self.arr[i] = (self.arr[i][0] + dx, self.arr[i][1] + dy)


class Point:
    # клас точка
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class ConvexPolygon:
    active = False
    name = 'ConvexPolygon'
    def __init__(self, cl, arr):
        self.cl = cl
        
        arr2 = []
        for x, y in arr:
            arr2.append(Point(x, y))
            
        self.arr = ConvexPolygon.make_shell(arr2)
        
    def draw(self):
        fill(*self.cl)
        if self.active == True and Settings.cnt % 10 <= 4:
            stroke(255, 255, 255)
        else:
            stroke(0, 0, 0)
        beginShape();
        for p in self.arr:
            vertex(p.x, p.y)
            circle(p.x, p.y, 5)
        vertex(self.arr[0].x, self.arr[0].y)
        endShape()
    
    def move(self, dx, dy):
        for i in range(len(self.arr)):
            self.arr[i].move(dx, dy)
    
    def is_inside(self, p):
        for i in range(len(self.arr)):            
            if i + 1 < len(self.arr):
                v = self.arr[i]
                to = self.arr[i+1]
                if self.check(p.x, p.y, v.x, v.y, to.x, to.y) < 0:
                    return False
            else:
                v = self.arr[i]
                to = self.arr[0]
                if self.check(p.x, p.y, v.x, v.y, to. x, to.y) < 0:
                    return False
        return True
        
    @staticmethod
    def check(x1, y1, x2, y2, x3, y3):
        res = ((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)) / 2
        return res
                
    @staticmethod
    def make_shell(arr):
        # алгоритм побудови опуклої оболонки
        
        def myfunc(e):
            return e.x
        
        arr.sort(key=myfunc)
        arr1 = []
        arr2 = []
        start = arr[0]
        end_ = arr[-1]
        
        cnt = 0
        for p in arr:
            if cnt == 0:
                cnt = 1
                continue
            if ConvexPolygon.check(start.x, start.y, end_.x, end_.y, p.x, p.y) <= 0:
                arr1.append(p)
            else:
                arr2.append(p)
        arr2.append(end_)
        
        res1 = [start, ]
        for p in arr1:
            while (len(res1) > 1) and (ConvexPolygon.check(res1[-2].x, res1[-2].y, p.x, p.y, res1[-1].x, res1[-1].y) >= 0):
                res1.pop()
            res1.append(p)
        
        res2 = [start, ]
        for p in arr2:
            while (len(res2) > 1) and (ConvexPolygon.check(res2[-2].x, res2[-2].y, p.x, p.y, res2[-1].x, res2[-1].y) <= 0):
                res2.pop()
            res2.append(p)
        
        res2.pop()
        res2.reverse()
        res2.pop()
        res = res1 + res2
        
        return res


def draw_palette():
    # palette
    fill(255, 255, 255)
    noStroke()
    rect(0, 0, 700, 61)
    line(0, 0, 0, 255)
    line(0, 20, 255, 20)
    line(0, 40, 255, 40)
    line(0, 60, 255, 60)
    line(255, 0, 255, 60)
    for i in range(1, 255):
        stroke(i, 0, 0)
        line(i, 1, i, 19)
        stroke(0, i, 0)
        line(i, 21, i, 39)
        stroke(0, 0, i)
        line(i, 41, i, 59)
    
    # rectangles
    rect(Settings.cl['R'], 0, 5, 20)
    rect(Settings.cl['G'], 20, 5, 20)
    rect(Settings.cl['B'], 40, 5, 20)
    
    # current color
    stroke(0, 0, 0)
    fill(Settings.cl['R'], Settings.cl['G'], Settings.cl['B'])
    circle(280, 30, 40)

def draw_frames():
    noStroke()
    fill(200, 228, 222)
    rect(0, 0, 700, 100)
    rect(0, 0, 75, 600)
    rect(626, 0, 75, 600)
    rect(0, 551, 700, 50)

def canvas_update():
    noStroke()
    fill(255, 255, 255)
    rect(0, 0, 700, 600)
    stroke(0, 0, 0)
    fill(255, 255, 255)
    rect(75, 100, 550, 450)

def draw_buttons():
    fill(255, 255, 255)
    stroke(0, 0, 0)
    line(375, 0, 375, 60)
    # circle
    circle(400, 30, 25)
    line(425, 0, 425, 60)
    # rectangle
    rect(435, 20, 30, 20)
    line(475, 0, 475, 60)
    # polygon
    new_polygon = Polygon((255, 255, 255), [
                                  (485, 14),
                                  (520, 20),
                                  (520, 40),
                                  (500, 30),
                                  (485, 40)
                                  ])
    new_polygon.draw()
    line(525, 0, 525, 60)
    # convex polygon
    new_conv_polygon = ConvexPolygon((255, 255, 255), [
                                  (540, 14),
                                  (555, 10),
                                  (570, 20),
                                  (570, 40),
                                  (550, 50),
                                  (535, 40)
                                  ])
    new_conv_polygon.draw()
    line(575, 0, 575, 60)
    # split
    fill(0, 0, 0)
    textSize(14)
    text('Split(P)', 578, 34)
    line(625, 0, 625, 60)
    # frames
    line(375, 0, 625, 0)
    line(375, 60, 625, 60)    


def update_color():
    if Settings.pos == -1:
        return
    objects[Settings.pos].cl = (Settings.cl['R'], Settings.cl['G'], Settings.cl['B'])

# distance between two points
def distance(x1, y1, x2, y2):
    
    def sqr(x):
        return x * x
    
    return math.sqrt(sqr(x2-x1) + sqr(y2-y1))

def selected(obj):
    if obj.name == 'Circle':
        if distance(mouseX, mouseY, obj.x, obj.y) * 2 <= obj.r:
            return True
    elif obj.name == 'Rectangle':
        if mouseX >= obj.x and mouseX <= obj.x + obj.w:
            if mouseY >= obj.y and mouseY <= obj.y + obj.h:
                return True
    elif obj.name == 'ConvexPolygon':
        if obj.is_inside(Point(mouseX, mouseY)):
            return True
    
    return False

def get_pos(x, y, arr):
    res = 10000
    for i in range(len(arr)):
        res = min(res, distance(x, y, arr[i].x, arr[i].y))
    for i in range(len(arr)):
        if res == distance(x, y, arr[i].x, arr[i].y):
            return i


def setup():
    size(700, 600)
    background(255, 255, 255)
    canvas_update()

def draw():
    if mousePressed:
        # select color
        if mouseX <= 255:
            if mouseY <= 20:
                Settings.cl['R'] = mouseX
                update_color()
            elif mouseY <= 40:
                Settings.cl['G'] = mouseX
                update_color()
            elif mouseY <= 60:
                Settings.cl['B'] = mouseX
                update_color()
        if mouseY <= 60:
            # set color
            obj = Circle((0, 0, 0), 280, 30, 40)
            if selected(obj):
                update_color()
            
            if mouseX >= 375:
                if mouseX <= 425:
                    Settings.operation = 'Creating circle...'
                    canvas_update()
                elif mouseX <= 475:
                    Settings.operation = 'Creating rectangle...'
                    canvas_update()
                elif mouseX <= 525:
                    Settings.operation = 'Creating polygon...'
                    canvas_update()
                elif mouseX <= 575:
                    Settings.operation = 'Creating convex polygon...'
                    canvas_update()
                elif mouseX <= 625:
                    Settings.operation = 'Spliting convex polygon...'
                    canvas_update()
            
        # select object
        if Settings.operation == 'None' and mouseY > 60:
            p = 0
            for obj in objects:
                if selected(obj):
                    if Settings.pos != -1:
                        objects[Settings.pos].active = False
                    Settings.pos = p
                    objects[Settings.pos].active = True
                    break
                p += 1
                if p == len(objects):
                    objects[Settings.pos].active = False
                    Settings.pos = -1

        if mouseX >= 75 and mouseX <= 625 and mouseY >= 100 and mouseY <= 550:
            # click for creating circle
            if Settings.operation == 'Creating circle...':
                if Settings.arr == []:
                    Settings.arr.append((mouseX, mouseY))        
            # click for creating rectangle
            if Settings.operation == 'Creating rectangle...':
                if Settings.arr == []:
                    Settings.arr.append((mouseX, mouseY))
            # click for split polygon
            if Settings.operation == 'Spliting convex polygon...':
                if Settings.arr == []:
                    Settings.arr.append((mouseX, mouseY))
        
        
    if keyPressed:
        # move
        if Settings.pos != -1:
            if key == 'w':
                objects[Settings.pos].move(0, -1)
            if key == 's':
                objects[Settings.pos].move(0, 1)
            if key == 'a':
                objects[Settings.pos].move(-1, 0)
            if key == 'd':
                objects[Settings.pos].move(1, 0)
            canvas_update()

        if key == 'f':
            if Settings.operation == 'Creating polygon...':
                Settings.arr.append((mouseX, mouseY))
            if Settings.operation == 'Creating convex polygon...':
                Settings.arr.append((mouseX, mouseY))
        
        # fix figures
        if key == ENTER:
            if Settings.operation == 'Creating circle...':
                radius = distance(mouseX, mouseY, Settings.arr[-1][0], Settings.arr[-1][1])
                new_obj = Circle((Settings.cl['R'], Settings.cl['G'], Settings.cl['B']), Settings.arr[-1][0], Settings.arr[-1][1], radius)
                objects.append(new_obj)
                canvas_update()
                Settings.null()
            if Settings.operation == 'Creating rectangle...':
                x1 = min(mouseX, Settings.arr[-1][0])
                y1 = min(mouseY, Settings.arr[-1][1])
                x2 = max(mouseX, Settings.arr[-1][0])
                y2 = max(mouseY, Settings.arr[-1][1])
                new_obj = Rectangle((Settings.cl['R'], Settings.cl['G'], Settings.cl['B']), x1, y1, x2-x1, y2-y1)
                objects.append(new_obj)
                canvas_update()
                Settings.null()
            if Settings.operation == 'Creating polygon...':
                new_obj = Polygon((Settings.cl['R'], Settings.cl['G'], Settings.cl['B']), Settings.arr)
                objects.append(new_obj)
                canvas_update()
                Settings.null()
            if Settings.operation == 'Creating convex polygon...':
                new_obj = ConvexPolygon((Settings.cl['R'], Settings.cl['G'], Settings.cl['B']), Settings.arr)
                objects.append(new_obj)
                canvas_update()
                Settings.null()
            if Settings.operation == 'Spliting convex polygon...':
                x1 = Settings.arr[-1][0]
                y1 = Settings.arr[-1][1]
                x2 = mouseX
                y2 = mouseY
                p = Settings.pos
                if objects[p].name == 'ConvexPolygon':
                    Settings.cl['R'] = objects[p].cl[0]
                    Settings.cl['G'] = objects[p].cl[1]
                    Settings.cl['B'] = objects[p].cl[2]
                    arr_ = objects[p].arr
                    p1, p2 = get_pos(x1, y1, arr_), get_pos(x2, y2, arr_)
                    pos1 = min(p1, p2)
                    pos2 = max(p1, p2)
                    arr1 = []
                    for i in range(pos1, pos2+1):
                        arr1.append(arr_[i])
                    arr2 = []
                    for i in range(pos2, len(arr_)):
                        arr2.append((arr_[i].x, arr_[i].y))
                    for i in range(pos1+1):
                        arr2.append((arr_[i].x, arr_[i].y))
                
                    objects[p].arr = arr1
                    new_obj = ConvexPolygon((Settings.cl['R'], Settings.cl['G'], Settings.cl['B']), arr2)
                    objects.append(new_obj)
                    canvas_update()
                    Settings.null()
            
    # interactive creating objects
    # creating circle
    if Settings.operation == 'Creating circle...' and Settings.arr != []:
        radius = distance(mouseX, mouseY, Settings.arr[-1][0], Settings.arr[-1][1])
        canvas_update()
        fill(Settings.cl['R'], Settings.cl['G'], Settings.cl['B'])
        circle(Settings.arr[-1][0], Settings.arr[-1][1], radius)
    # creating rectangle
    if Settings.operation == 'Creating rectangle...' and Settings.arr != []:
        x1 = min(mouseX, Settings.arr[-1][0])
        y1 = min(mouseY, Settings.arr[-1][1])
        x2 = max(mouseX, Settings.arr[-1][0])
        y2 = max(mouseY, Settings.arr[-1][1])
        canvas_update()
        fill(Settings.cl['R'], Settings.cl['G'], Settings.cl['B'])
        rect(x1, y1, x2-x1, y2-y1)
    # creating polygon
    if Settings.operation == 'Creating polygon...' and Settings.arr != []:
        if len(Settings.arr) != 1:
            line(Settings.arr[-2][0], Settings.arr[-2][1], Settings.arr[-1][0], Settings.arr[-1][1])
        circle(Settings.arr[-1][0], Settings.arr[-1][1], 5)
    # creating convex polygon
    if Settings.operation == 'Creating convex polygon...' and Settings.arr != []:
        if len(Settings.arr) != 1:
            line(Settings.arr[-2][0], Settings.arr[-2][1], Settings.arr[-1][0], Settings.arr[-1][1])
        circle(Settings.arr[-1][0], Settings.arr[-1][1], 5)
    
    # draw all objects and canvas
    for obj in objects:
        obj.draw()
    draw_frames()
    draw_palette()
    draw_buttons()
    
    # information about current operation
    fill(255, 0, 0)
    textSize(20)
    text(Settings.operation, (700 - len(Settings.operation) * 7) // 2, 580)
    
    # count
    Settings.cnt += 1
