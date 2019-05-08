import glob
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import math
# from collections import deque
# import pygame
# TODO fix loading

path1 = '/home/emsala/Documenten/Media Distillery/replay-recognition/reoccurence-dataset/20180813_1200/frames'
path2 = '/home/emsala/Documenten/Media Distillery/replay-recognition/reoccurence-dataset/20180813_1500/frames'


class CreateSimilarityMatrix():

    def __init__(self, path1, path2):
        self.path_x = path1
        self.path_y = path2
        self.list_of_imgpaths_x = list()
        self.list_of_imgpaths_y = list()
        self.nr_of_img_x = 0
        self.nr_of_img_y = 0

        self.img_size = 500

        self.row_x_1 = []
        self.row_x_2 = []
        self.row_x_3 = []
        self.row_x_4 = []
        self.row_y_1 = []
        self.row_y_2 = []
        self.row_y_3 = []
        self.row_y_4 = []
        self.number_of_rows = 4

        self.merged_imgs = 0

        self.get_lists_of_frames()

        self.x = 0 #list_of_imgpaths_y
        self.y = 0 #list_of_imgpaths_x

        self.f = plt.figure()
        self.selected_files = []
        self.ax = self.f.add_subplot(111)
        self.cid = self.f.canvas.mpl_connect('button_press_event',
                                   lambda event: self.onclick(event))
        self.cid2 = self.f.canvas.mpl_connect('key_press_event',
                                   lambda event: self.onkey(event))
        self.similarity_matrix = np.zeros(shape=(self.nr_of_img_y, self.nr_of_img_y))
        #self.similarity_matrix = np.load('/home/emsala/plots/similarity_matrix.txt')


    def reuse_similarity_matrix(self):
        myfile = 'similarity_matrix.txt'
        # data = np.loadtxt(myfile, dtype=int)
        data = np.zeros(shape=(len(self.list_of_imgpaths_y), len(self.list_of_imgpaths_x)))
        print(data)
        return data

    def get_lists_of_frames(self):
        list_of_imgpaths_y = sorted(glob.glob(self.path_y + '/*'))
        list_of_imgpaths_x = sorted(glob.glob(self.path_x + '/*'))
        self.list_of_imgpaths_y = [imgpath for imgpath in list_of_imgpaths_y if imgpath.endswith('.jpg')]
        self.list_of_imgpaths_x = [imgpath for imgpath in list_of_imgpaths_x if imgpath.endswith('.jpg')]
        self.nr_of_img_y = len(self.list_of_imgpaths_y)
        self.nr_of_img_x = len(self.list_of_imgpaths_x)

    def select_images_to_plot(self):
        """stack 3 rows of 20 images per folder as to compare 60 images of folder ´x' with 60 images of folder 'y' """
        for i in range(0, 20):
            self.row_y_1.append(cv2.resize(cv2.imread(self.list_of_imgpaths_y[self.y + i]), (self.img_size,self.img_size)))
            self.row_x_1.append(cv2.resize(cv2.imread(self.list_of_imgpaths_x[self.x + i]), (self.img_size, self.img_size)))
        self.row_y_1 = np.hstack(self.row_y_1)
        self.row_x_1 = np.hstack(self.row_x_1)

        for i in range(20, 40):
            self.row_y_2.append(cv2.resize(cv2.imread(self.list_of_imgpaths_y[self.y + i]), (self.img_size, self.img_size)))
            self.row_x_2.append(cv2.resize(cv2.imread(self.list_of_imgpaths_x[self.x + i]), (self.img_size, self.img_size)))
        self.row_y_2 = np.hstack(self.row_y_2)
        self.row_x_2 = np.hstack(self.row_x_2)

        for i in range(40, 60):
            self.row_y_3.append(cv2.resize(cv2.imread(self.list_of_imgpaths_y[self.y + i]), (self.img_size, self.img_size)))
            self.row_x_3.append(cv2.resize(cv2.imread(self.list_of_imgpaths_x[self.x + i]), (self.img_size, self.img_size)))
        self.row_y_3 = np.hstack(self.row_y_3)
        self.row_x_3 = np.hstack(self.row_x_3)

        for i in range(60, 80):
            self.row_y_4.append(cv2.resize(cv2.imread(self.list_of_imgpaths_y[self.y + i]), (self.img_size, self.img_size)))
            self.row_x_4.append(cv2.resize(cv2.imread(self.list_of_imgpaths_x[self.x + i]), (self.img_size, self.img_size)))
        self.row_y_4 = np.hstack(self.row_y_4)
        self.row_x_4 = np.hstack(self.row_x_4)

        merged_img_rows_y = np.vstack((self.row_y_1, self.row_y_2, self.row_y_3, self.row_y_4))
        merged_img_rows_x = np.vstack((self.row_x_1, self.row_x_2, self.row_x_3, self.row_x_4))
        self.merged_imgs = np.vstack((merged_img_rows_y, merged_img_rows_x))
        self.merged_imgs = cv2.cvtColor(self.merged_imgs, cv2.COLOR_BGR2RGB)

    def plot(self):
        self.select_images_to_plot()
        self.ax = self.f.add_subplot(111)
        self.ax.imshow(self.merged_imgs)
        plt.show()


    def onclick(self, event):
        if event.button == 1:
            img_index = self.round_img_index(event.xdata)
            path_index = self.round_path_index(event.ydata)
            self.selected_files.append([path_index, img_index])
            print(self.selected_files)

    def files_to_matrix(self):
        indexes_y = [selected_file[1] for selected_file in self.selected_files if selected_file[0] == 'y']
        print(indexes_y)
        indexes_x = [selected_file[1] for selected_file in self.selected_files if selected_file[0] == 'x']
        print(indexes_x)

        for index_y in indexes_y:
            for index_x in indexes_x:
                self.similarity_matrix[index_y, index_x] = 1
                print('changed')


    def onkey(self, event):
        if event.key == 'right':
            self.x += 60
            plt.clf()
            self.plot()
        elif event.key == 'left':
            self.x -= 60
            plt.clf()
            self.plot()
        elif event.key == 'up':
            self.y += 60
            plt.clf()
            self.plot()
        elif event.key == 'down':
            self.y -= 60
            plt.clf()
            self.plot()
        elif event.key == 'r':
            self.automatic_route_through_all_imgs()
            print('doesnt work yet')
        elif event.key == 'c':
            self.selected_files = []
            print('cleared')
        elif event.key == 'w':
            np.savetxt('/home/emsala/plots/similarity_matrix.txt', self.similarity_matrix, fmt='%d')
        elif event.key == 'm':
            print('put in matrix')
            self.files_to_matrix()
            self.files = []
            print(self.similarity_matrix)

    def automatic_route_through_all_imgs(self):
        pass

    def round_path_index(self, click_data):
        if click_data < self.img_size * self.number_of_rows:
            path = 'y'
        else:
            path = 'x'
        return path

    def round_img_index(self, click_data):
        if click_data < self.img_size:
            img_index = 0
        else:
            img_index = int(math.ceil(click_data / 500)) - 1
        return img_index


if __name__ == '__main__':
    CSM = CreateSimilarityMatrix(path1, path2)
    CSM.plot()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(pd.DataFrame(CSM.similarity_matrix))