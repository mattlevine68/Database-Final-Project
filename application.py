import tkinter as tk
import database


conn_string = "host='localhost' dbname='final_project' user='project_user' password='goodGrades'"

class Application(tk.Frame):
    def __init__(self, master=None, query_options = None):
        super().__init__(master)
        self.master = master
        self.query_options = query_options
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_widget()
        self.query_widget()
        self.quit_widget()

    def query_widget(self):
        self.query = tk.Button(self)
        self.query['text'] = 'First Query'
        self.query['command'] = self.query_options.diversity_query
        self.query.pack(side='top')

        self.label = tk.Label(self, text='Limit Results')
        self.label.pack(side='left')
        self.Entry = tk.Label(self, bd=5)
        self.Entry.pack(side='right')

    def hi_widget(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

    def quit_widget(self):
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
    def say_hi(self):
        print("hi there, everyone!")

if __name__ == '__main__':
    query_options = database.CollegeQuery(conn_string)
    root = tk.Tk()
    app = Application(master=root, query_options = query_options)
    app.master.title('College Databse Queries')
    app.master.maxsize(1000,400)
    app.mainloop()
