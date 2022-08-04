from instagram_private_api import Client
from PIL import ImageTk, Image
from os import listdir, mkdir
from tkinter import Spinbox
from tkinter import Button
from random import shuffle
from tkinter import Label
from tkinter import Entry
from tkinter import Frame
from os.path import isdir
from shutil import rmtree
from tkinter import Tk
import requests as rq

class Gohan:
    def __del__(self) -> None:
        if isdir("imgs"): rmtree("imgs")

    def __init__(self) -> None:
        self._window = Tk()
        self._window.title("DeskRobot - Gohan")
        self._window.config(bg="lightgray")
        self._window.resizable(False, False)

        self._label(column=0)

        self._label("usuário: ", 1, 1)
        login = self._entry(1, 2)

        self._label("senha: ", 2, 1)
        senha = self._entry(2, 2, show="*")

        self._label("ig do sorteio: ", 3, 1)
        ig_sorteio = self._entry(3, 2)

        self._label(row=4)
        Button(text="login", command=lambda: self._run(login.get(), senha.get(), ig_sorteio.get()),
            font=("Arial", 15), bg="lightblue", width=30).grid(row=5, column=1, columnspan=3)

        self._label(row=6)
        self._label("amigos/comentário: ", 7, 1, colspan=2)
        self._qnt = Spinbox(bg="white", font=("Arial", 15), width=2, from_=1, to=5)
        self._qnt.grid(row=7, column=2, columnspan=2)

        self._label(row=10, column=3)
        self._window.mainloop()

    def _run(self, login:str, senha:str, ig_sorteio:str) -> None:
        if not login or not senha or not ig_sorteio: return

        self._me = Client(login, senha)
        
        seguindo = self._me.user_following(self._me.authenticated_user_id, self._me.generate_uuid())
        ig_sorteio = list(filter(lambda u: ig_sorteio == u["username"], seguindo["users"]))[0]["pk"]

        me_segue, meus_seguidores = self._me.user_followers(self._me.authenticated_user_id, self._me.generate_uuid()), []
        seguindo = list(map(lambda u: u["username"], seguindo["users"]))

        while True:
            meus_seguidores.append(me_segue)
            if "next_max_id" not in me_segue.keys(): break

            me_segue = self._me.user_followers(self._me.authenticated_user_id, self._me.generate_uuid(), max_id=me_segue["next_max_id"])

        meus_seguidores = [user for seguidores in list(map(lambda s: s["users"], meus_seguidores)) for user in seguidores]
        meus_seguidores = list(map(lambda u: u["username"], meus_seguidores))

        em_comum = list(set(seguindo).intersection(meus_seguidores))

        if not isdir("imgs"): mkdir("imgs")
        # for _, post in enumerate(list(filter(lambda p: 1 == p["media_type"], self._me.user_feed(ig_sorteio)["items"]))):
        for _, post in enumerate(list(filter(lambda p: 1 == p["media_type"], self._me.user_feed(self._me.authenticated_user_id)["items"]))):
            if 15 < _: break
            open(f"imgs/{_:03}- {post['id']}.png", "wb").write(rq.get(post["image_versions2"]["candidates"][-1]["url"]).content)

        imgs, files, cols = listdir("imgs"), {}, [1, 3, 5, 7]
        _frame = Frame(self._window, bg="lightgray")
        for c in cols:
            Label(_frame, bg="lightgray").grid(row=0, column=c-1)
        
        for i, img in enumerate(imgs):
            if 15 < i: break
            files[i] = ImageTk.PhotoImage(Image.open(f"imgs/{img}").resize((75, 75)))

            def func(post_id=img[5:-4], users=em_comum):
                return self._comentar(post_id, users)

            c = i % 4
            r = int((i - c) / 4)
            Button(_frame, image=files[i], text=img[:3], compound="top", padx=5, pady=5, command=func).grid(row=r, column=cols[c])

        self._label(row=8)
        _frame.grid(row=9, column=1, columnspan=2)
        self._window.mainloop()

    def _comentar(self, post:str, users:list) -> None:
        shuffle(users)
        print(int(self._qnt.get()), post,  "".join([f"@{u} " for u in users[0:0 + int(self._qnt.get())]]))

        for _ in range(0, len(users), 3):
            self._me.post_comment(post, "".join([f"@{u} " for u in users[_:_ + int(self._qnt.get())]]))
            break

    def _entry(self, row:int=0, column:int=0, rowspan:int=1, colspan:int=1, show:str=None, width:int=20) -> Entry:
        _input = Entry(bg="white", font=("Arial", 15), width=width, show=show)
        _input.grid(row=row, column=column, rowspan=rowspan, columnspan=colspan)

        return _input

    def _label(self, text:str="", row:int=0, column:int=0, pady:int=0, rowspan:int=1, colspan:int=1) -> None:
        Label(text=text, bg="lightgray", font=("Arial", 15), padx=20, pady=pady) \
            .grid(row=row, column=column, rowspan=rowspan, columnspan=colspan)

if "__main__" == __name__:
    Gohan()