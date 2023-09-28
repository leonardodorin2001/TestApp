
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.list import OneLineListItem

from kivy.metrics import dp

from kivy.core.window import Window

#import database sqlalchemy
from models import Base,engine, session, User, Task


class Home(Screen):
    pass

class LogIn(Screen):

    
    def LogIn(self):
        username = self.ids.username.text
        password = self.ids.password.text

        if username == "" or password == "":
            self.ids.username.error = True
            self.ids.password.error = True
        else:
            self.user = session.query(User).filter(User.username == username, User.password == password).one_or_none()  
            
            if self.user == None:
                self.ids.userinfo.text = "this user dosen't exist"
                
            else:
                self.manager.current = 'index'
                self.manager.get_screen('index').ids.name_user.title = self.user.username


class SingUp(Screen):
    def SingUpFunction(self):
        username = self.ids.username.text
        password = self.ids.password.text
        
        if username == "" or password == "" and (username == "" and password == ""):
            self.ids.username.error = True
            self.ids.password.error = True
        else:
            user = User(username= self.ids.username.text,
                        password = self.ids.password.text)
            session.add(user)
            session.commit()
            self.manager.current="logIn"


 

class Index(Screen):
        
        def on_enter(self, *args):
           self.ids.table.clear_widgets()

           table_data = []
           
           for item in session.query(Task):
               new_item = (str(item.id), item.task, item.info)
               table_data.append(new_item)

           table = MDDataTable(size_hint=(0.9,0.6), 
                               check = True,
                               rows_num=10,
                               column_data=[
                                    ("No.", dp(30)),
                                    ("Task", dp(30)),
                                    ("Info ", dp(30))
                                ], row_data=table_data
                            )
           table.bind(on_row_press = self.check_press)

           self.ids.table.add_widget(table)
           
        def check_press(self, instance_table, instance_row):
            row_num = int(instance_row.index/len(instance_table.column_data))

            row_data = instance_table.row_data[row_num]
            
            # print(row_num)
            # print(row_data)

            self.id = row_data[0]
            self.task =  row_data[1] 
            self.info = row_data[2]
            
            close_btn = MDRectangleFlatIconButton(icon="close-circle", text="Close", on_release=self.close_dialog)
            edit_btn = MDRectangleFlatIconButton(icon="application-edit", text="Edit", on_release =self.edit_dialog)
            Delete_btn = MDRectangleFlatIconButton(icon="delete", text="Delete", on_release = self.delete_dialog)

            self.dialog = MDDialog(title = f'Edit {self.task}',
                              text = f'Info about task \nId: {self.id}, \nTask: {self.task} \nInfo: {self.info}',
                              size_hint = (0.9,0.7),
                              buttons= [close_btn,edit_btn,Delete_btn])


            self.dialog.open()

        def close_dialog(self, obj):
            self.dialog.dismiss()
        
        def edit_dialog(self,obj):

            self.dialog.dismiss()
            
            self.manager.get_screen('editTask').ids.edit_task.title = self.task
            self.manager.get_screen('editTask').ids.edit_task_name.text = self.task
            self.manager.get_screen('editTask').ids.edit_task_info.text = self.info
            self.manager.get_screen('editTask').ids.id_task.text = self.id
 

            self.manager.current="editTask"



               
        def delete_dialog(self,obj):
            
            self.dialog.dismiss()
            
            #Create a function to delete task from database
            self.manager.get_screen('delete_task').ids.id_label_delete.text = self.id
            self.manager.get_screen('delete_task').ids.info_task_delete.text = f'Task: {self.task}\n Info: {self.info}'
            self.manager.current="delete_task"

           

        




class AddTask(Screen):

    def add_task(self):
        task  = self.ids.task_name.text
        info = self.ids.infoTask.text

        if task == "" or info == "":
            self.ids.task_name.error = True
            self.ids.infoTask.error = True
        else:
            task = Task(task = task, info = info)
            session.add(task)
            session.commit()

            self.ids.task_name.text =""
            self.ids.infoTask.text =""
            

            self.manager.current = "index"

      

class edittask(Screen):

    def edit_task(self):
        self.task = self.ids.edit_task_name.text
        self.info = self.ids.edit_task_info.text
        self.id = self.ids.id_task.text

        task_db = session.query(Task).filter(Task.id == int(self.id)).one_or_none()

        if self.task == "" or self.info == "" :
            self.ids.edit_task_name.error = True
            self.ids.edit_task_info.error = True
        else:    
            task_db.task = self.task
            task_db.info = self.info
            session.commit()
            self.manager.current = "index"
        

class deleteTask(Screen):
    
    def delete_task(self):
        self.id_delete = self.ids.id_label_delete.text

        task_for_delete = session.query(Task).filter(Task.id == int(self.id_delete)).one_or_none()
        session.delete(task_for_delete)
        session.commit()
        self.manager.current = "index"
        
   

sm = ScreenManager()
sm.add_widget(Home(name="Home"))
sm.add_widget(LogIn(name="logIn"))
sm.add_widget(SingUp(name="SingUp"))
sm.add_widget(Index(name='index'))
sm.add_widget(AddTask(name="addTask"))
sm.add_widget(edittask(name="editTask"))
sm.add_widget(deleteTask(name="delete_task"))


class App(MDApp):
    
    def build(self):
        self.theme_cls.primary_palette = 'Orange'
        self.theme_cls.theme_style= 'Dark'
        screen = Builder.load_file('screenManager.kv')

        return screen


if __name__ == "__main__":
    Window.size= (360,640)
    Base.metadata.create_all(engine)

    App().run()