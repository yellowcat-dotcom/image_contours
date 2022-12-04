from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import cv2
import numpy as np
from tkinter import messagebox
from skimage.metrics import structural_similarity as ssim

root = Tk()

immm = ''
img_prewitt = ''
img_canny = ''
label_1 = ''
label_2 = ''
label_3 = ''
label_4 = ''
sravnenie = ''


def createNewWindow():
    newWindow = Toplevel(root)

    label = Label(newWindow, text="""Над полученными в результате пременения различных методов изображениями был проведен небольшой анализ:
                """, font=("Times New Roman",14))
    label.place(x=175, y=1)
    label_1 = Label(newWindow, text=sravnenie, font=("Times New Roman",14))
    label_1.place(x=1, y=30)

    newWindow.title("Информация")
    newWindow.geometry("1300x425")
    newWindow.resizable()
    newWindow.resizable(width=True, height=True)
    newWindow.option_add("*tearOff", FALSE)


# ТУТ Я ПРОБУЮ ВЫВЕСТИ СООБЩЕНИЕ О СРАВНЕВАНИИ СООБЩЕНИЙ
def mse(imageA, imageB):
    # "среднеквадратичная ошибка" между двумя изображениями - это
    # сумма квадратов разницы между двумя изображениями
    # ПРИМЕЧАНИЕ: два изображения должны иметь одинаковый размер
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # возвращает MSE, чем меньше ошибка, тем больше "похож" два изображения
    return err


def open_img():
    x = openfilename()
    global img
    img = Image.open(x)
    img = img.resize((450, 300), Image.Resampling.LANCZOS)
    ab = ImageTk.PhotoImage(img)
    # label.destroy()
    global panel
    panel = Label(root, image=ab)
    panel.image = ab
    panel.place(x=5, y=30)

    global label_1
    label_1 = Label(text="Начальное изображение")
    label_1.place(x=155, y=332)

    my_photo = cv2.imread(x)
    # фильтр Собеля
    kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

    global immm
    immm = cv2.filter2D(my_photo, -1, kernel)
    im = cv2.resize(immm, (450, 300), cv2.INTER_NEAREST)
    imm = Image.fromarray(im)
    imgtk = ImageTk.PhotoImage(imm)
    global pane
    pane = Label(root, image=imgtk)
    pane.image = imgtk
    pane.place(x=505, y=30)

    global label_2
    label_2 = Label(text="Результат работы метода Собеля")
    label_2.place(x=655, y=332)

    # prewitt
    global img_prewitt
    kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    img_prewittx = cv2.filter2D(my_photo, -1, kernelx)
    img_prewitty = cv2.filter2D(my_photo, -1, kernely)
    img_prewitt = img_prewittx + img_prewitty

    prewitt_im = cv2.resize(img_prewitt, (450, 300), cv2.INTER_NEAREST)
    prewitt_imm = Image.fromarray(prewitt_im)
    prewitt_imgtk = ImageTk.PhotoImage(prewitt_imm)

    global prewitt_pane
    prewitt_pane = Label(root, image=prewitt_imgtk)
    prewitt_pane.image = prewitt_imgtk
    prewitt_pane.place(x=5, y=380)

    global label_3
    label_3 = Label(text="Результат работы метода Превитта")
    label_3.place(x=155, y=682)

    global img_canny
    img_canny = cv2.Canny(my_photo, 100, 200)

    canny_im = cv2.resize(img_canny, (450, 300), cv2.INTER_NEAREST)
    canny_imm = Image.fromarray(canny_im)
    canny_imgtk = ImageTk.PhotoImage(canny_imm)

    global canny_pane
    canny_pane = Label(root, image=canny_imgtk)
    canny_pane.image = canny_imgtk
    canny_pane.place(x=505, y=380)
    global label_4
    label_4 = Label(text="Результат работы метода Джона Ф.Кэнни")
    label_4.place(x=655, y=682)

    # ТУТ Я ПРОБУЮ ВЫВЕСТИ СООБЩЕНИЕ О СРАВНЕВАНИИ СООБЩЕНИЙ
    # img_ab = ImageTk.getimage(ab)
    metod_sobel = cv2.cvtColor(immm, cv2.COLOR_BGR2GRAY)
    metod_prewitt = cv2.cvtColor(img_prewitt, cv2.COLOR_BGR2GRAY)
    # metod_canny = cv2.cvtColor(img_canny, cv2.COLOR_BGR2GRAY)

    # SSIM был создан для более точного определения различности двух изображений.
    # Он лежит в промежутке от -1 до 1
    # при значении равном 1, означает, что мы имеем две одинаковые картинки.

    # MSE всегда положительный, хотя он может быть равен 0, если прогнозы полностью точны.

    m_list = []
    s_list = []

    m_s_p = mse(metod_sobel, metod_prewitt)
    m_list.append(m_s_p)
    s_s_p = ssim(metod_sobel, metod_prewitt)
    s_list.append(s_s_p)
    m_s_p = str(m_s_p)
    s_s_p = str(s_s_p)


    m_s_c = mse(metod_sobel, img_canny)
    m_list.append(m_s_c)
    s_s_c = ssim(metod_sobel, img_canny)
    s_list.append(s_s_c)
    m_s_c = str(m_s_c)
    s_s_c = str(s_s_c)


    m_p_c = mse(metod_prewitt, img_canny)
    m_list.append(m_p_c)
    s_p_c = ssim(metod_prewitt, img_canny)
    s_list.append(s_p_c)
    m_p_c = str(m_p_c)
    s_p_c = str(s_p_c)


    min_m_list = min(m_list)
    max_m_list = max(m_list)

    min_s_list = min(s_list)
    max_s_list = max(s_list)

    info_m = """Данные о Среднеквадратической ошибке (MSE): 
       
Собель и Превитт: """ + str(m_list[0]) + """
Собель и Кэнни: """ + str(m_list[1]) + """
Превитт и Кэнни: """ + str(m_list[2]) + """

"""
    info_m = info_m + str(
'Больше всего, согласно данным Среднеквадратической ошибки, между собой похожи изображения полученные с помощью методов ')
    if min_m_list == m_list[0]:
        info_m = info_m + 'Собеля и Превитта '
    if min_m_list == m_list[1]:
        info_m = info_m + 'Собеля и Кэнни '
    if min_m_list == m_list[2]:
        info_m = info_m + 'Превитта и Кэнни '
    info_m = info_m + """
Меньше всего, согласно данным Среднеквадратической ошибки, между собой похожи изображения полученные с помощью методов """
    if max_m_list == m_list[0]:
        info_m = info_m + 'Собеля и Превитта '
    if max_m_list == m_list[1]:
        info_m = info_m + 'Собеля и Кэнни '
    if max_m_list == m_list[2]:
        info_m = info_m + 'Превитта и Кэнни '

    info_s = """    
    Данные об Индексе структурного сходства(SSIM):
    
Собель и Превитт: """ + str(s_list[0]) + """
Собель и Кэнни: """ + str(s_list[1]) + """
Превитт и Кэнни: """ + str(s_list[2]) + """

"""
    info_s = info_s + str(
'Больше всего, согласно данным об Индексе структурного сходства, между собой похожи изображения полученные с помощью методов ')
    if min_s_list == s_list[0]:
        info_s = info_s + 'Собеля и Превитта '
    if min_s_list == s_list[1]:
        info_s = info_s + 'Собеля и Кэнни '
    if min_s_list == s_list[2]:
        info_s = info_s + 'Превитта и Кэнни '
    info_s = info_s + """
Меньше всего, согласно данным об Индексе структурного сходства, между собой похожи изображения полученные с помощью методов """
    if max_s_list == s_list[0]:
        info_s = info_s + 'Собеля и Превитта '
    if max_s_list == s_list[1]:
        info_s = info_s + 'Собеля и Кэнни '
    if max_s_list == s_list[2]:
        info_s = info_s + 'Превитта и Кэнни '

    global sravnenie
    sravnenie = info_m + '\n' + info_s

    # print(info_m)
    # print()
    # print(info_s)

    # print(m_list)
    # print(s_list)


def openfilename():
    filename = filedialog.askopenfilename(title='Выбор изображения')
    return filename


def remove_text():
    if immm != '':
        pane.destroy()
        panel.destroy()
        prewitt_pane.destroy()
        canny_pane.destroy()
        label_1.destroy()
        label_2.destroy()
        label_3.destroy()
        label_4.destroy()

    else:
        messagebox.showerror(title="Ошибка", message="Необходимо выбрать изображение")


def program():
    messagebox.showinfo(title="О программе", message="""Наименование: Image Loader
Версия: 0001
Автор: Гончаренко Валентина Викторовна
Дата выпуска: Когда-то в 2022 году""")


def tutorials():
    messagebox.showinfo(title="О программе", message="""Для получения контуров изображения вам необходимо
нажать \"Выбрать изображение\" во вкладке \"Файл\".
Вы увидите на экране изображения контуров, полученных разными методами.
Вы можете сохранить их по отдельности.""")


def save_Sobel():
    # file = filedialog.asksaveasfilename(title = u'save file ', filetypes = files, defaultextension=files)
    if immm != '':
        files = [('JPEG files', '*.jpeg'),
                 ('PNG Files', '*.png'),
                 ('Python Files', '*.py')]
        cv2.imwrite(filedialog.asksaveasfilename(title=u'save file ', filetypes=files, defaultextension=files), immm)
        messagebox.showinfo(title="Информация", message="Изображение сохранено")

    else:
        messagebox.showerror(title="Ошибка", message="Необходимо выбрать изображение")
        # img.save(filedialog.asksaveasfilename(title = u'save file ', filetypes = files, defaultextension=files))


def save_prewitt():
    # file = filedialog.asksaveasfilename(title = u'save file ', filetypes = files, defaultextension=files)
    if img_prewitt != '':
        files = [('JPEG files', '*.jpeg'),
                 ('PNG Files', '*.png'),
                 ('Python Files', '*.py')]
        cv2.imwrite(filedialog.asksaveasfilename(title=u'save file ', filetypes=files, defaultextension=files),
                    img_prewitt)
        messagebox.showinfo(title="Информация", message="Изображение сохранено")

    else:
        messagebox.showerror(title="Ошибка", message="Необходимо выбрать изображение")
        # img.save(filedialog.asksaveasfilename(title = u'save file ', filetypes = files, defaultextension=files))


def save_canny():
    # file = filedialog.asksaveasfilename(title = u'save file ', filetypes = files, defaultextension=files)
    if img_canny != '':
        files = [('JPEG files', '*.jpeg'),
                 ('PNG Files', '*.png'),
                 ('Python Files', '*.py')]
        cv2.imwrite(filedialog.asksaveasfilename(title=u'save file ', filetypes=files, defaultextension=files),
                    img_canny)
        messagebox.showinfo(title="Информация", message="Изображение сохранено")

    else:
        messagebox.showerror(title="Ошибка", message="Необходимо выбрать изображение")
        # img.save(filedialog.asksaveasfilename(title = u'save file ', filetypes = files, defaultextension=files))


root.title("Contour search")
root.geometry("1000x750")
root.resizable()
root.resizable(width=True, height=True)
root.option_add("*tearOff", FALSE)

main_menu = Menu()
file_menu = Menu()
setings_menu = Menu()

setings_menu.add_command(label="Метод_Собеля", command=save_Sobel)  # , command = save)
setings_menu.add_command(label="Метод_Превитта", command=save_prewitt)
setings_menu.add_command(label="Метод_Кэнни", command=save_canny)

file_menu.add_command(label="Выбрать изображение", command=open_img)
file_menu.add_command(label="Удалить изображение", command=remove_text)
file_menu.add_cascade(label="Сохранить", menu=setings_menu)

main_menu.add_cascade(label="Файл", menu=file_menu)
main_menu.add_command(label="Помощь", command=tutorials)
main_menu.add_command(label="О программе", command=program)
main_menu.add_command(label="Информация", command=createNewWindow)
main_menu.add_command(label="Выход", command=root.destroy)

root.config(menu=main_menu)

imgg = Image.open('fon2.png')
imgg = imgg.resize((1000, 750), Image.Resampling.LANCZOS)
bg = ImageTk.PhotoImage(imgg)
# global label
label = Label(root, image=bg)
label.place(x=0, y=0)

root.mainloop()

