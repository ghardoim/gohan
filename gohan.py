from instagram_private_api import Client
from os import listdir, mkdir, remove
from random import randint, shuffle
from PIL import ImageTk, Image
from tkinter import Spinbox
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import Frame
from os.path import isdir
from shutil import rmtree
from tkinter import Tk
from time import sleep
from glob import glob
import requests as rq

class Gohan:
    def __del__(self) -> None:
        if isdir("imgs"): rmtree("imgs")

    def __init__(self) -> None:
        self._window = Tk()
        self._window.title("DeskRobot - Gohan")
        self._window.config(bg="lightgray")
        self._window.resizable(False, False)
        self._label(column=0, colspan=5, width=40)

        self._label("usuário: ", 1, 1, width=10)
        login = self._entry(1, 2)
        self._label("senha: ", 2, 1, width=10)
        senha = self._entry(2, 2, show="*")

        self._label(row=3, colspan=5, width=40)
        self._button(lambda: self._login(login.get(), senha.get()), "login", 4)
        self._label(row=5, colspan=5, width=40)
        self._window.mainloop()

    def _login(self, login:str, senha:str) -> None:
        if not login or not senha: return
        self._label("ig do sorteio: ", 6, 1, width=10)
        ig_sorteio = self._entry(6, 2)

        self._me = Client(login, senha)
        self._seguindo = self._me.user_following(self._me.authenticated_user_id, self._me.generate_uuid())
        me_segue, meus_seguidores = self._me.user_followers(self._me.authenticated_user_id, self._me.generate_uuid()), []
        seguindo = list(map(lambda u: u["username"], self._seguindo["users"]))
        while True:
            meus_seguidores.append(me_segue)
            if "next_max_id" not in me_segue.keys(): break
            me_segue = self._me.user_followers(self._me.authenticated_user_id, self._me.generate_uuid(), max_id=me_segue["next_max_id"])

        meus_seguidores = [user for seguidores in list(map(lambda s: s["users"], meus_seguidores)) for user in seguidores]
        meus_seguidores = list(map(lambda u: u["username"], meus_seguidores))
        self._em_comum = list(set(seguindo).intersection(meus_seguidores))

        self._label(row=7, colspan=5, width=40)
        self._button(lambda: self._run(ig_sorteio.get()), "buscar", 8)
        self._label(row=9, colspan=5, width=40)

    def _run(self, ig_sorteio:str) -> None:
        if not ig_sorteio: return
        ig_sorteio = list(filter(lambda u: ig_sorteio == u["username"], self._seguindo["users"]))[0]["pk"]

        self._qnt = self._spinbox("amigos/comentário:", 10)
        self._ncomments = self._spinbox("n° comentários:", 11)
        self._label(row=12, colspan=5, width=40)

        if not isdir("imgs"): mkdir("imgs")
        for file in glob("imgs/*.png"): remove(file)
        for p, post in enumerate(list(filter(lambda p: 1 == p["media_type"], self._me.user_feed(ig_sorteio)["items"]))):
            if 7 < p: break
            open(f"imgs/{p:03}- {post['id']}.png", "wb").write(rq.get(post["image_versions2"]["candidates"][-1]["url"]).content)

        imgs, files, cols, _frame = listdir("imgs"), {}, [1, 3, 5, 7], Frame(self._window, bg="lightgray")
        for c in cols: Label(_frame, bg="lightgray").grid(row=0, column=c-1)
        for i, img in enumerate(imgs):
            if 15 < i: break
            files[i] = ImageTk.PhotoImage(Image.open(f"imgs/{img}").resize((75, 75)))

            def func(post_id=img[5:-4], users=self._em_comum):
                return self._comentar(post_id, users)
            c = i % 4
            r = int((i - c) / 4)
            Button(_frame, image=files[i], text=img[:3], compound="top", padx=5, pady=5, command=func).grid(row=r, column=cols[c])

        _frame.grid(row=13, column=1, columnspan=2)
        self._label(row=14, colspan=5, width=40)
        self._window.mainloop()

    def _comentar(self, post:str, users:list) -> None:
        shuffle(users)
        for _ in range(int(self._ncomments.get())):
            nusers = randint(0, len(users) - int(self._qnt.get()) - 1)
            self._me.post_comment(post, "".join([f"@{u} " for u in users[nusers:nusers + int(self._qnt.get())]]))
            if 1 < int(self._ncomments.get()): sleep(randint(30, 60*3))

    def _entry(self, row:int=0, column:int=0, rowspan:int=1, colspan:int=1, show:str=None, width:int=20) -> Entry:
        _input = Entry(bg="white", font=("Arial", 15), width=width, show=show)
        _input.grid(row=row, column=column, rowspan=rowspan, columnspan=colspan)
        return _input

    def _label(self, text:str="", row:int=0, column:int=0, pady:int=0, rowspan:int=1, colspan:int=1, width:int=0) -> None:
        Label(text=text, bg="lightgray", font=("Arial", 15), padx=20, pady=pady, width=width) \
            .grid(row=row, column=column, rowspan=rowspan, columnspan=colspan)

    def _button(self, script, text:str, row:int) -> None:
        Button(text=text, command=script, font=("Arial", 15), bg="lightblue", width=35).grid(row=row, column=1, columnspan=2)

    def _spinbox(self, text:str, row:int) -> Spinbox:
        self._label(text, row, 0, colspan=3)
        _spnbox = Spinbox(bg="white", font=("Arial", 15), width=2, from_=1, to=5)
        _spnbox.grid(row=row, column=2, columnspan=2)
        return _spnbox

if "__main__" == __name__: Gohan()