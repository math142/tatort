
from tkinter import Label,Button,Entry,Tk,END,Listbox
import mysql.connector
import os

class interface(Tk):
    def __init__(self):
        super().__init__()
        self.minsize(250,200)
        self.listResultat = Listbox(self)
        self.listResultat.grid(row=0,column=0)
        self.labelSerie = Label(self,text="Serie")
        self.labelSerie.grid(row=1,column=0)
        self.EntrySerie = Entry(self)
        self.EntrySerie.grid(row=1,column=1)
        self.labelVille = Label(self,text="Ville")
        self.labelVille.grid(row=2,column=0)
        self.EntryVille = Entry(self)
        self.EntryVille.grid(row=2,column=1)
        self.labelHauptkommissar = Label(self,text="HauptKommissar")
        self.labelHauptkommissar.grid(row=3,column=0)
        self.EntryHaupt = Entry(self)
        self.EntryHaupt.grid(row=3,column=1)
        self.labelDate = Label(self,text="Date de diffusion")
        self.labelDate.grid(row=4,column=0)
        self.entryDate = Entry(self)
        self.entryDate.grid(row=4,column=1)
        self.buttonRechercher = Button(self,text="Rechercher",command=self.rechercher)
        self.buttonRechercher.grid(row=5,column=0)
        self.boutonJouer = Button(self,text="Jouer",command=self.Jouer)
        self.boutonJouer.grid(row=5,column=1)
    def rechercher(self):
        self.listResultat.delete(0,END)
        mydb = mysql.connector.connect(
            host="localhost",
            user="fernweh",
            password="clem02069008",
            database="kino")
        mycursor = mydb.cursor()
        serie = self.EntrySerie.get()
        ville = self.EntryVille.get()
        hauptkommissar = self.EntryHaupt.get()
        date = self.entryDate.get()
        if date == "":
            sql="""select titre from tatort where ville = %s  and hauptkommissar = %s""",(ville,hauptkommissar)
            mycursor.execute(*sql)
            result = mycursor.fetchall()
            for x in range(len(result)):
                self.listResultat.insert(END,result[x])

        elif hauptkommissar == "":
            sql = """select titre from tatort where ville = %s  and date_diffusion > %s""", (ville, date)
            mycursor.execute(*sql)
            result = mycursor.fetchall()
            for x in range(len(result)):

                self.listResultat.insert(END, result[x])
        elif ville == "":
            sql = """select titre from tatort where date_diffusion > %s  and hauptkommissar = %s""", (date, hauptkommissar)
            mycursor.execute(*sql)
            result = mycursor.fetchall()
            for x in range(len(result)):
                self.listResultat.insert(END, result[x])

    def Jouer(self):
        value = self.listResultat.curselection()
        titre = self.listResultat.get(value[0])
        mydb = mysql.connector.connect(
            host="localhost",
            user="fernweh",
            password="clem02069008",
            database="kino")
        sql = """select URL from tatort where titre = %s  """, (titre)
        mycursor = mydb.cursor()
        mycursor.execute(*sql)
        Url = mycursor.fetchall()
        url = Url[0][0].strip(",")
        
        cmd ="vlc '%s'"%url
        os.system(cmd)


if __name__ == '__main__':
    formulaire = interface()
    formulaire.mainloop()
