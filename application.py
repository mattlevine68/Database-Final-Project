import tkinter as tk
import database


conn_string = "host='localhost' dbname='final_project' user='project_user' password='goodGrades'"

#Uses tkinter to create a GUI to present to class
#Each queryx_widget has either labels, entries or buttons to work with queries
#all of the caller functions are if a query has an entry it gets the result first then calls the query in database.py
class Application(tk.Frame):
    def __init__(self, master=None, query_options = None):
        super().__init__(master)
        self.master = master
        self.query_options = query_options
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.career_stem_query_widget()
        self.diversity_query_widget()
        self.worst_grad_rate_widget()
        self.winning_enrolled_widget()
        self.winning_with_tech()
        self.quit_widget()

    def diversity_query_caller(self):
        self.query_options.diversity_query(self.entry_diversity.get())

    def diversity_query_widget(self):
        self.label_diversity = tk.Label(self, text='Limit:')
        self.label_diversity.grid(row=1, column=0, pady=2)

        self.entry_diversity = tk.Entry(self)
        self.entry_diversity.grid(row=1, column=1, pady=2)

        self.query_diversity = tk.Button(self)
        self.query_diversity['text'] = 'Diversity Query'
        self.query_diversity['command'] = self.diversity_query_caller
        self.query_diversity.grid(row=1, column=6, pady=2)

    def career_stem_caller(self):
        self.query_options.career_query(self.entry_career_stem.get(), self.entry_career_stem_state.get())

    def career_stem_query_widget(self):
        self.label_career_stem = tk.Label(self, text='Limit:')
        self.label_career_stem.grid(row=0, column=0, pady=2)

        self.entry_career_stem = tk.Entry(self)
        self.entry_career_stem.grid(row=0, column=1, pady=2)

        self.label_career_stem_state = tk.Label(self, text='State:')
        self.label_career_stem_state.grid(row=0, column=2, pady=2)

        self.entry_career_stem_state = tk.Entry(self)
        self.entry_career_stem_state.grid(row=0, column=3, pady=2)

        self.query_career_stem = tk.Button(self)
        self.query_career_stem["text"] = "Career Stem Query"
        self.query_career_stem["command"] = self.career_stem_caller
        self.query_career_stem.grid(row=0, column=6, pady=2)

    def worst_grad_caller(self):
        self.query_options.worst_grad_rate_query(self.entry_worst_grad.get())

    def worst_grad_rate_widget(self):
        self.label_worst_grad = tk.Label(self, text='Min Samples:')
        self.label_worst_grad.grid(row=2, column=0, pady=2)

        self.entry_worst_grad = tk.Entry(self)
        self.entry_worst_grad.grid(row=2, column=1, pady=2)

        self.query_worst_grad = tk.Button(self)
        self.query_worst_grad["text"] = "Grad Rate Query"
        self.query_worst_grad["command"] = self.worst_grad_caller
        self.query_worst_grad.grid(row=2, column=6, pady=2)

    def winning_enrolled_caller(self):
        self.query_options.team_query(self.entry_winning_percent.get(), self.entry_winning_enrolled.get())

    def winning_enrolled_widget(self):
        self.label_winning_percent = tk.Label(self, text='Win Percent:')
        self.label_winning_percent.grid(row=3, column=0, pady=2)

        self.entry_winning_percent = tk.Entry(self)
        self.entry_winning_percent.grid(row=3, column=1, pady=2)

        self.label_winning_enrolled = tk.Label(self, text='Enrolled:')
        self.label_winning_enrolled.grid(row=3, column=2, pady=2)

        self.entry_winning_enrolled = tk.Entry(self)
        self.entry_winning_enrolled.grid(row=3, column=3, pady=2)

        self.query_winning_enrolled = tk.Button(self)
        self.query_winning_enrolled["text"] = "Winning Enrolled Query"
        self.query_winning_enrolled["command"] = self.winning_enrolled_caller
        self.query_winning_enrolled.grid(row=3, column=6, pady=2)

    def winning_with_tech_caller(self):
        self.query_options.sport_query(self.entry_winning_tech.get(), self.entry_power_rating.get(), self.entry_offense_rank.get())

    def winning_with_tech(self):
        self.label_winning_tech = tk.Label(self, text='Limit:')
        self.label_winning_tech.grid(row=5, column=0, pady=2)

        self.entry_winning_tech = tk.Entry(self)
        self.entry_winning_tech.grid(row=5, column=1, pady=2)

        self.label_power_rating = tk.Label(self, text='Power Rating:')
        self.label_power_rating.grid(row=5, column=2, pady=2)

        self.entry_power_rating = tk.Entry(self)
        self.entry_power_rating.grid(row=5, column=3, pady=2)

        self.label_offense_rank = tk.Label(self, text='Offense Rank:')
        self.label_offense_rank.grid(row=5, column=4, pady=2)

        self.entry_offense_rank = tk.Entry(self)
        self.entry_offense_rank.grid(row=5, column=5, pady=2)

        self.query_winning_tech = tk.Button(self)
        self.query_winning_tech["text"] = "Winning Tech Query"
        self.query_winning_tech["command"] = self.winning_with_tech_caller
        self.query_winning_tech.grid(row=5, column=6, pady=2)

    def quit_widget(self):
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=6, column=6, pady=2)


if __name__ == '__main__':
    query_options = database.CollegeQuery(conn_string)
    root = tk.Tk()
    app = Application(master=root, query_options = query_options)
    app.master.title('College Databse Queries')
    app.master.maxsize(1000,400)
    app.mainloop()
