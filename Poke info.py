#Tharun Tilakumara-10L 2019/4/29
#This is probably the most jumbled spaggeti code i have made to date
#pokeapi.co

import requests
import PIL
from tkinter import*
import tkinter as tk
from PIL import Image, ImageTk

#functions start here

#asks user for pokemon name or id

def get_input():
    repeat=True
    while repeat==True:
        name_or_id=input("name :or id? n/i : ")
        print("")
        name_or_id=name_or_id.lower()
        
        if name_or_id=="n":
            repeat=False
            pokemon=input("Enter a pokemon name: ")
            print("")
            pokemon=pokemon.lower()           
        elif name_or_id=="i":
            repeat=False
            pokemon=int(input("Enter a pokemon ID: "))
            print("")           
        else:
            continue
        
        return pokemon


    
# set api-endpoints and sets parameters
def set_url_and_params(pokemon):
    global URL1,URL2,URL3,PARAMS1,PARAMS2,PARAMS3
    URL1 = ("http://pokeapi.co/api/v2/pokemon/{0}".format(pokemon))
    URL2 = ("http://pokeapi.co/api/v2/pokemon-species/{0}".format(pokemon))
    URL3 = ("https://pokeapi.co/api/v2/pokemon-species/{0}".format(pokemon))
    # defining a params dict for the parameters to be sent to the API 
    PARAMS1 = {"types":pokemon}
    PARAMS2 = {"flavor_text_entries":pokemon}
    PARAMS3 = {"generation":pokemon}



# sending get request and saving the response as response object
def request_data():
    global data1,data2,data3
    
    response1 = requests.get(url = URL1, params = PARAMS1) 
    response2 = requests.get(url = URL2, params = PARAMS2) 
    response3 = requests.get(url = URL3, params = PARAMS3)
    
    if response1.status_code==200:
        print("Successful connection")
    elif response1.status_code==404:
        print("\n",response1.status_code)
        print("Not Found")
        return True
        
    
    if response2.status_code==200:
        print("Successful connection")
    elif response2.status_code==404:
        print("\n",response2.status_code)
        print("Not Found")
        return True

    if response3.status_code==200:
        print("Successful connection")
    elif response3.status_code==404:
        print("\n",response3.status_code)
        print("Not Found")
        return True

    data1 = response1.json()
    data2 = response2.json()
    data3 = response3.json()




#searches through jsons to find and assign info to variables
def search_for_data():       
#data 1
    poke_name=data1["name"]
    poke_ID=data1["id"]
    poke_type=data1["types"][0]["type"]["name"]
    poke_height=data1["height"]
    poke_generation=data2["generation"]["name"]
    
    #get sprite and convert to useable form
    global sprite_available
    sprite_available=True
    try:
        r=requests.get(data1["sprites"]["front_default"])
        with open("poke_sprite.png","wb") as f:
            f.write(r.content)
            
    except requests.exceptions.MissingSchema as error:
        print("could not find pokemon sprite \n")
        sprite_available=False

#data2
    #exception correction for error in database. (languages incorrect)
    if data2["flavor_text_entries"][1]["language"]["name"]=="en":
        poke_dex_entry=data2["flavor_text_entries"][1]["flavor_text"]
    else:
        poke_dex_entry=data2["flavor_text_entries"][2]["flavor_text"]
#data3
                  
    attributes=[poke_ID,poke_name,poke_type,poke_height,poke_generation,poke_dex_entry]
    return attributes


#formats the splash text so that it fits on the display window
def format_Splash_text(text):
    words=text.split()
    count=0
    sentence=""

    for word in words:
        sentence=sentence+" "+word
        count+=1

        if count==4:
            sentence=sentence+"\n"  
            count=0

    return sentence
    


#formats data to be easily readable
def display(attributes):
    print("\n")
    print("ID: ",attributes[0])
    print("NAME: ",attributes[1])
    print("TYPE: ",attributes[2])
    print("HEIGHT: ",attributes[3]*10,"cm")
    print("GENERATION: ",attributes[4])
    print("POKEDEX ENTRY: ",attributes[5],"\n")
    
    display_window(attributes)


#this function is a liiiiiiiitle too long        
def display_window(attributes):
    window=Tk()
    window.title(attributes[1])
    window.geometry("270x510") #dimensions of the window
    window.configure(background='black')
    

    topframe=Frame(window)
    topframe.pack()
    bottomframe=Frame(window)
    bottomframe.pack(side="bottom")
    
    
    
    if sprite_available==True:
        #resizing sprite image
        sprite=Image.open("poke_sprite.png")
        
        baseheight=200 #variable 
        hpercent = (baseheight/float(sprite.size[1]))
        wsize = int((float(sprite.size[0])*float(hpercent)))
        sprite=sprite.resize((wsize,baseheight), PIL.Image.ANTIALIAS)
        sprite.save("poke_sprite.png")
        img=ImageTk.PhotoImage(Image.open("poke_sprite.png"))
        
        #placing sprite image in top frame  
        panel=Label(topframe,image=img)
        panel.pack(side="right",fill='both',expand="yes")


    #creating and placing the text for all the subtitles bellow
    name=Label(window,text="NAME: "+attributes[1],font="Verdana 20 ",fg="white",bg="black")
    name.place(x=10,y=210)
    
    ID=Label(window,text="ID: "+str(attributes[0]),fg="white",bg="black")
    ID.place(x=10,y=240)
    
    Type=Label(window,text="TYPE: "+str(attributes[2]),fg="white",bg="black") 
    Type.place(x=10,y=260)

    height_cm=attributes[3]*10
    height_cm=str(height_cm)
    Height=Label(window,text="HEIGHT: "+height_cm+"cm",fg="white",bg="black")
    Height.place(x=10,y=280)
    
    Generation=Label(window,text="GENERATION: "+attributes[4],fg="white",bg="black")
    Generation.place(x=10,y=300)


    Dex_entry=Label(window,text="POKEDEX ENTRY: ",fg="white",bg="black")
    formatted_Splash_text=format_Splash_text(attributes[5])
    Splash_text=Label(window,text=formatted_Splash_text,anchor='w',justify=LEFT,fg="white",bg="black")
    Dex_entry.place(x=10,y=320)
    Splash_text.place(x=10,y=340)

    
    window.mainloop()
  
    


#main program starts here

#ask again or quit

again=True
while again==True:
    
    pokemon=get_input()
    set_url_and_params(pokemon)
    error=request_data()
    print("Error status: ",error,"\n")

    if error!=True:
        attributes=search_for_data()
        display(attributes)
    else:
        print("Something went wrong, try again\n")

    while True:
        
        ans=input("ask again? y/n: ")
        ans=ans.lower()
        
        if ans=="n":
            exit()
        elif ans=="y":
            break
        else:
            continue



