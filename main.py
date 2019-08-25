# -*- coding:utf-8 -*-

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from math import *
from threading import Thread
from threading import Timer
from datetime import datetime
from urllib.request import urlopen
import requests
import re
import json
import webbrowser
import sys
import os

TAB_ALL = [
    [1, "Orb of Alteration"],
    [2, "Orb of Fusing"],
    [3, "Orb of Alchemy"],
    [4, "Chaos Orb"],
    [5, "Gemcutter's Prism"],
    [6, "Exalted Orb"],
    [7, "Chromatic Orb"],
    [8, "Jeweller's Orb"],
    [9, "Orb of Chance"],
    [10, "Cartographer's Chisel"],
    [11, "Orb of Scouring"],
    [12, "Blessed Orb"],
    [13, "Orb of Regret"],
    [14, "Regal Orb"],
    [15, "Divine Orb"],
    [16, "Vaal Orb"],
    [17, "Scroll of Wisdom"],
    [18, "Portal Scroll"],
    [19, "Armourer's Scrap"],
    [20, "Blacksmith's Whetstone"],
    [21, "Glassblower's Bauble"],
    [22, "Orb of Transmutation"],
    [23, "Orb of Augmentation"],
    [24, "Mirror of Kalandra"],
    [25, "Eternal Orb"],
    [26, "Perandus Coin"],
    [35, "Silver Coin"],
    [27, "Sacrifice at Dusk"],
    [28, "Sacrifice at Midnight"],
    [29, "Sacrifice at Dawn"],
    [30, "Sacrifice at Noon"],
    [31, "Mortal Grief"],
    [32, "Mortal Rage"],
    [33, "Mortal Hope"],
    [34, "Mortal Ignorance"],
    [36, "Eber's Key"],
    [37, "Yriel's Key"],
    [38, "Inya's Key"],
    [39, "Volkuur's Key"],
    [40, "Offering to the Goddess"],
    [41, "Fragment of the Hydra"],
    [42, "Fragment of the Phoenix"],
    [43, "Fragment of the Minotaur"],
    [44, "Fragment of the Chimera"],
    [45, "Apprentice Cartographer's Sextant"],
    [46, "Journeyman Cartographer's Sextant"],
    [47, "Master Cartographer's Sextant"],
    [48, "Sacrifice set"],
    [49, "Mortal set"],
    [50, "Pale Court set"],
    [51, "Shaper set"],
    [52, "Splinter of Xoph"],
    [53, "Splinter of Tul"],
    [54, "Splinter of Esh"],
    [55, "Splinter of Uul-Netol"],
    [56, "Splinter of Chayula"],
    [57, "Blessing of Xoph"],
    [58, "Blessing of Tul"],
    [59, "Blessing of Esh"],
    [60, "Blessing of Uul-Netol"],
    [61, "Blessing of Chayula"],
    [62, "Xoph's Breachstone"],
    [63, "Tul's Breachstone"],
    [64, "Esh's Breachstone"],
    [65, "Uul-Netol's Breachstone"],
    [66, "Chayula's Breachstone"],
    [494, "Ancient Reliquary Key"],
    [512, "Divine Vessel"],
    [513, "Orb of Annulment"],
    [514, "Orb of Binding"],
    [515, "Orb of Horizons"],
    [516, "Harbinger's Orb"],
    [517, "Engineer's Orb"],
    [518, "Ancient Orb"],
    [519, "Annulment Shard"],
    [520, "Mirror Shard"],
    [521, "Exalted Shard"]]

tab_item = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
    [41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
    [51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
    [61, 62, 63, 64, 65, 66, 494, 512, 513, 514],
    [515, 516, 517, 518, 519, 520, 521, 0, 0, 0],
]

tk_im = []


def printf(text):
    print(text)
    file = open('log', 'a')
    file.write('{} \n'.format(text))
    file.close()


class Result():
    def __init__(self):
        self.result = []
        self.winner = []
        for i in range(80):
            self.result.append({'from': i + 1, 'to': []})

        for i in range(80):
            for j in range(80):
                self.result[i]['to'].append([])

    def clear(self):
        self.__init__()

    def insert_result(self, res, want, have):
        self.result[int(have) - 1]['to'][int(want) - 1] = res
        LOG = open('data.log', 'w')
        LOG.write(json.dumps(self.result, indent=2))
        LOG.close()

    def get_result(self, want, have):
        return self.result[int(have) - 1]['to'][int(want) - 1]

    def analyse(self):
        effectiv = False
        self.winner = []
        for i in range(80):
            for j in range(i, 80):
                if self.get_result(i, j) and self.get_result(j, i):
                    r = self.get_result(i, j)[0][0]/self.get_result(i, j)[0][1]
                    t = self.get_result(j, i)[0][0]/self.get_result(j, i)[0][1]
                    if r * t > 1.0:
                        self.winner.append([r * t, i, j])
                        printf('W : i_{} j_{} r*t_{}'.format(i, j, r * t))
                        effectiv = True
        if effectiv:
            self.winner.sort()
            self.winner = self.winner[::-1]
        return effectiv


def findOccurences(league, want, have):
    r = requests.get("http://currency.poe.trade/search",
                     params={'league': league,
                             'online': 'x',
                             'want': want,
                             'have': have})
    string = r.text.encode('ascii', 'ignore').decode('utf-8')
    tab = []
    triggered_char = 'displayoffer-middle'
    nb_offer = 0
    for i in re.finditer(triggered_char, string):
        nb_offer += 1
        new_string = string[i.start():i.start()+1000]
        stocks = []
        nb_stock = 0
        for j in re.finditer('stock', new_string):
            nb_stock += 1
            inter = new_string[j.start()+7:j.start()+13]
            stock = inter[:inter.find('"')]
            stocks.append(stock)
        st = 0
        try:
            st = stocks[0]
        except:
            st = 0
        inter = string[i.start()+21:i.start()+45]
        liste = (inter[:inter.find(' ')],
                 inter[inter.find(' ', int(len(inter) / 2)):inter.find('<')])
        l1 = inter[:inter.find(' ')]
        inter = inter[inter.find(' ')+1:]
        inter = inter[inter.find(' ')+1:]
        l2 = inter[:inter.find('<')]
        tab.append([float(l1), float(l2)])
        print("{}, {}, {}".format(l1, l2, st))
    return tab


def createImage():
    if not os.path.exists('currency_32.png'):
        f = open('currency_32.png', 'wb')
        f.write(requests.get(
                'http://currency.poe.trade/static/currency_32.png?772983101'
                ).content)
        f.close()
    for i in range(80):
        x = i * 33
        cropped = Image.open('currency_32.png').crop((x, 0, x + 32, 32))
        tk_im.append(ImageTk.PhotoImage(cropped))


def getImg(idx):
    if not tk_im:
        createImage()
    return tk_im[idx]


def generateLink(tab):
    link = []
    for i in tab:
        for j in tab:
            if i != j:
                link.append([i, j])
    return link


class checker(Thread):
    def __init__(self, league, have, want):
        Thread.__init__(self)
        self.league = league
        self.have = have
        self.want = want

    def run(self):
        res = findOccurences(self.league, self.have, self.want)
        result.insert_result(res, self.have, self.want)
        # printf(res)


class Gui():
    def __init__(self, root):
        self.root = root

        self.menubar = Menu(self.root)

        self.settings_menu = Menu(self.menubar, tearoff=0)
        self.tt_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Settings', menu=self.settings_menu)
        self.menubar.add_cascade(label='ME', menu=self.tt_menu)

        self.settings_menu.add_command(label='Change settings file',
                                       command=self.change_settings_file)
        self.settings_menu.add_command(label='Reload config',
                                       command=self.reload_config)

        self.tt_menu.add_command(label='Load my Currency',
                                 command=self.load_currency)

        self.canvas = Canvas(self.root, width=900, height=410)
        self.canvas.pack()

        self.league_label = Label(text='League')
        self.league_label_window = self.canvas.create_window(
            10, 10, anchor=NW,
            window=self.league_label)

        self.league_choice = Text(height=1, width=10)
        self.league_choice_window = self.canvas.create_window(
            80, 10, anchor=NW,
            window=self.league_choice)
        self.league_choice.insert(INSERT, 'Legion')

        self.number_item_label = Label(text='Number to search')
        self.number_item_label_window = self.canvas.create_window(
            10, 30, anchor=NW,
            window=self.number_item_label)

        self.number_item_choice = Spinbox(from_=0, to=80,
                                          width=4, command=self.number_changed)
        self.number_item_choice_window = self.canvas.create_window(
            126, 30, anchor=NW,
            window=self.number_item_choice)

        self.number_item_choice.delete(0, "end")
        self.number_item_choice.insert(0, 4)

        self.search_button = Button(text='Search',
                                    height=2, width=10,
                                    relief=RAISED, command=self.search_item)
        self.search_button_window = self.canvas.create_window(
            170, 10, anchor=NW,
            window=self.search_button)

        self.show_best_value = tk.IntVar()
        self.show_best = Checkbutton(text='Show Best',
                                     variable=self.show_best_value,
                                     command=self.best_checked)
        self.show_best_window = self.canvas.create_window(
            260, 10, anchor=NW,
            window=self.show_best)

        self.timer_label = Label(text='Timer time')
        self.timer_label_window = self.canvas.create_window(
            290, 30, anchor=NW,
            window=self.timer_label)

        self.timer_box = Spinbox(from_=0,
                                 to=60,
                                 width=2,
                                 command=self.timer_changed)
        self.timer_box_window = self.canvas.create_window(
            260, 30, anchor=NW,
            window=self.timer_box)

        self.timer_box.delete(0, "end")
        self.timer_box.insert(0, 15)

        self.canvas.create_line(425, 0, 425, 390)
        self.canvas.create_rectangle(10, 400, 425, 410)
        self.info_label = Label(text='0%')
        self.info_label_window = self.canvas.create_window(
            10, 378, anchor=NW,
            window=self.info_label)
        self.canvas.create_rectangle(12, 402, 12, 408,
                                     fill='green', tags='progressbar')
        # (12, 402) => (423, 402)

        self.log1 = Text(height=7, width=16)
        self.log1_window = self.canvas.create_window(440,
                                                     10,
                                                     anchor=NW,
                                                     window=self.log1)

        self.log2 = Text(height=7, width=16)
        self.log2_window = self.canvas.create_window(580,
                                                     10,
                                                     anchor=NW,
                                                     window=self.log2)

        self.info = Text(height=7, width=16)
        self.info_window = self.canvas.create_window(720, 10, anchor=NW,
                                                     window=self.info)

        self.open_window = Button(text=" Open Browser ", height=2, width=15,
                                  relief=RAISED, command=self.open_browser)
        self.open_window_window = self.canvas.create_window(
            660, 140, anchor=NW,
            window=self.open_window)

        self.charge_next_trade = Button(text=" Charge Next ",
                                        height=2, width=10,
                                        relief=RAISED,
                                        command=self.next_winner)
        self.charge_next_trade_window = self.canvas.create_window(
            800, 140, anchor=NW,
            window=self.charge_next_trade)

        self.winner_tab = [Button(image=getImg(3),
                                  width=32, height=32,
                                  bg='green'
                                  ) for i in range(3)]
        self.winner_tab_window = [
            self.canvas.create_window(440 + i * 80, 140,
                                      anchor=NW, window=self.winner_tab[i])
            for i in range(3)
        ]

        self.log = Text(height=12, width=50)
        self.log_window = self.canvas.create_window(440, 200,
                                                    anchor=NW, window=self.log)

        temp1 = Label(text='=>')
        temp1_window = self.canvas.create_window(490, 145,
                                                 anchor=NW, window=temp1)
        temp2 = Label(text='=>')
        temp2_window = self.canvas.create_window(570, 145,
                                                 anchor=NW, window=temp2)

        self.items = []
        self.enabled_items = [i + 1 for i in range(4)]
        self.show_best_value.set(True)
        self.winner_loaded = 0

        self.root.config(menu=self.menubar)

        self.settings_file_path = './poemarket.cfg'
        self.settings = {}
        self.create_config()
        self.reload_config()
        self.show_currency()
        self.number_changed()
        createImage()

    def timer_changed(self):
        pass

    def create_config(self):
        self.settings['Item_Order'] = []
        for i in range(8):
            self.settings['Item_Order'].append([])
            for j in range(10):
                idx = i * 10 + j
                self.settings['Item_Order'][i].append(
                    TAB_ALL[idx % len(TAB_ALL)][0])

        if not os.path.exists(self.settings_file_path):
            file = open(self.settings_file_path, 'w')
            file.write(json.dumps({
                'POESESSID': 'your POESESSID here',
                'accountName': 'your name account here',
                'Item_Order': self.settings['Item_Order'],
            }, indent=2))
            file.close()

    def change_settings_file(self):
        files = filedialog.askopenfilename(initialdir='./',
                                           initialfile='poemarket.cfg',
                                           title='Select config file',
                                           filetypes=(
                                               ('config files', '*.cfg'),
                                               ('all files', '*.*')))
        if files:
            self.settings_file_path = files

    def reload_config(self):
        if not os.path.exists(self.settings_file_path):
            self.create_config()
        file = open(self.settings_file_path, 'r')
        self.settings = json.loads(file.read())
        file.close()
        self.info_label.config(text='Config reloaded !')

    def load_currency(self):
        URL = 'https://www.pathofexile.com/character-window/get-stash-items'
        data = {
            'league': self.league_choice.get(1.0, END)[::-1][1:][::-1],
            'tabs': 1,
            'tabIndex': 0,
            'accountName': self.settings['accountName'],
        }
        self.currency = {}
        cookie = {'POESESSID': self.settings['POESESSID']}
        stashs = json.loads(requests.get(URL,
                                         params=data,
                                         cookies=cookie).text)
        for tabIndex in range(0, stashs['numTabs']):
            data['tabIndex'] = tabIndex
            private_stashs = json.loads(requests.get(URL,
                                                     params=data,
                                                     cookies=cookie).text)
            for item in private_stashs['items']:
                printf(item)

    def set_pb(self, pc):
        self.canvas.delete(self.canvas.find_withtag('progressbar'))

        self.info_label.config(
            text='{:>5.2f}%                  '
            .format(pc * 100))
        self.canvas.create_rectangle(12, 402,
                                     int(12 + pc * 411), 408,
                                     fill='green', tags='progressbar')
        # (12, 402) => (423, 402)

    def best_checked(self):
        pass

    def logg(self, text):
        self.log.delete(1.0, END)
        self.log.insert(1.0, text)

    def number_changed(self):
        nb = 0
        self.enabled_items = []
        for i in range(len(self.items)):
            for j in range(len(self.items[i])):
                if nb < int(self.number_item_choice.get()):
                    self.items[i][j][0].config(bg='green')
                    self.enabled_items.append(i * 10 + j + 1)
                    nb += 1
                else:
                    self.items[i][j][0].config(bg='red')

    def winner_clicked(self, value):
        self.log1.delete(1.0, END)
        self.log1.insert(1.0, '{}'.format(value))

    def show_currency(self):
        self.items = []
        for i in range(8):
            self.items.append([])
            for j in range(10):
                idx = i * 10 + j + 1
                id_item = self.settings['Item_Order'][i][j]
                color = 'red'
                if id_item in self.enabled_items:
                    color = 'green'

                btn = Button(text='{}'.format(idx))
                btn.config(image=getImg(idx - 1),
                           width=32, height=32, bg=color,
                           command=self.btn_make_callback(i, j))
                btn_window = self.canvas.create_window(10 + j * 40,
                                                       60 + i * 40,
                                                       anchor=NW, window=btn)

                self.items[i].append([btn, btn_window])

    def btn_callback(self, arg1, arg2):
        if self.items[arg1][arg2][0].cget('bg') == 'green':
            self.items[arg1][arg2][0].config(bg='red')
        else:
            self.items[arg1][arg2][0].config(bg='green')

        self.enabled_items = self.get_enabled_item()

    def get_enabled_item(self):
        self.enabled_items = []
        for i in range(len(self.items)):
            for j in range(len(self.items[i])):
                if self.items[i][j][0].cget('bg') == 'green':
                    self.enabled_items.append(i * 10 + j + 1)
        return self.enabled_items

    def btn_make_callback(self, arg1, arg2):
        return (lambda: self.btn_callback(arg1, arg2))

    def open_browser(self):
        if result.winner:
            URL = """http://currency.poe.trade/search?league={}&online=x&want={}&have={}"""
            webbrowser.open(URL.format(
                self.league_choice.get(1.0, END)[::-1][1:][::-1],
                result.winner[self.winner_loaded][1],
                result.winner[self.winner_loaded][2]))
            webbrowser.open(URL.format(
                self.league_choice.get(1.0, END)[::-1][1:][::-1],
                result.winner[self.winner_loaded][2],
                result.winner[self.winner_loaded][1]))

    def search_item(self):
        result.clear()
        allLink = generateLink(self.enabled_items)
        maxThread = 333
        thread = []
        printf('link lenght : {} max thread : {} need iter : {}'.format(
            len(allLink),
            maxThread,
            str(float(len(allLink) / maxThread))[:4]))
        for i in range(ceil(len(allLink) / maxThread)):
            for j in range(maxThread):
                nowIdx = j + i * maxThread
                if nowIdx < len(allLink):
                    have = str(allLink[nowIdx][0])
                    want = str(allLink[nowIdx][1])
                    thread.append(checker(
                        self.league_choice.get(1.0, END)[::-1][1:][::-1],
                        have, want))
            for j in range(maxThread):
                nowIdx = j + i * maxThread
                if nowIdx < len(allLink):
                    thread[nowIdx].start()
            for j in range(maxThread):
                nowIdx = j + i * maxThread
                if nowIdx < len(allLink):
                    printf(
                        '{:>4}% thread_{} joined'
                        .format(str(100 * (nowIdx + 1) / len(allLink))[:4],
                                nowIdx))
                    self.set_pb((nowIdx + 1) / len(allLink))
                    self.root.update_idletasks()
                    thread[nowIdx].join()
        self.load_winner(0)

    def next_winner(self):
        self.load_winner((self.winner_loaded + 1) % len(result.winner))

    def load_winner(self, number):
        if result.analyse() and self.show_best_value.get():
            self.winner_loaded = number
            allLink = generateLink(self.enabled_items)
            best = result.winner[number]
            printf(result.winner)
            printf(best)
            self.print_result(allLink, best[1:], self.log1)
            self.print_result(allLink, best[1:][::-1], self.log2)
            self.winner_tab[0].config(image=getImg(best[2] - 1))
            self.winner_tab[1].config(image=getImg(best[1] - 1))
            self.winner_tab[2].config(image=getImg(best[2] - 1))
            r1 = result.get_result(best[1], best[2])
            r2 = result.get_result(best[2], best[1])
            myresult = ''
            for i in range(min(5, len(r1), len(r2))):
                res = (r1[i][0] / r1[i][1] * r2[i][0] / r2[i][1] - 1) * 100
                myresult += 'Gain: {:>4}%\n'.format(str(res)[:4])
            myresult += '------------\nNet G: {:>4}'.format(
                str(r1[0][0] / r1[0][1] - r2[0][1] / r2[0][0])[:4])
            self.info.delete(1.0, END)
            self.info.insert(1.0, myresult)
            string = ''
            for i in result.winner:
                fst = ''
                sec = ''
                for j in TAB_ALL:
                    if j[0] == i[1]:
                        fst = j[1]
                    if j[0] == i[2]:
                        sec = j[1]
                string += '{:3.1f}% for {} <=> {}\n'.format(i[0] * 100 - 100,
                                                            fst, sec)
            self.log.delete(1.0, END)
            self.log.insert(1.0, string)
        else:
            self.info.delete(1.0, END)
            self.log.delete(1.0, END)
            self.log1.delete(1.0, END)
            self.log2.delete(1.0, END)

    def print_result(self, allLink, best, logger):
        myresult = ''
        r = result.get_result(best[0], best[1])
        for i in range(min(5, len(r))):
            myresult += '{:>4}=>{:>4}/{:>4}\n'.format(
                str(int(r[i][1]))[:4],
                str(int(r[i][0]))[:4],
                str(float(r[i][0] / r[i][1]))[:4])
        if r[0][0] > r[0][1]:
            myresult += '------------\n{:>4}=>{:>4}'.format(
                1, str(float(r[0][0] / r[0][1]))[:4])
        else:
            myresult += '------------\n{:>4}=>{:>4}'.format(
                str(float(r[0][1] / r[0][0]))[:4], 1)
        logger.delete(1.0, END)
        logger.insert(1.0, myresult)


if __name__ == '__main__':
    root = Tk()
    result = Result()
    gui = Gui(root)
    root.mainloop()
