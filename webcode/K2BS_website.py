from glob import glob
from webtools import *
from datetime import datetime

import pandas as pd
import numpy as np

def Fill_subsection_links(Webpage, Location, Savename):
    types = Savename.split('_')
    
    if len(types) > 1:
        Webpage.substituteplaceholder('PLACEHOLDER_LENGTH',
                                  addlink2string(types[0], Location[0] + types[0] + '.html'))
        if len(types) > 3:
            Webpage.substituteplaceholder('PLACEHOLDER_BRIGHTNESS',
                                      addlink2string(types[1], Location[1] + types[0] + '_' + types[1] + '.html'))
            Webpage.substituteplaceholder('PLACEHOLDER_TYPE_ONE',
                                      addlink2string(types[2], Location[2] + types[0] + '_' + types[1] + '_' + types[2] + '.html'))
            Webpage.substituteplaceholder('PLACEHOLDER_TYPE_TWO',
                                      addlink2string(types[3].split('.')[0], Location[3] + Savename))
        else:
            if len(types) == 3:
                Webpage.substituteplaceholder('PLACEHOLDER_BRIGHTNESS',
                                      addlink2string(types[1], Location[1] + types[0] + '_' + types[1] + '.html'))
                Webpage.substituteplaceholder('PLACEHOLDER_TYPE_ONE',
                                          addlink2string(types[2].split('.')[0], Location[2] + Savename))

                Webpage.substituteplaceholder('PLACEHOLDER_TYPE_TWO','')
            else:
                Webpage.substituteplaceholder('PLACEHOLDER_BRIGHTNESS',
                                      addlink2string(types[1].split('.')[0], Location[1] + types[0] + '_' + types[1]))
                Webpage.substituteplaceholder('PLACEHOLDER_TYPE_ONE','')
                Webpage.substituteplaceholder('PLACEHOLDER_TYPE_TWO','')
    else:
        if len(types) == 1:
            Webpage.substituteplaceholder('PLACEHOLDER_LENGTH',
                                      addlink2string(types[0].split('.')[0], Location[0] + types[0]))
            Webpage.substituteplaceholder('PLACEHOLDER_BRIGHTNESS','')
            Webpage.substituteplaceholder('PLACEHOLDER_TYPE_ONE','')
            Webpage.substituteplaceholder('PLACEHOLDER_TYPE_TWO','')
        else:
            Webpage.substituteplaceholder('PLACEHOLDER_LENGTH','')
            Webpage.substituteplaceholder('PLACEHOLDER_BRIGHTNESS','')
            Webpage.substituteplaceholder('PLACEHOLDER_TYPE_ONE','')
            Webpage.substituteplaceholder('PLACEHOLDER_TYPE_TWO','')
        
    return Webpage

def Reduce_string(string):
    """
    Reduces the size of a html event string by one component.
    """
    temp = string.split('_')
    temp2=''
    for i in range(len(temp)-1):
        if i != (len(temp)-2):
            temp2 += temp[i] + '_'
        else:
            temp2 += temp[i] + '.html'
    return temp2

def Make_individual_event_page(Directory,Location):
    direc = glob(Directory + 'Figures/**/**/**/')
    direc = [ x for x in direc if "Prob" not in x ]
    direc = [ x for x in direc if "Near" not in x ]
    direc = [ x for x in direc if "In" not in x ]
    temp = glob(Directory + 'Figures/**/**/**/**/')
    if len(direc) == 1:
        direc = [direc]
    if len(temp) == 1:
        temp = [temp]
    direc.append(temp)
    direc = [item for sublist in direc for item in sublist]
    temp = [e for e in direc if 'Frame' not in e]
    direc = temp
    

    for path in direc:
        files = glob(path+'/*')
        events = []
        for file in files:
            if '-' in file:
                events.append(file.split('-')[-1].split('.')[0])
            else:
                events.append(file.split('/')[-1].split('.')[0])
        events = list(set(events))

        for event in events:
            EPIC = event.split('ktwo')[-1].split('_')[0]
            Number = event.split('_')[-1]
            cols2show = ['Campaign', 'EPIC', 'Event number', 'Host type', 'Start', 'Duration', 'Counts', 'Size','RA','DEC','Host', 'Channel', 'Module', 'Output', 'Zoofig']

            data = pd.read_csv(Directory + '/Events.csv')
            data = data.values
            
            row = np.where((int(EPIC) == data[:,1]) & (int(Number) == data[:,2]))

            defaultwebpagename = './default/defaultpage_K2BS_individual_event.html'
            webpage = webpageclass()
            webpage.loaddefaultpage(defaultwebpagename)
            webpage.substituteplaceholder('PLACEHOLDER_TITLE_PLACEHOLDER','K2:BS ' + event.split('ktwo')[-1])
            webpage.substituteplaceholder('PLACEHOLDER_CAMPAIGN','c'+path.split('c')[1].split('/')[0])

            webpage.substituteplaceholder('PLACEHOLDER_BACKTOMAINLINK_PLACEHOLDER',
                                          addlink2string('K2:BS Homepage',Location[0].split('length')[0]+'K2BSHomepage.html'))

            
            infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')
            
            infotable.startrow()
            infotable.addcol('Event info',colspan=1,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
            infotable.endrow()
            infotable.startrow()
            for col in cols2show:
                infotable.addcol(col,textalign='center',width=None,bold=1, color = 'white', bgcolor = 0.75)
            infotable.endrow()
            infotable.startrow()
            for col in data[row,:][0][0]:
                infotable.addcol(str(col),textalign='center')
            infotable.endrow()
            webpage.substituteplaceholder('PLACEHOLDER_INFOTABLE_PLACEHOLDER',infotable.gettable(sortable=True))
            
            infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='400px')
            cols2show = ['Figure','Video']
            infotable.startrow()
            infotable.addcol(cols2show[0])
            infotable.addcol(cols2show[1])
            infotable.endrow()
            
            event_pdf = glob(path+'*'+event+'*.pdf')
            event_TN = glob(path+'*'+event+'*.png')
            event_vid = glob(path+'*'+event+'*.mp4')

            filler = './default/anger.jpg'
            if len(event_pdf) == 0:
                event_pdf = [filler]
            if len(event_TN) == 0:
                event_TN = [filler]
            if len(event_vid) == 0:
                event_vid = [filler]
            
                
            infotable.startrow()
            s = '<embed src="' + event_pdf[0] + '" width="500" height="400">'
            #s = imagestring4web(event_pdf[0],width=None,height='400')
            infotable.addcol(s)   
            s = vidstring4web(event_vid[0],width='500',height='400')
            infotable.addcol(s)
            infotable.endrow()

            webpage.substituteplaceholder('PLACEHOLDER_IMAGETABLE_PLACEHOLDER',infotable.gettable(sortable=True))    
            
            types = path.split('Figures')[-1].split('/')
            types = types[1:-1]
            savename = ''
            for i in types:
                if i not in types[-1]:
                    savename += i + '_'
                else:
                    savename += i + '.html'
            webpage = Fill_subsection_links(webpage, Location, savename)
            type3 = Location[4] + data[row,0] + '-' + savename
            webpage.substituteplaceholder('PLACEHOLDER_TYPE_CAMPAIGN',
                                          addlink2string(data[row,0][0][0],type3[0][0]))
            
            today = datetime.now()
            update_date = str(today.date())
            webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
            webpage.savepage(Location[5] + event.split('ktwo')[-1] + '.html')


def Make_candidate_webpage(Directory, Location):
    """
    Gather all like events in a campaign and make a webpage.
    """
    
    direc = glob(Directory + 'Figures/**/**/**/')
    direc = [ x for x in direc if "Prob" not in x ]
    direc = [ x for x in direc if "Near" not in x ]
    direc = [ x for x in direc if "In" not in x ]
    temp = glob(Directory + 'Figures/**/**/**/**/')
    if len(direc) == 1:
        direc = [direc]
    if len(temp) == 1:
        temp = [temp]
    direc.append(temp)
    direc = [item for sublist in direc for item in sublist]
    temp = [e for e in direc if 'Frame' not in e]
    direc = temp


    for path in direc:

        cols2show = ['Figure', 'Video', 'EPIC ID', 'Event #', 'Channel', 'Module']

        defaultwebpagename = './default/defaultpage_K2BS_events.html'
        webpage = webpageclass()
        webpage.loaddefaultpage(defaultwebpagename)
        webpage.substituteplaceholder('PLACEHOLDER_TITLE_PLACEHOLDER','K2:BS')
        webpage.substituteplaceholder('PLACEHOLDER_CAMPAIGN','c'+path.split('c')[1].split('/')[0])
                                      
        webpage.substituteplaceholder('PLACEHOLDER_BACKTOMAINLINK_PLACEHOLDER',
                                      addlink2string('K2:BS Homepage',Location[0].split('length')[0]+'K2BSHomepage.html'))


        infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')

        infotable.startrow()
        infotable.addcol('Candidates',colspan=1,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
        infotable.endrow()
        infotable.startrow()
        for col in cols2show:
            infotable.addcol(col,textalign='center',width=None,bold=1, color = 'white', bgcolor = 0.75)
        infotable.endrow()

        files = glob(path+'/*')
        events = []
        for file in files:
            if '-' in file:
                events.append(file.split('-')[-1].split('.')[0])
            else:
                events.append(file.split('/')[-1].split('.')[0])
        events = list(set(events))
        # 
        data = pd.read_csv(Directory + '/Events.csv')
        data = data.values

        for event in events:
            event_pdf = glob(path+'*'+event+'*.pdf')
            event_TN = glob(path+'*'+event+'*.png')
            event_vid = glob(path+'*'+event+'*.mp4')

            filler = './default/anger.jpg'
            if len(event_pdf) == 0:
                event_pdf = [filler]
            if len(event_TN) == 0:
                event_TN = [filler]
            if len(event_vid) == 0:
                event_vid = [filler]
            

            row = np.where(data[:,1] == int(event.split('_')[0].split('o')[1]))[0]
            if len(row) > 1:
                row = row[0]
            channel = data[row,11]
            if type(channel) == np.ndarray:
                channel = channel[0]            
            module = data[row,12]
            if type(module) == np.ndarray:
                module = module[0]
                
            infotable.startrow()
            s = addlink2string(imagestring4web(event_TN[0],width=None,height='150'),event_pdf[0])
            infotable.addcol(s)   
            s = addlink2string(vidstring4web(event_vid[0],width=None,height='150'),event_vid[0])
            infotable.addcol(s)
            temp = filler
            for eve in glob(Location[5]+'*'):
                if event.split('ktwo')[-1] == eve.split('/')[-1].split('.html')[0]:
                    temp = eve
            
            infotable.addcol(event.split('ktwo')[1].split('_')[0])
            infotable.addcol(addlink2string(event.split('_')[1],temp))
            infotable.addcol(str(channel))
            infotable.addcol(str(module))

            infotable.endrow()

        webpage.substituteplaceholder('PLACEHOLDER_IMAGETABLE_PLACEHOLDER',infotable.gettable(sortable=True))


        today = datetime.now()
        update_date = str(today.date())
        webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)

        # now save it.
        c_split = path.split('c')[1]

        if len(c_split.split('/')) > 6: # magic number to seperate single type objects from nested type objects
            savename = c_split.split('/')[2] + '_' +c_split.split('/')[3] + '_' +c_split.split('/')[4] + '_' +c_split.split('/')[5] +'.html'
        else:
            savename = c_split.split('/')[2] + '_' +c_split.split('/')[3] + '_' +c_split.split('/')[4] +'.html'
        webpage = Fill_subsection_links(webpage,Location,savename)
        
        savename = 'c'+path.split('c')[1].split('/')[0]+ '-' + savename
        
        webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
        webpage.savepage(Location[4] + savename)
        
def Make_category_pages(Location):
    body_text = ["Events are 'probably' associated with a ",
                 "Events are 'near' a ",
                 "Events are 'in' a "]
    body_cat = ['Prob','Near','In']

    files = glob(Location[4] + '*.html')

    group = []
    for file in files:
        group.append(file.split('-')[1])
    sorte = list(set(group))
    stage3 = []
    for name in sorte:
        if len(name.split('_')) == 4: 
            defaultwebpagename = './default/defaultpage_K2BS_category.html'
            webpage = webpageclass()
            webpage.loaddefaultpage(defaultwebpagename)
            webpage.substituteplaceholder('PLACEHOLDER_TITLE_PLACEHOLDER','K2:BS')
            webpage.substituteplaceholder('PLACEHOLDER_TYPE_PLACEHOLDER', name.split('.')[0].split('_')[-1])

            webpage.substituteplaceholder('PLACEHOLDER_BACKTOMAINLINK_PLACEHOLDER',
                                          addlink2string('K2:BS Homepage','K2BSHomepage.html'))

            infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')

            infotable.startrow()
            infotable.addcol('Campaigns',colspan=1,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
            infotable.endrow()
            for link in files:
                if name in link:
                    infotable.startrow()
                    infotable.addcol(addlink2string(link.split('-')[0].split('/')[-1],link))   
                    infotable.endrow()

            webpage.substituteplaceholder('PLACEHOLDER_IMAGETABLE_PLACEHOLDER',infotable.gettable(sortable=True))
            temp = 0
            for i in range(len(body_cat)):
                  if name.split('_')[2] == body_cat[i]:
                        temp = i
            body = body_text[temp] + name.split('_')[-1].split('.')[0]
            webpage.substituteplaceholder('PLACEHOLDER_BODY',body)
            webpage = Fill_subsection_links(webpage,Location,Reduce_string(name))
            today = datetime.now()
            update_date = str(today.date())
            webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
            webpage.savepage(Location[3] + name)



    body_text = ["Events are 'probably' associated with a mask object",
                 "Events are 'near' a mask object",
                 "Events are 'in' a mask object"]

    body_cat = ['Prob','Near','In']

    files = glob(Location[3] + '*.html')
    group = []
    for file in files:
        temp = file.split('/')[-1]
        group.append(Reduce_string(temp))
    sorte = list(set(group))

    for name in sorte:
        defaultwebpagename = './default/defaultpage_K2BS_category.html'
        webpage = webpageclass()
        webpage.loaddefaultpage(defaultwebpagename)
        webpage.substituteplaceholder('PLACEHOLDER_TITLE_PLACEHOLDER','K2:BS')
        webpage.substituteplaceholder('PLACEHOLDER_TYPE_PLACEHOLDER', name.split('_')[-1].split('.')[0])
        webpage.substituteplaceholder('PLACEHOLDER_BACKTOMAINLINK_PLACEHOLDER',
                                          addlink2string('K2:BS Homepage',Location[0].split('length')[0]+'K2BSHomepage.html'))
        infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')

        infotable.startrow()
        infotable.addcol('Object types',colspan=1,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
        infotable.endrow()

        for link in files:
            if name.split('.')[0] in link:
                infotable.startrow()
                infotable.addcol(addlink2string(link.split('_')[-1].split('.')[0],link))
                infotable.endrow()

        webpage.substituteplaceholder('PLACEHOLDER_IMAGETABLE_PLACEHOLDER',infotable.gettable(sortable=True))
        temp = 0
        for i in range(len(body_cat)):
              if name.split('_')[2].split('.')[0] == body_cat[i]:
                    temp = i
        webpage.substituteplaceholder('PLACEHOLDER_BODY',body_text[temp])
        webpage = Fill_subsection_links(webpage,Location,Reduce_string(name))
        today = datetime.now()
        update_date = str(today.date())
        webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
        webpage.savepage(Location[2] + name)


    # Now for the non mask stuff
    body_text = "Events are associated with a "

    files = glob(Location[4] + '*.html')

    group = []
    for file in files:
        group.append(file.split('-')[1])
    sorte = list(set(group))
    stage3 = []
    for name in sorte:
        if len(name.split('_')) == 3: 
            defaultwebpagename = './default/defaultpage_K2BS_category.html'
            webpage = webpageclass()
            webpage.loaddefaultpage(defaultwebpagename)
            webpage.substituteplaceholder('PLACEHOLDER_TITLE_PLACEHOLDER','K2:BS')
            webpage.substituteplaceholder('PLACEHOLDER_TYPE_PLACEHOLDER', name.split('_')[-1].split('.')[0])
            webpage.substituteplaceholder('PLACEHOLDER_BACKTOMAINLINK_PLACEHOLDER',
                                              addlink2string('K2:BS Homepage',Location[0].split('length')[0]+'K2BSHomepage.html'))
            infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')

            infotable.startrow()
            infotable.addcol('Campaigns',colspan=1,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
            infotable.endrow()
            for link in files:
                if name in link:
                    infotable.startrow()
                    infotable.addcol(addlink2string(link.split('-')[0].split('/')[-1],link))   
                    infotable.endrow()

            webpage.substituteplaceholder('PLACEHOLDER_IMAGETABLE_PLACEHOLDER',infotable.gettable(sortable=True))

            webpage.substituteplaceholder('PLACEHOLDER_BODY',body_text + name.split('_')[-1].split('.')[0])
            webpage = Fill_subsection_links(webpage,location,Reduce_string(name))
            today = datetime.now()
            update_date = str(today.date())
            webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
            webpage.savepage(Location[2] + name)
            
def Make_brightness_pages(Location):
    files = glob(Location[2] + '*.html')
    group = []
    for file in files:
        temp = file.split('/')[-1]
        group.append(Reduce_string(temp))
    sorte = list(set(group))

    for name in sorte:
        defaultwebpagename = './default/defaultpage_K2BS_category.html'
        webpage = webpageclass()
        webpage.loaddefaultpage(defaultwebpagename)
        webpage.substituteplaceholder('PLACEHOLDER_TITLE_PLACEHOLDER','K2:BS')
        webpage.substituteplaceholder('PLACEHOLDER_TYPE_PLACEHOLDER', name.split('_')[-1].split('.')[0])
        webpage.substituteplaceholder('PLACEHOLDER_BACKTOMAINLINK_PLACEHOLDER',
                                          addlink2string('K2:BS Homepage','../K2BSHomepage.html'))
        infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')

        infotable.startrow()
        infotable.addcol('Object types',colspan=1,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
        infotable.endrow()

        for link in files:
            if name.split('.')[0] in link:
                infotable.startrow()
                infotable.addcol(addlink2string(link.split('_')[-1].split('.')[0],link))
                infotable.endrow()

        webpage.substituteplaceholder('PLACEHOLDER_IMAGETABLE_PLACEHOLDER',infotable.gettable(sortable=True))
        temp = 0
        body_text = ' events.'
        webpage.substituteplaceholder('PLACEHOLDER_BODY',name.split('_')[-1].split('.')[0] + body_text)
        webpage = Fill_subsection_links(webpage,Location,Reduce_string(name))
        today = datetime.now()
        update_date = str(today.date())
        webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
        webpage.savepage(Location[1] + name)
        
def Make_length_pages(Location):
    files = glob(Location[1] + '*.html')
    group = []
    for file in files:
        temp = file.split('/')[-1]
        group.append(Reduce_string(temp))
    sorte = list(set(group))
    for name in sorte:
        defaultwebpagename = './default/defaultpage_K2BS_category.html'
        webpage = webpageclass()
        webpage.loaddefaultpage(defaultwebpagename)
        webpage.substituteplaceholder('PLACEHOLDER_TITLE_PLACEHOLDER','K2:BS')
        webpage.substituteplaceholder('PLACEHOLDER_TYPE_PLACEHOLDER', name.split('_')[-1].split('.')[0])
        webpage.substituteplaceholder('PLACEHOLDER_BACKTOMAINLINK_PLACEHOLDER',
                                          addlink2string('K2:BS Homepage',Location[0].split('length')[0]+'K2BSHomepage.html'))
        infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')

        infotable.startrow()
        infotable.addcol('Object types',colspan=1,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
        infotable.endrow()

        for link in files:
            if name.split('.')[0] in link:
                infotable.startrow()
                infotable.addcol(addlink2string(link.split('_')[-1].split('.')[0],link))
                infotable.endrow()

        webpage.substituteplaceholder('PLACEHOLDER_IMAGETABLE_PLACEHOLDER',infotable.gettable(sortable=True))
        temp = 0
        body_text = ' events.'
        webpage.substituteplaceholder('PLACEHOLDER_BODY',name.split('_')[-1].split('.')[0] + body_text)
        webpage = Fill_subsection_links(webpage,Location,Reduce_string(name))
        today = datetime.now()
        update_date = str(today.date())
        webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
        webpage.savepage(Location[0] + name)
        
def Make_homepage(Location):
    files = glob(Location[0] + '*.html')
    defaultwebpagename = './default/defaultpage_K2BS_homepage.html'
    webpage = webpageclass()
    webpage.loaddefaultpage(defaultwebpagename)
    webpage.substituteplaceholder('PLACEHOLDER_TITLE_PLACEHOLDER','K2: Background Survey')
    webpage.substituteplaceholder('PLACEHOLDER_TYPE_PLACEHOLDER', name.split('_')[-1].split('.')[0])
    infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')
    infotable.startrow()
    infotable.addcol('Event length',colspan=1,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
    infotable.endrow()

    for link in files:
        infotable.startrow()
        infotable.addcol(addlink2string(link.split('/')[-1].split('.')[0],link))
        infotable.endrow()
    webpage.substituteplaceholder('PLACEHOLDER_IMAGETABLE_PLACEHOLDER',infotable.gettable(sortable=True))        
    today = datetime.now()
    update_date = str(today.date())
    webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
    webpage.savepage('./K2BSHomepage.html')
