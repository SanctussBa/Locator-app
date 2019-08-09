from tkinter import *
from tkinter import messagebox
from geopy.geocoders import Nominatim
import pandas
import csv
import folium
import webbrowser



window = Tk()
window.title("My World")
window.iconbitmap("icon.ico")
window.geometry("706x482")



def delete():
     MsgBox = messagebox.askquestion('Delete all Locations','Are you sure you want to delete all data?')
     if MsgBox =='yes':    
          f = open('try3.csv','w')
          f.truncate()
          f.close()
          f = open('try3.csv','a')
          f.write('category,street,zip,city,country,notes,lat,lon\n')
          f.close()
     else:
          pass
     
def statistics():
     
     frame_main.pack_forget()
     frame_address.pack_forget()
     frame_city.pack_forget()
     frame_category_list.pack_forget()
     frame_country_list.pack_forget()
     frame_stat.pack(expand=YES, fill=BOTH)
     
     f = pandas.read_csv('try3.csv')
     f1 = pandas.DataFrame(f)
     total = f1.shape[0]# counts total amount of rows in DataFrame INT

     a = f1.country.nunique()# COUNTS AMOUNT OF UNIQUE VALUES IN COLUMN 'COUNTRY' INT

     b = f1.country.value_counts().head(3)
     if b.empty ==True:
          c = '0'
     else:
          c = b.to_string()# STRING TOP 3 COUNTRIES VISITED

     d = f1.city.nunique() #CITIES VISITED TOTAL AMOUNT INT

     e = f1.city.value_counts().head(3)
     if e.empty==True:
          g = '0'
     else:
          g = e.to_string() # STRING TOP 3 CITIES VISITED

     h = f1.loc[(f1['category']=='vacation')]
     j = h.shape[0]

     i = f1.loc[(f1['category']=='work')]
     k = i.shape[0]
     
     l = f1.loc[(f1['category']=='living')]
     m = l.shape[0]
     
     n = f1.loc[(f1['category']=='other')]
     o = n.shape[0]
     
     
     stat_label.grid(row=1, column=0, rowspan=2, sticky=N, pady=30, padx=30)
     stat_label.config(text="The total amount of all locations: "+str(total)+"\n\n"
                       +"Countries visited: "+str(a)+"\n\n"
                       +"Top 3 Countries visited:\n"+c+"\n"
                       +"\nCities Visited: "+str(d)+"\n\n"
                       +"Top 3 Cities visited:\n"+g+"\n")

     by_category.grid(row=1, column=1, sticky=N, pady=30, padx=30)
     by_category.config(text="You have been to :\n\n"+str(j)+" locations on vacation"
                        +"\n"+str(k)+" locations for work"
                        +"\n"+str(m)+" locations living"
                        +"\n"+str(o)+" other locations")
     
     globe.grid(row=2, column=1, sticky=N)
     
def see_all_locations():
     f = pandas.read_csv('try3.csv')


     f1 = f[['lat','lon','notes','category']]

     big_map = folium.Map([f1['lat'].mean(),f1['lon'].mean()],zoom_start=3)
     fg = folium.FeatureGroup(name='All')
     for lat, lon, note, cat in zip(f1['lat'],f1['lon'],f1['notes'], f1['category']):

         if cat == 'living':
             fg.add_child(folium.Marker(location=[lat,lon],popup='<b>'+str(note)+'</b>', icon=folium.features.CustomIcon('homelogo.png', icon_size=(40,40))))
         elif cat == 'work':
             fg.add_child(folium.Marker(location=[lat,lon],popup='<b>'+str(note)+'</b>', icon=folium.features.CustomIcon('logowork.png', icon_size=(60,60))))
         elif cat == 'vacation':
             fg.add_child(folium.Marker(location=[lat,lon],popup='<b>'+str(note)+'</b>', icon=folium.features.CustomIcon('vacationlogo.png', icon_size=(60,60))))
         else:
             fg.add_child(folium.Marker(location=[lat,lon],popup='<b>'+str(note)+'</b>', icon=folium.features.CustomIcon('otherlogo.png', icon_size=(60,60))))

                  
     big_map.add_child(fg)
     big_map.save("All.html")
     webbrowser.open_new('All.html')


     
def by_country():
     def list_of_cities(event):
          def show_notes(event):
               def update_label(event):
                    def show_location():
                         global list_notes
                         f = pandas.read_csv('try3.csv')
                         sel_note = list_notes.curselection()[0]
                         c = list_notes.get(sel_note)
                         n = f.loc[f['notes'] ==str(c),['notes']]
                         n1 = n.values.tolist()
                         n2 = str(n1[0][0])
                         f3 = f.loc[f['notes'] ==str(c),['lat']]
                         f4 = f.loc[f['notes'] ==str(c),['lon']]
                         f5 = f3.values.tolist()
                         f6 = f4.values.tolist()
                         lat_lon = f5[0]+f6[0]
                         icon = folium.features.CustomIcon('homelogo.png',icon_size=(30,30))
                         map3 = folium.Map(location=lat_lon)
                         fg = folium.FeatureGroup(name='My Location')
                         fg.add_child(folium.Marker(location=lat_lon, icon=icon, popup='<b>'+n2+'</b>'))
                         map3.add_child(fg)
                         map3.save('Map3.html')
                         webbrowser.open_new('Map3.html')

                     
                    global list_notes
                    f = pandas.read_csv('try3.csv')
                       
                    b_show_location.grid(row=1,column=2)
                    b_show_location.configure(command=show_location) 

                       
                    note_label2.grid(row=1,column=1)
                    sel_note = list_notes.curselection()[0]
                    c = list_notes.get(sel_note)
                    f1 = f.loc[f['notes']==str(c),['street','zip','city','country','notes']]
                    f2 = f1.values.tolist()
                    a = str(f2[0][0])+', '+str(f2[0][1])
                    b= str(f2[0][2])
                    c= str(f2[0][3])
                    d= str(f2[0][4])
                    if str(f2[0][0])=='nan':
                         e = "City: "+b+"\nCountry: "+c+"\nNotes: "+d
                         note_label2.configure(text=e)
                    else:
                         e = "Address: "+a+"\nCity: "+b+"\nCountry: "+c+"\nNotes: "+d
                         note_label2.configure(text=e)
                  
               
               global list_notes, list_cities, b_show_location
               list_notes.delete(0,'end')
               b_show_location.grid_forget()
               note_label2.grid_forget()
                  
               f = pandas.read_csv('try3.csv')
               sel_city = list_cities.curselection()
               if len(sel_city)>0:
                    sel_city=int(list_cities.curselection()[0])
                    selection = list_cities.get(sel_city)
                    active = [list_cities.get(int(i)) for i in list_cities.curselection()]
                    sel_note = f.loc[(f['city']==str(selection))]
                    list_sel_notes = list(sel_note['notes'])
                    unique_notes = []
                    for x in list_sel_notes:
                         if x not in unique_notes:
                              unique_notes.append(x)
                    for x in unique_notes:
                         list_notes.insert('end',x)
                           
               list_notes.bind('<<ListboxSelect>>', update_label)


          def show_country():
               
               f = pandas.read_csv('try3.csv')
               sel_country = list_countries.curselection()[0]
               selection = list_countries.get(sel_country)
               f2 = f.loc[(f['country']==str(selection))]

               f3 = f2[['lat','lon','notes','category']]
               map2 = folium.Map([f3['lat'].mean(),f3['lon'].mean()],zoom_start=5)

               fg = folium.FeatureGroup(name='By Country')

               for lat, lon, note, cat in zip(f3['lat'],f3['lon'],f3['notes'], f3['category']):
                    if cat == 'living':
                         fg.add_child(folium.Marker(location=[lat,lon],popup='<b>'+str(note)+'</b>', icon=folium.features.CustomIcon('homelogo.png', icon_size=(40,40))))
                    elif cat == 'work':
                         fg.add_child(folium.Marker(location=[lat,lon],popup='<b>'+str(note)+'</b>', icon=folium.features.CustomIcon('logowork.png', icon_size=(60,60))))
                    elif cat == 'vacation':
                         fg.add_child(folium.Marker(location=[lat,lon],popup='<b>'+str(note)+'</b>', icon=folium.features.CustomIcon('vacationlogo.png', icon_size=(60,60))))
                    else:
                         fg.add_child(folium.Marker(location=[lat,lon],popup='<b>'+str(note)+'</b>', icon=folium.features.CustomIcon('otherlogo.png', icon_size=(60,60))))

               map2.add_child(fg)
               map2.save("Map2.html")
               webbrowser.open_new('Map2.html')


          try:
                    
               f = pandas.read_csv('try3.csv')
               list_cities.delete(0,'end')
               list_notes.delete(0,'end')
               b_show_location.grid_forget()
               note_label2.grid_forget()
              
               sel_country = list_countries.curselection()
               if len(sel_country)>0:
                    sel_country=int(list_countries.curselection()[0])
                    selection = list_countries.get(sel_country)
                    active = [list_countries.get(int(i)) for i in list_countries.curselection()]

      
                    sel_city = f.loc[(f['country']== str(selection))]
                    list_sel_cities = list(sel_city['city'])
                    unique_cities = []
                    for x in list_sel_cities:
                         if x not in unique_cities:
                              unique_cities.append(x)
                    for x in unique_cities:
                         list_cities.insert('end',x)
               b_country.grid(row=1,column=0, sticky=N, pady=25)
               b_country.configure(text="Show all locations\nin "+str(selection))
               b_country.configure(command=show_country)

               list_cities.bind('<<ListboxSelect>>', show_notes)

          except UnboundLocalError:
               pass
                 

     f = pandas.read_csv('try3.csv')

     frame_main.pack_forget()
     frame_address.pack_forget()
     frame_city.pack_forget()
     frame_category_list.pack_forget()
     frame_stat.pack_forget()
     
     frame_country_list.pack(expand=YES, fill=BOTH)

     frame11.grid(row=1,column=0, padx=70, sticky=N)


     list_countries.grid(row=0,column=0)
     list_cities.grid(row=0,column=1)
     list_notes.grid(row=0,column=2)

     
     list_cities.delete(0,'end')
     list_notes.delete(0,'end')

     # CREATE A LIST IN 'COUNTRY LIST' LISTBOX WITH UNIQUE COUNTRIES
     countries_indata = f['country']
     list_countries1 = countries_indata.tolist()
     unique_countries = []
     for x in list_countries1:
          if x not in unique_countries:
               unique_countries.append(x)
     for x in unique_countries:
          list_countries.insert('end',x)

     # GRID AND UPGRADE INFO LABEL WITH NUMBER OF COUNTRIES VISITED
     l_info.grid(row=0,column=0,columnspan=3)
     nr_of_countries = len(unique_countries)
     l_info.configure(text="You have visited "+str(nr_of_countries)+" countries!")



     list_countries.bind('<<ListboxSelect>>', list_of_cities)

     b_show_location.grid_forget()
     note_label2.grid_forget()


def category():
     def living_countries():
          def living_cities(event):
               def living_notes(event):
                    def info_label(event):
                         def show_location():
                              global listbox_notes
                              f = pandas.read_csv('try3.csv')
                             
                              sel_note = listbox_notes.curselection()[0]
                              c = listbox_notes.get(sel_note)
                              n = f.loc[f['notes'] ==str(c),['notes']]
                              n1 = n.values.tolist()
                              n2 = str(n1[0][0])
                              f3 = f.loc[f['notes'] ==str(c),['lat']]
                              f4 = f.loc[f['notes'] ==str(c),['lon']]
                              f5 = f3.values.tolist()
                              f6 = f4.values.tolist()
                              lat_lon = f5[0]+f6[0]
                             
                              icon = folium.features.CustomIcon('homelogo.png',icon_size=(40,40))
                             
                              map1 = folium.Map(location=lat_lon)
                              fg = folium.FeatureGroup(name='My Location')
                              fg.add_child(folium.Marker(location=lat_lon, icon=icon, popup='<b>'+n2+'</b>'))
                              map1.add_child(fg)
                              map1.save('Map.html')
                              webbrowser.open_new('Map.html')
                        
                         global note_label, listbox_notes
                         f = pandas.read_csv('try3.csv')
                         note_label.grid(row=1, column=0, columnspan=2)
                         b_show.grid(row=1,column=2)
                         b_show.configure(command=show_location)
                         sel_note = listbox_notes.curselection()[0]
                         c = listbox_notes.get(sel_note)
                         
                         
                         f1 = f.loc[f['notes']==str(c),['street','zip','city','country','notes']]
                         f2 = f1.values.tolist()
                         
                         a = str(f2[0][0])+', '+str(f2[0][1])
                         b = str(f2[0][2])
                         c = str(f2[0][3])
                         d = str(f2[0][4])
                         if str(f2[0][0]) =='nan':
                              e = "City: "+b+"\nCountry: "+c+"\nNotes: "+d
                              note_label.configure(text=e)
                         else:
                             
                              e = "Address: "+a+"\nCity: "+b+"\nCountry: "+c+"\nNotes: "+d
                              note_label.configure(text=e)
                                                 
                    
                    global listbox_notes, listbox_cities
                    f = pandas.read_csv('try3.csv')
                    listbox_notes.delete(0,'end')
                    b_show.grid_forget()
                    note_label.grid_forget()

                    sel_city = listbox_cities.curselection()
                    if len(sel_city) > 0:
                         sel_city = int(listbox_cities.curselection()[0])
                         selection = listbox_cities.get(sel_city)
                         active = [listbox_cities.get(int(i)) for i in listbox_cities.curselection()]
                                        
                         selection = listbox_cities.get(sel_city)
                         sel_notes = f.loc[(f['category']=='living') & (f['city'] == str(selection))]
                         list_sel_notes = list(sel_notes['notes'])
                         unique_notes_living = []
                         for x in list_sel_notes:
                              if x not in unique_notes_living:
                                   unique_notes_living.append(x)
                         for x in unique_notes_living:
                              listbox_notes.insert('end', x)
                    listbox_notes.bind('<<ListboxSelect>>', info_label)    

                    
               global listbox_countries, unique_countries_living
               global listbox_cities, country_living
               f = pandas.read_csv('try3.csv')
               listbox_cities.delete(0,'end')
               listbox_notes.delete(0,'end')
                 
               b_show.grid_forget()
               note_label.grid_forget()
                 

               sel_country = listbox_countries.curselection()
               if len(sel_country) > 0:
                    sel_country =int(listbox_countries.curselection()[0])
                    selection = listbox_countries.get(sel_country)
                    active = [listbox_countries.get(int(i)) for i in listbox_countries.curselection()]
                 
                    sel_city = f.loc[(f['category']=='living') & (f['country'] == str(selection))]
                    list_sel_cities = list(sel_city['city'])
                    unique_cities_living = []
                    for x in list_sel_cities:
                         if x not in unique_cities_living:
                              unique_cities_living.append(x)
                    for x in unique_cities_living:
                         listbox_cities.insert('end', x)
               listbox_cities.bind('<<ListboxSelect>>', living_notes)

            
          global listbox_countries, listbox_cities, listbox_notes
          f = pandas.read_csv('try3.csv')

          listbox_countries.delete(0,'end')
          listbox_cities.delete(0,'end')
          listbox_notes.delete(0,'end')

          b_show.grid_forget()
          note_label.grid_forget()

          country_living = f.loc[f['category'] == 'living']
          list_country_living = list(country_living['country'])
          unique_countries_living = []

          for x in list_country_living:
               if x not in unique_countries_living:
                    unique_countries_living.append(x)
          for x in unique_countries_living:
               listbox_countries.insert('end', x)
          listbox_countries.bind('<<ListboxSelect>>', living_cities)

     def working_countries():
          def working_cities(event):
               def working_notes(event):
                    def info_label(event):
                         def show_location():
                        
                              global listbox_notes
                              f = pandas.read_csv('try3.csv')
                             
                              sel_note = listbox_notes.curselection()[0]
                              c = listbox_notes.get(sel_note)
                              n = f.loc[f['notes'] ==str(c),['notes']]
                              n1 = n.values.tolist()
                              n2 = str(n1[0][0])
                              f3 = f.loc[f['notes'] ==str(c),['lat']]
                              f4 = f.loc[f['notes'] ==str(c),['lon']]
                              f5 = f3.values.tolist()
                              f6 = f4.values.tolist()
                              lat_lon = f5[0]+f6[0]
                             
                              icon = folium.features.CustomIcon('logowork.png',icon_size=(50,50))
                             
                              map1 = folium.Map(location=lat_lon)
                              fg = folium.FeatureGroup(name='My Location')
                              fg.add_child(folium.Marker(location=lat_lon, icon=icon, popup='<b>'+n2+'</b>'))
                              map1.add_child(fg)
                              map1.save('Map.html')
                              webbrowser.open_new('Map.html')
                        
                         global note_label, listbox_notes
                         f = pandas.read_csv('try3.csv')
                         note_label.grid(row=1, column=0, columnspan=2)
                         b_show.grid(row=1,column=2)
                         b_show.configure(command=show_location)
                         sel_note = listbox_notes.curselection()[0]
                         c = listbox_notes.get(sel_note)
                         
                         
                         f1 = f.loc[f['notes']==str(c),['street','zip','city','country','notes']]
                         f2 = f1.values.tolist()
                         
                         a = str(f2[0][0])+', '+str(f2[0][1])
                         b = str(f2[0][2])
                         c = str(f2[0][3])
                         d = str(f2[0][4])
                         if str(f2[0][0]) =='nan':
                             e = "City: "+b+"\nCountry: "+c+"\nNotes: "+d
                             note_label.configure(text=e)
                         else:
                             
                             e = "Address: "+a+"\nCity: "+b+"\nCountry: "+c+"\nNotes: "+d
                             note_label.configure(text=e)

                        
                    global listbox_notes, listbox_cities
                    f = pandas.read_csv('try3.csv')
                    listbox_notes.delete(0,'end')
                     
                    b_show.grid_forget()
                    note_label.grid_forget()
                     
                    sel_city = listbox_cities.curselection()
                    if len(sel_city) > 0:
                         sel_city = int(listbox_cities.curselection()[0])
                         selection = listbox_cities.get(sel_city)
                         active = [listbox_cities.get(int(i)) for i in listbox_cities.curselection()]               
                         selection = listbox_cities.get(sel_city)
                         sel_notes = f.loc[(f['category']=='work') & (f['city'] == str(selection))]
                         list_sel_notes = list(sel_notes['notes'])
                         unique_notes_working = []
                         for x in list_sel_notes:
                              if x not in unique_notes_working:
                                   unique_notes_working.append(x)
                         for x in unique_notes_working:
                              listbox_notes.insert('end', x)

                    listbox_notes.bind('<<ListboxSelect>>', info_label)
                    
               global listbox_countries, unique_countries_working
               global listbox_cities, country_working
               f = pandas.read_csv('try3.csv')
               listbox_cities.delete(0,'end')
               listbox_notes.delete(0,'end')
                 
               b_show.grid_forget()
               note_label.grid_forget()
                 

               sel_country = listbox_countries.curselection()
               if len (sel_country) > 0:
                    sel_country = int(listbox_countries.curselection()[0])
                    selection = listbox_countries.get(sel_country)
                    active = [listbox_countries.get(int(i)) for i in listbox_countries.curselection()]   
                    sel_city = f.loc[(f['category']=='work') & (f['country'] == str(selection))]
                    list_sel_cities = list(sel_city['city'])
                    unique_cities_working = []
                    for x in list_sel_cities:
                         if x not in unique_cities_working:
                              unique_cities_working.append(x)
                    for x in unique_cities_working:
                         listbox_cities.insert('end', x)
               listbox_cities.bind('<<ListboxSelect>>', working_notes)

                    
                
          global listbox_countries, listbox_cities, listbox_notes
          f = pandas.read_csv('try3.csv')
        
          listbox_countries.delete(0,'end')
          listbox_cities.delete(0,'end')
          listbox_notes.delete(0,'end')
        
          b_show.grid_forget()
          note_label.grid_forget()
        
          country_working = f.loc[f['category'] == 'work']
          list_country_working = list(country_working['country'])
          unique_countries_working = []
          n = []
          for x in list_country_working:
               if x not in unique_countries_working:
                    unique_countries_working.append(x)
          for x in unique_countries_working:
               listbox_countries.insert('end', x)

          listbox_countries.bind('<<ListboxSelect>>', working_cities)

     def vacation_countries():
          def vacation_cities(event):
               def vacation_notes(event):
                    def info_label(event):
                         def show_location():
                              global listbox_notes
                              f = pandas.read_csv('try3.csv')
                             
                              sel_note = listbox_notes.curselection()[0]
                              c = listbox_notes.get(sel_note)
                              n = f.loc[f['notes'] ==str(c),['notes']]
                              n1 = n.values.tolist()
                              n2 = str(n1[0][0])
                              f3 = f.loc[f['notes'] ==str(c),['lat']]
                              f4 = f.loc[f['notes'] ==str(c),['lon']]
                              f5 = f3.values.tolist()
                              f6 = f4.values.tolist()
                              lat_lon = f5[0]+f6[0]
                             
                              icon = folium.features.CustomIcon('vacationlogo.png',icon_size=(50,50))
                             
                              map1 = folium.Map(location=lat_lon)
                              fg = folium.FeatureGroup(name='My Location')
                              fg.add_child(folium.Marker(location=lat_lon, icon=icon, popup='<b>'+n2+'</b>'))
                              map1.add_child(fg)
                              map1.save('Map.html')
                              webbrowser.open_new('Map.html')

                        
                         global note_label, listbox_notes
                         f = pandas.read_csv('try3.csv')
                         note_label.grid(row=1, column=0, columnspan=2)
                         b_show.grid(row=1,column=2)
                         b_show.configure(command=show_location)
                         sel_note = listbox_notes.curselection()[0]
                         c = listbox_notes.get(sel_note)
                         
                         
                         f1 = f.loc[f['notes']==str(c),['street','zip','city','country','notes']]
                         f2 = f1.values.tolist()
                         
                         a = str(f2[0][0])+', '+str(f2[0][1])
                         b = str(f2[0][2])
                         c = str(f2[0][3])
                         d = str(f2[0][4])
                         if str(f2[0][0]) =='nan':
                              e = "City: "+b+"\nCountry: "+c+"\nNotes: "+d
                              note_label.configure(text=e)
                         else:
                              e = "Address: "+a+"\nCity: "+b+"\nCountry: "+c+"\nNotes: "+d
                              note_label.configure(text=e)

                        
                    global listbox_notes, listbox_cities
                    f = pandas.read_csv('try3.csv')
                    listbox_notes.delete(0,'end')
                     
                    b_show.grid_forget()
                    note_label.grid_forget()
                     

                    sel_city = listbox_cities.curselection()
                    if len(sel_city) > 0:
                         sel_city = int(listbox_cities.curselection()[0])
                         selection = listbox_cities.get(sel_city)
                         active = [listbox_cities.get(int(i)) for i in listbox_cities.curselection()]
                         selection = listbox_cities.get(sel_city)
                         sel_notes = f.loc[(f['category']== 'vacation') & (f['city']==str(selection))]
                         list_sel_notes = list(sel_notes['notes'])
                         unique_notes_vacation = []
                         for x in list_sel_notes:
                              unique_notes_vacation.append(x)
                         for x in unique_notes_vacation:
                              listbox_notes.insert('end', x)
                
                    listbox_notes.bind('<<ListboxSelect>>', info_label)
                
               global listbox_countries, unique_countries_vacation
               global listbox_cities, country_vacation
               f = pandas.read_csv('try3.csv')
               listbox_cities.delete(0,'end')
               listbox_notes.delete(0,'end')
                 
               b_show.grid_forget()
               note_label.grid_forget()
                 

               sel_country = listbox_countries.curselection()
               if len (sel_country) > 0:
                    sel_country = int(listbox_countries.curselection()[0])
                    selection = listbox_countries.get(sel_country)
                    active = [listbox_countries.get(int(i)) for i in listbox_countries.curselection()]   
                    sel_city = f.loc[(f['category']=='vacation') & (f['country'] == str(selection))]
                    list_sel_cities = list(sel_city['city'])
                    unique_cities_vacation = []
                    for x in list_sel_cities:
                         if x not in unique_cities_vacation:
                              unique_cities_vacation.append(x)
                    for x in unique_cities_vacation:
                         listbox_cities.insert('end', x)
               listbox_cities.bind('<<ListboxSelect>>', vacation_notes)

                
          global listbox_countries, listbox_cities, listbox_notes
          f = pandas.read_csv('try3.csv')

          listbox_countries.delete(0,'end')
          listbox_cities.delete(0,'end')
          listbox_notes.delete(0,'end')

          b_show.grid_forget()
          note_label.grid_forget()

          country_vacation = f.loc[f['category'] == 'vacation']
          list_country_vacation = list(country_vacation['country'])
          unique_countries_vacation = []
          n = []
          for x in list_country_vacation:
               if x not in unique_countries_vacation:
                    unique_countries_vacation.append(x)
          for x in unique_countries_vacation:
               listbox_countries.insert('end', x)
          listbox_countries.bind('<<ListboxSelect>>', vacation_cities)

        
     def other_countries():  
          def other_cities(event):
               def other_notes(event):
                    def info_label(event):
                         def show_location():
                             
                              global listbox_notes
                              f = pandas.read_csv('try3.csv')
                             
                              sel_note = listbox_notes.curselection()[0]
                              c = listbox_notes.get(sel_note)
                              n = f.loc[f['notes'] ==str(c),['notes']]
                              n1 = n.values.tolist()
                              n2 = str(n1[0][0])
                              f3 = f.loc[f['notes'] ==str(c),['lat']]
                              f4 = f.loc[f['notes'] ==str(c),['lon']]
                              f5 = f3.values.tolist()
                              f6 = f4.values.tolist()
                              lat_lon = f5[0]+f6[0]
                             
                              icon = folium.features.CustomIcon('otherlogo.png',icon_size=(50,50))
                             
                              map1 = folium.Map(location=lat_lon)
                              fg = folium.FeatureGroup(name='My Location')
                              fg.add_child(folium.Marker(location=lat_lon, icon=icon, popup='<b>'+n2+'</b>'))
                              map1.add_child(fg)
                              map1.save('Map.html')
                              webbrowser.open_new('Map.html')

                             
                         global note_label, listbox_notes
                         f = pandas.read_csv('try3.csv')
                         note_label.grid(row=1, column=0, columnspan=2)
                         b_show.grid(row=1,column=2)
                         b_show.configure(command=show_location)
                         sel_note = listbox_notes.curselection()[0]
                         c = listbox_notes.get(sel_note)
                         
                         
                         f1 = f.loc[f['notes']==str(c),['street','zip','city','country','notes']]
                         f2 = f1.values.tolist()
                         
                         a = str(f2[0][0])+', '+str(f2[0][1])
                         b = str(f2[0][2])
                         c = str(f2[0][3])
                         d = str(f2[0][4])
                         if str(f2[0][0]) =='nan':
                              e = "City: "+b+"\nCountry: "+c+"\nNotes: "+d
                              note_label.configure(text=e)
                         else:
                              e = "Address: "+a+"\nCity: "+b+"\nCountry: "+c+"\nNotes: "+d
                              note_label.configure(text=e)

                             
                    global listbox_notes, listbox_cities
                    f = pandas.read_csv('try3.csv')
                    listbox_notes.delete(0,'end')
                     
                    b_show.grid_forget()
                    note_label.grid_forget()


                    sel_city = listbox_cities.curselection()
                    if len(sel_city) > 0:
                         sel_city = int(listbox_cities.curselection()[0])
                         selection = listbox_cities.get(sel_city)
                         active = [listbox_cities.get(int(i)) for i in listbox_cities.curselection()]
                         selection = listbox_cities.get(sel_city)
                         sel_notes = f.loc[(f['category']== 'other') & (f['city']==str(selection))]
                         list_sel_notes = list(sel_notes['notes'])
                         unique_notes_other = []
                         for x in list_sel_notes:
                              unique_notes_other.append(x)
                         for x in unique_notes_other:
                              listbox_notes.insert('end', x)

                    listbox_notes.bind('<<ListboxSelect>>', info_label)
                     
               global listbox_countries, unique_countries_other
               global listbox_cities, country_other
               f = pandas.read_csv('try3.csv')
               listbox_cities.delete(0,'end')
               listbox_notes.delete(0,'end')

               b_show.grid_forget()
               note_label.grid_forget()


               sel_country = listbox_countries.curselection()
               if len (sel_country) > 0:
                    sel_country = int(listbox_countries.curselection()[0])
                    selection = listbox_countries.get(sel_country)
                    active = [listbox_countries.get(int(i)) for i in listbox_countries.curselection()]   
                    sel_city = f.loc[(f['category']=='other') & (f['country'] == str(selection))]
                    list_sel_cities = list(sel_city['city'])
                    unique_cities_other = []
               for x in list_sel_cities:
                    if x not in unique_cities_other:
                         unique_cities_other.append(x)
               for x in unique_cities_other:
                    listbox_cities.insert('end', x)
               listbox_cities.bind('<<ListboxSelect>>', other_notes)


        
          global listbox_countries, listbox_cities, listbox_notes
          f = pandas.read_csv('try3.csv')
          listbox_countries.delete(0,'end')
          listbox_cities.delete(0,'end')
          listbox_notes.delete(0,'end')

          b_show.grid_forget()
          note_label.grid_forget()

          country_other = f.loc[f['category'] == 'other']
          list_country_other = list(country_other['country'])
          unique_countries_other = []
          n = []
          for x in list_country_other:
               if x not in unique_countries_other:
                    unique_countries_other.append(x)
          for x in unique_countries_other:
               listbox_countries.insert('end', x)    
          listbox_countries.bind('<<ListboxSelect>>', other_cities)

     
     frame_main.pack_forget()
     frame_address.pack_forget()
     frame_city.pack_forget()
     frame_country_list.pack_forget()
     frame_stat.pack_forget()
     frame_category_list.pack(expand=YES, fill=BOTH)


     f = pandas.read_csv('try3.csv')
     countries_indata = f['country']
     list_countries1 = countries_indata.tolist()
     unique_countries = []
     for x in list_countries1:
          if x not in unique_countries:
               unique_countries.append(x)
               
     l_info1.grid(row=0,column=0,columnspan=4)
     nr_of_countries = len(unique_countries)
     l_info1.configure(text="You have visited "+str(nr_of_countries)+" countries!")


     frame1.grid(row=1, column=0, padx=10, sticky=N)
     frame2.grid(row=1, column=1, padx=10, sticky=N)


     b_living.grid(row=0, column=0, pady=10, padx=10)
     b_working.grid(row=1, column=0, pady=10, padx=10)
     b_vacation.grid(row=2, column=0, pady=10, padx=10)
     b_other.grid(row=3, column=0, pady=10, padx=10)

     b_living.configure(command=living_countries)
     b_working.configure(command=working_countries)
     b_vacation.configure(command=vacation_countries)
     b_other.configure(command=other_countries)

     listbox_countries.grid(row=0, column=0)
     listbox_cities.grid(row=0, column=1)
     listbox_notes.grid(row=0, column=2)

            
def add_city():
     frame_category_list.pack_forget()
     frame_main.pack_forget()
     frame_address.pack_forget()
     frame_country_list.pack_forget()
     frame_stat.pack_forget()
    
     def save_city():
        
          new_city = e_city.get()
          new_country = e_country.get()
          new_notes = e_notes.get()

          if new_city == "":
               messagebox.showinfo("Missing Info", "You are missing city name")
          elif new_country == "":
               messagebox.showinfo("Missing Info", "You are missing country name")
          elif new_notes == "":
               messagebox.showinfo("Missing Info", "You are missing notes")
          else:
               try:
                    if var.get() == 1:
                         x = str('living')
                         geolocator = Nominatim(user_agent="app")
                         location = geolocator.geocode(new_city+","+new_country)
                         new_lat = location.latitude
                         new_lon = location.longitude
                         add_location = open("try3.csv","a")
                         add_location.write(x +','+""+","+""+","+new_city.capitalize()+","+new_country.capitalize()+","+new_notes+","+str(new_lat)+","+str(new_lon)+"\n")
                         add_location.close()
                    elif var.get() == 2:
                         x = str('work')
                         geolocator = Nominatim(user_agent="app")
                         location = geolocator.geocode(new_city+","+new_country)
                         new_lat = location.latitude
                         new_lon = location.longitude
                         add_location = open("try3.csv","a")
                         add_location.write(x +','+""+","+""+","+new_city.capitalize()+","+new_country.capitalize()+","+new_notes+","+str(new_lat)+","+str(new_lon)+"\n")
                         add_location.close()
                    elif var.get() == 3:
                         x = str('vacation')
                         geolocator = Nominatim(user_agent="app")
                         location = geolocator.geocode(new_city+","+new_country)
                         new_lat = location.latitude
                         new_lon = location.longitude
                         add_location = open("try3.csv","a")
                         add_location.write(x +','+""+","+""+","+new_city.capitalize()+","+new_country.capitalize()+","+new_notes+","+str(new_lat)+","+str(new_lon)+"\n")
                         add_location.close()
                    else:
                         x = str('other')
                         geolocator = Nominatim(user_agent="app")
                         location = geolocator.geocode(new_city+","+new_country)
                         new_lat = location.latitude
                         new_lon = location.longitude
                         add_location = open("try3.csv","a")
                         add_location.write(x +','+""+","+""+","+new_city.capitalize()+","+new_country.capitalize()+","+new_notes+","+str(new_lat)+","+str(new_lon)+"\n")
                         add_location.close() 
                         
               except AttributeError:
                    messagebox.showinfo("Wrong Address", "Something wrong with your address,\nI cannot recognize it!")
               except UnicodeEncodeError:
                    messagebox.showinfo("Unrecognized Characters", "Please use locations only in English language.")
               else:

                    e_city.delete(0,'end')
                    e_country.delete(0,'end')
                    e_notes.delete(0,'end')

    
     frame_city.pack(expand=YES, fill=BOTH)


     l_main = Label(frame_city, text="ADD NEW CITY", font="Times 26", background="#e1d1e6", pady=30).grid(row=0, column=1, columnspan=3)
     l_city = Label(frame_city, text="City",font="Times 20", background="#e1d1e6", pady=8, padx=8).grid(row=2,column=0, sticky=E)
     l_country = Label(frame_city, text="Country",font="Times 20", background="#e1d1e6", pady=8, padx=8).grid(row=3,column=0, sticky=E)
     l_notes = Label(frame_city, text="Notes",font="Times 20", background="#e1d1e6", pady=8, padx=8).grid(row=4,column=0, sticky=E)

     city_string = StringVar()
     country_string = StringVar()
     notes_string = StringVar()

     e_city = Entry(frame_city, borderwidth= 2, font="Times 20", textvariable=city_string)
     e_country = Entry(frame_city, borderwidth= 2, font="Times 20", textvariable=country_string)
     e_notes = Entry(frame_city, borderwidth= 2, font="Times 20", textvariable=notes_string)

     e_city.grid(row=2, column=1, sticky=W)
     e_country.grid(row=3, column=1, sticky=W)
     e_notes.grid(row=4, column=1, sticky=W)

     b_add = Button(frame_city, text="Add location", bg="#bd93c9",
                   font="Times 16", bd=4, padx=20, activebackground="#f3d68d", command=save_city)
     b_add.grid(row=5,column=1)


     var = IntVar()

     c_living = Radiobutton(frame_city, text="Living", font="Times 15", background="#e1d1e6", padx=8, variable=var, value = 1)
     c_work = Radiobutton(frame_city, text="Business\Work", font="Times 15", background="#e1d1e6", padx=8, variable=var, value = 2)
     c_vacation = Radiobutton(frame_city, text="Vacation", font="Times 15", background="#e1d1e6", padx=8, variable=var, value = 3)
     c_other = Radiobutton(frame_city, text="Other",font="Times 15", background="#e1d1e6",padx=8, variable=var, value = 4)

     c_living.grid(column=2, row=2, sticky=W)
     c_work.grid(column=2, row=3, sticky=W)
     c_vacation.grid(column=2, row=4, sticky=W)
     c_other.grid(column=2, row=5, sticky=W)
    
def add_address():
     frame_category_list.pack_forget()
     frame_main.pack_forget()
     frame_city.pack_forget()
     frame_country_list.pack_forget()
     frame_stat.pack_forget()
    
     def save_address():
        
          new_street = e_street.get()
          new_zip = e_zip.get()
          new_city = e_city.get()
          new_country = e_country.get()
          new_notes = e_notes.get()

            
          if new_street == "":
               messagebox.showinfo("Missing Info", "You are missing street name")
          elif new_zip == "":
               messagebox.showinfo("Missing Info", "You are missing Zip Code")
          elif new_city == "":
               messagebox.showinfo("Missing Info", "You are missing City or Region")
          elif new_notes == "":
               messagebox.showinfo("Missing Info", "You are missing Description of place")
                
          else:
               try:
                    if var.get() == 1:
                         x = str('living')
                         geolocator = Nominatim(user_agent="app")
                         location = geolocator.geocode(new_street+","+new_zip+","+new_city)
                         new_lat = location.latitude
                         new_lon = location.longitude
                         add_location = open("try3.csv","a")
                         add_location.write(x +','+new_street.capitalize()+","+new_zip+","+new_city.capitalize()+","+new_country.capitalize()+","+new_notes+","+str(new_lat)+","+str(new_lon)+"\n")
                         add_location.close()
                    elif var.get() == 2:
                         x = str('work')
                         geolocator = Nominatim(user_agent="app")
                         location = geolocator.geocode(new_street+","+new_zip+","+new_city)
                         new_lat = location.latitude
                         new_lon = location.longitude
                         add_location = open("try3.csv","a")
                         add_location.write(x +','+new_street.capitalize()+","+new_zip+","+new_city.capitalize()+","+new_country.capitalize()+","+new_notes+","+str(new_lat)+","+str(new_lon)+"\n")
                         add_location.close()
                    elif var.get() == 3:
                         x = str('vacation')
                         geolocator = Nominatim(user_agent="app")
                         location = geolocator.geocode(new_street+","+new_zip+","+new_city)
                         new_lat = location.latitude
                         new_lon = location.longitude
                         add_location = open("try3.csv","a")
                         add_location.write(x +','+new_street.capitalize()+","+new_zip+","+new_city.capitalize()+","+new_country.capitalize()+","+new_notes+","+str(new_lat)+","+str(new_lon)+"\n")
                         add_location.close()
                    else:
                         x = str('other')
                         geolocator = Nominatim(user_agent="app")
                         location = geolocator.geocode(new_street+","+new_zip+","+new_city)
                         new_lat = location.latitude
                         new_lon = location.longitude
                         add_location = open("try3.csv","a")
                         add_location.write(x +','+new_street.capitalize()+","+new_zip+","+new_city.capitalize()+","+new_country.capitalize()+","+new_notes+","+str(new_lat)+","+str(new_lon)+"\n")
                         add_location.close()
                
               except AttributeError:
                    messagebox.showinfo("Wrong Address", "Something wrong with your address,\nI cannot recognize it!")
               except UnicodeEncodeError:
                    messagebox.showinfo("Unrecognized Characters", "Please use locations only in English language.")
               else:
                    e_street.delete(0,'end')
                    e_zip.delete(0,'end')
                    e_city.delete(0,'end')
                    e_country.delete(0,'end')
                    e_notes.delete(0,'end')

        
        
     frame_address.pack(expand=YES, fill=BOTH)
     l_main = Label(frame_address, text="ADD NEW LOCATION", font="Times 26", background="#e1d1e6", pady=30).grid(row=0, column=1, columnspan=3)

     l_street = Label(frame_address, text="Street", font="Times 20", background="#e1d1e6", pady=8, padx=8).grid(row=1,column=0, sticky=E)
     l_zip = Label(frame_address, text="Zip Code", font="Times 20", background="#e1d1e6", pady=8, padx=8).grid(row=2,column=0, sticky=E)
     l_city = Label(frame_address, text="City", font="Times 20", background="#e1d1e6", pady=8, padx=8).grid(row=3,column=0, sticky=E)
     l_country = Label(frame_address, text="Country", font="Times 20", background="#e1d1e6", pady=8, padx=8).grid(row=4,column=0, sticky=E)
     l_notes = Label(frame_address, text="Notes", font="Times 20", background="#e1d1e6", pady=8, padx=8).grid(row=5,column=0, sticky=E)

     street_string = StringVar()
     zip_string = StringVar()
     city_string = StringVar()
     country_string = StringVar()
     notes_string = StringVar()

     e_street = Entry(frame_address, borderwidth= 1, font="Times 20",textvariable=street_string)
     e_zip = Entry(frame_address, borderwidth= 1, font="Times 20",textvariable=zip_string)
     e_city = Entry(frame_address, borderwidth= 1, font="Times 20",textvariable=city_string)
     e_country = Entry(frame_address, borderwidth= 1, font="Times 20",textvariable=country_string)
     e_notes = Entry(frame_address, borderwidth= 1, font="Times 20",textvariable=notes_string)

     b_add = Button(frame_address, text="Add location", bg="#bd93c9",
                       font="Times 16", bd=4, padx=20, activebackground="#f3d68d", command=save_address).grid(row=6,column=1)


     e_street.grid(row=1, column=1, sticky=W)
     e_zip.grid(row=2, column=1, sticky=W)
     e_city.grid(row=3, column=1, sticky=W)
     e_country.grid(row=4, column=1, sticky=W)
     e_notes.grid(row=5, column=1, sticky=W)

     var = IntVar()

     c_living = Radiobutton(frame_address, text="Living", font="Times 15", background="#e1d1e6", padx=8, variable=var, value = 1)
     c_work = Radiobutton(frame_address, text="Business\Work", font="Times 15",background="#e1d1e6", padx=8, variable=var, value = 2)
     c_vacation = Radiobutton(frame_address, text="Vacation", font="Times 15",background="#e1d1e6", padx=8, variable=var, value = 3)
     c_other = Radiobutton(frame_address, text="Other", font="Times 15",background="#e1d1e6", padx=8, variable=var, value = 4)

     c_living.grid(column=3, row=2, sticky=W)
     c_work.grid(column=3, row=3, sticky=W)
     c_vacation.grid(column=3, row=4, sticky=W)
     c_other.grid(column=3, row=5, sticky=W)



# LIST OF FRAMES    
frame_main = Frame(window)    
frame_address = Frame(window, bg="#e1d1e6")

frame_city = Frame(window, bg="#e1d1e6")
frame_category_list = Frame(window, bg="#e1d1e6")
frame_country_list = Frame(window, bg="#e1d1e6")

frame1 = Frame(frame_category_list, bg="#e1d1e6")
frame2 = Frame(frame_category_list, bg="#e1d1e6")


frame11 = Frame(frame_country_list, bg="#e1d1e6")


#LIST OF BUTTONS, LISTBOXES AND LABELS IN 'BY CATEGORY'
b_living = Button(frame1, text='Living', bg="#bd93c9",font="Times 16", bd=4, padx=30, activebackground="#f3d68d")
b_working = Button(frame1, text='Working', bg="#bd93c9",font="Times 16", bd=4, padx=20, activebackground="#f3d68d")
b_vacation = Button(frame1, text='Vacation', bg="#bd93c9",font="Times 16", bd=4, padx=20, activebackground="#f3d68d")
b_other = Button(frame1, text='Other', bg="#bd93c9",font="Times 16", bd=4, padx=32, activebackground="#f3d68d")

listbox_countries = Listbox(frame2,font="Times 16",selectbackground="#bd93c9",width=12,exportselection=False)
listbox_cities = Listbox(frame2,font="Times 16",selectbackground="#bd93c9",width=15,exportselection=False)
listbox_notes = Listbox(frame2,font="Times 16",selectbackground="#bd93c9",width=15,exportselection=False)

note_label = Label(frame2,font="Times 12", anchor=W, bg="#e1d1e6")
b_show = Button(frame2, text="Show Location",font="Times 12", bg="#bd93c9")


# LIST OF BUTTONS, LISTBOXES AND LABELS IN 'BY COUNTRY'
l_info = Label(frame_country_list, font="Times 22", background="#e1d1e6", pady=25)
l_info1 = Label(frame_category_list, font="Times 22", background="#e1d1e6", pady=25)

list_countries = Listbox(frame11,font="Times 16",selectbackground="#bd93c9",width=12, exportselection=False)
list_cities = Listbox(frame11,font="Times 16",selectbackground="#bd93c9",width=25, exportselection=False)
list_notes = Listbox(frame11,font="Times 16",selectbackground="#bd93c9",width=15, exportselection=False)

b_country = Button(frame11,font="Times 12", bg="#bd93c9")
b_show_location = Button(frame11, text='Show Location',font="Times 12", bg="#bd93c9")
note_label2 = Label(frame11, font="Times 12", background="#e1d1e6", pady=25)

#LIST OF FRAMES, LABELS IN DEF 'STATISTICS'

frame_stat = Frame(window, bg="#e1d1e6")

stat_label = Label(frame_stat,font="Times 16", background="#e1d1e6", borderwidth=5, relief='raised', pady=10, padx=10, justify=LEFT)
by_category = Label(frame_stat,font="Times 16", background="#e1d1e6", borderwidth=5, relief='raised', pady=10, padx=10, justify=LEFT)
img = PhotoImage(file='globe.png')
globe = Label(frame_stat, image=img, borderwidth=0, relief='flat')

# LIST OF MENUS AND SUBMENUS
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Add new address", background="#e1d1e6", activebackground="#bd93c9",font="Times 14",  command=add_address)
filemenu.add_command(label="Add new city", background="#e1d1e6", activebackground="#bd93c9",font="Times 14", command=add_city)
submenu = Menu(filemenu, tearoff = 0)
submenu.add_command(label="By category", background="#e1d1e6", activebackground="#bd93c9",font="Times 14", command = category)
submenu.add_command(label = "By country", background="#e1d1e6", activebackground="#bd93c9",font="Times 14", command = by_country)
filemenu.add_cascade(label="See List of locations", background="#e1d1e6", activebackground="#bd93c9",font="Times 14", menu=submenu)

filemenu.add_command(label="See map", background="#e1d1e6", activebackground="#bd93c9",font="Times 14", command=see_all_locations)
filemenu.add_separator()
filemenu.add_command(label="Statistics", background="#e1d1e6", activebackground="#bd93c9",font="Times 14", command=statistics)
filemenu.add_command(label="Delete data", background="#e1d1e6", activebackground="#bd93c9",font="Times 14", command=delete)
filemenu.add_separator()
filemenu.add_command(label="Exit", background="#e1d1e6", activebackground="#bd93c9",font="Times 14", command=window.destroy)

menubar.add_cascade(label="Options", background="#e1d1e6", activebackground="#bd93c9",font="Times 14", menu=filemenu)

window.config(menu=menubar)

#MAIN OPENING PICTURE
canvas = Canvas(frame_main, width=706, height=482)
canvas.grid(column=0, row=0)


photo = PhotoImage(file="welcome.gif")
canvas.create_image(0,0, image=photo, anchor = 'nw')

#LOGO PICTURES FOR CATEGORY LIST
logo_home = PhotoImage(file='homelogo.png').subsample(5,5)
logo_work = PhotoImage(file='logowork.png').subsample(5,5)
logo_vacation = PhotoImage(file='vacationlogo.png').subsample(5,5)
logo_other = PhotoImage(file='otherlogo.png').subsample(5,5)


frame_main.pack()

window.mainloop()
