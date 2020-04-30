import tkinter as tk
from gmail_reader import GMailReader
from gmail_sender import GMailSender
from message_maker import create_message
import sys

############### VIEW YOUR MAIL SCREEN ################
WIDTH=600
HEIGHT=600
SELF = sys.argv[1]
if(not SELF):
    sys.exit("Email-ID not specified")

def view_screen_pre(root, qry, foldr, subj, rcr):
    query = ""
    qry = qry.get()
    print(qry)
    if(qry != ""):
        query += qry
    else:
        query += "scootsy"
    foldr = foldr.get()
    if(foldr != ""):
        query += " in:"+foldr
    subj = subj.get()
    if(subj != ""):
        query += " subject:"+subj
    rcr = rcr.get()
    if(rcr != ""):
        query += " to: "+rcr
    reader = GMailReader()
   
    mail = reader.get_single_message(query)
    if(not mail):
        print("no mail found")
    view_screen(root, mail)

def view_screen(rt, mail):
    frm = "From"
    subject = "Subject"
    body = "Body"
    try:
        headers = mail['payload']['headers']
        for header in headers:
            if(header['name'] == "Subject"):
                subject = header['value']
            if(header['name'] == "From"):
                frm = header['value']
        body = mail['snippet']
        print("body")
    except Exception as e:
        print(str(e))
    root = tk.Toplevel()
    w = WIDTH 
    h = HEIGHT 
    ws = root.winfo_screenwidth() 
    hs = root.winfo_screenheight() 
    x = (ws/2) - (w/2) 
    y = (hs/2) - (h/2)
    root.geometry('+%d+%d' % (x, y)) 
    root.resizable(True, True) 
    root.title("VIEW MAIL")
    
    canvas = tk.Canvas(root, height=HEIGHT , width=WIDTH)
    canvas.pack()
    
    frame = tk.Frame(root, bg='#80c1ff')
    frame.place(relx='0.1',rely='0.1',relheight='0.8',relwidth='0.8')
    
    button = tk.Button(frame, text='Main', bg='grey', command = lambda rt=root: main_screen(rt)) 
    button.place(relx=0.05,rely='0.9',relheight='0.05',relwidth='0.2')
    
    button = tk.Button(frame, text='Download', bg='grey') 
    button.place(relx=0.35,rely='0.9',relheight='0.05',relwidth='0.25')
    
    button = tk.Button(frame, text='Delete', bg='grey') 
    button.place(relx=0.7,rely='0.9',relheight='0.05',relwidth='0.2')
    
    label = tk.Label(frame, text='From') 
    label.place(relx=0.05,rely='0.05',relheight='0.05',relwidth='0.15')
    
    label = tk.Label(frame, text='Subject') 
    label.place(relx=0.05,rely='0.25',relheight='0.05',relwidth='0.15')
    
    label = tk.Label(frame, text='Message') 
    label.place(relx=0.05,rely='0.45',relheight='0.05',relwidth='0.15')
    
    label = tk.Label(frame, bg='white', text=frm) 
    label.place(relx=0.35,rely='0.05',relheight='0.05',relwidth='0.6')
    
    label = tk.Label(frame, bg='white' , text=subject) 
    label.place(relx=0.35,rely='0.25',relheight='0.05',relwidth='0.6')
    
    label = tk.Label(frame, bg='white',text=body, wraplength=250)
    label.place(relx=0.35,rely='0.45',relheight='0.3',relwidth='0.6')
    rt.destroy()
    root.mainloop()

########## SEARCH EMAIL SCREEN  ###############

def search_screen(rt):
    root = tk.Toplevel()
    w = WIDTH 
    h = HEIGHT 
    ws = root.winfo_screenwidth() 
    hs = root.winfo_screenheight() 
    x = (ws/2) - (w/2) 
    y = (hs/2) - (h/2)
    root.geometry('+%d+%d' % (x, y)) 
    root.resizable(True, True) 
    root.title("SEARCH EMAIL")

    rcr = tk.StringVar()
    subj = tk.StringVar()
    foldr = tk.StringVar()
    qry = tk.StringVar()
    
    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()
    
    frame = tk.Frame(root, bg='#80c1ff', bd=5)
    frame.place(relx=0.5, relwidth=1, relheight=0.7, anchor='n')
    
    frame_lower = tk.Frame(root, bg='yellow', bd=5)
    frame_lower.place(relx=0.5,rely =0.7, relwidth=1, relheight=0.3, anchor='n')
    
    label_r= tk.Label(frame,font = 40, text = 'Receiver' ,)
    label_r.place(relx = 0.1, rely = 0.05, relheight = 0.05, relwidth = 0.3 )
    
    receiver = tk.Entry(frame, font = 40, textvariable=rcr)
    receiver.place(relx = 0.1, rely = 0.1, relheight = 0.1 ,relwidth = 0.3)

    label_s= tk.Label(frame,font = 40, text = 'Subject' ,)
    label_s.place(relx = 0.6, rely = 0.05, relheight = 0.05, relwidth = 0.3 )
    
    subject = tk.Entry(frame, font = 40, textvariable=subj)
    subject.place(relx = 0.6, rely = 0.1, relheight = 0.1 ,relwidth = 0.3)
    
    label_q= tk.Label(frame, font = 40, text = 'Query Phrase' ,)
    label_q.place(relx = 0.6, rely = 0.55, relheight = 0.05, relwidth = 0.3 )
    
    query = tk.Entry(frame, font = 40, textvariable=qry)
    query.place(relx = 0.6, rely = 0.6, relheight = 0.1 ,relwidth = 0.3)
    
    label_f= tk.Label(frame, font = 40, text = 'Folder' ,)
    label_f.place(relx = 0.1, rely = 0.55, relheight = 0.15, relwidth = 0.25 )
    
    OPTIONS = [
    "Unread",
    "Sent",
    "Inbox",
    "Trash",
    "Anywhere"
    ] 
    
    w = tk.OptionMenu(frame, foldr, *OPTIONS)
    w.place(relx = 0.35, rely = 0.55, relheight = 0.15, relwidth = 0.05)
    
    main_page = tk.Button(frame_lower, text = 'Main Page', font = 40, command = lambda rt=root: main_screen(rt))
    main_page.place(relx = 0.1, rely = 0.40, relheight = 0.3, relwidth = 0.3)
    
    search = tk.Button(frame_lower, text = 'Search', font = 40, command = lambda root=root:view_screen_pre(root, qry, foldr, subj, rcr))
    search.place(relx = 0.6, rely = 0.40, relheight = 0.3, relwidth = 0.3)
    rt.destroy()

    root.mainloop()
#search_screen()




###### SEND EMAIL SCREEN #########
def send(to, subject, body):
    sender = GMailSender()
    if(to.get() != "" and subject.get() != "" and body != ""):
        sender.send_mail(create_message(SELF, to.get(), subject.get(), body))
    else:
        print("Incomplete fields")

def send_mail_screen(rt):
    root = tk.Toplevel() 
    root.title("SEND E-MAIL") 
    w = WIDTH 
    h = HEIGHT  
    ws = root.winfo_screenwidth() 
    hs = root.winfo_screenheight() 
    x = (ws/2) - (w/2) 
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y)) 
    root.resizable(True, True) 
    root.configure(background='bisque')
    large_font = ('Verdana',20)
    largest_font = ('Verdana',70)
    small_font = ('Verdana',10)

    to = tk.StringVar()
    subject = tk.StringVar()

    tk.Label(root, text="To",width='5', height='2').place(x=15, y=3)
    sendingtoEntry = tk.Entry(root, width = '20', textvariable=to, font=large_font).place(x=70, y=7)

    tk.Label(root, text="Subject",width='5', height='2').place(x=15, y=50)
    sendingtoEntry = tk.Entry(root, width = '20', textvariable=subject, font=large_font).place(x=70, y=50)
    
    tk.Label(root, text="Body",width='5', height='7').place(x=15, y=97)
    bodyEntry = tk.Text(root,height='11', width = '42',font=small_font)
    bodyEntry.place(x=70, y=97)
    
    # Button(root, text="Attachment", bg="#e79700", width=30, height=2, font=("Open Sans", 13, 'bold'), fg='white' ).place(x=100,y=180)
           
    # Button(root, text="Draft", bg="#e79700", width=10, height=2, font=("Open Sans", 13, 'bold'), fg='white' ).place(x=100,y=300)
    tk.Button(root, text="Send", bg="#e79700", width=10, height=2, font=("Open Sans", 13, 'bold'), fg='white', command = lambda bodyEntry=bodyEntry:send(to, subject, bodyEntry.get("1.0","end-1c"))).place(x=280,y=300)
    tk.Button(root, text="Main", bg="#e79700", width=10, height=3, font=("Open Sans", 13, 'bold'), fg='white', command = lambda rt=root: main_screen(rt)).place(x=15,y=400)
    rt.destroy()
    root.mainloop()

#send_mail_screen()
   
#################  MAIN initial screen  ###################
 
def main_screen(rt=None):
    root = tk.Toplevel()
    w = WIDTH 
    h = HEIGHT 
    ws = root.winfo_screenwidth() 
    hs = root.winfo_screenheight() 
    x = ws/2 - h/2
    y = hs/2 - h/2

    root.geometry('+%d+%d' % (x, y)) 
    root.resizable(True, True) 
    root.title("THE MAIL APP")
    
    canvas = tk.Canvas(root, height=HEIGHT , width=WIDTH)
    canvas.pack()
    
    frame = tk.Frame(root, bg='peach puff')
    frame.place(relx='0.1',rely='0.1',relheight='0.8',relwidth='0.8')
    
    label = tk.Label(frame, text='Home Screen', bg='peach puff') 
    label.place(relx='0.35',rely='0.25',relheight='0.15',relwidth='0.25')
    
    button = tk.Button(frame, text='View', bg='white', command = view_screen)
    button.place(relx='0.05',rely='0.4',relheight='0.20',relwidth='0.2')
    
    button = tk.Button(frame, text='Search', bg='white', command = lambda rt=root:search_screen(rt) )
    button.place(relx='0.35',rely='0.4',relheight='0.20',relwidth='0.25')
    
    button = tk.Button(frame, text='Send', bg='white',command = lambda rt=root:send_mail_screen(rt) )
    button.place(relx='0.7',rely='0.4',relheight='0.20',relwidth='0.2')
    if(rt):
        rt.destroy()
    root.mainloop()
main_screen()    

