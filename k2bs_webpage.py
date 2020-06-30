from glob import glob
from webtools import *
from datetime import datetime

import pandas as pd
import numpy as np


def Fill_subsection_links(Webpage, Location, Savename, Save_dir,Web_dir):
	types = Savename.split('_')
	
	if len(types) > 1:
		Webpage.substituteplaceholder('PLACEHOLDER_LENGTH',
								addlink2string(types[0], Web_dir + Location[0] + types[0] + '.html'))
		if len(types) > 3:
			Webpage.substituteplaceholder('PLACEHOLDER_BRIGHTNESS',
									addlink2string(types[1], Web_dir + Location[1] + types[0] + '_' + types[1] + '.html'))
			Webpage.substituteplaceholder('PLACEHOLDER_TYPE_ONE',
									addlink2string(types[2], Web_dir + Location[2] + types[0] + '_' + types[1] + '_' + types[2] + '.html'))
			Webpage.substituteplaceholder('PLACEHOLDER_TYPE_TWO',
									addlink2string(types[3].split('.')[0], Web_dir + Location[3] + Savename))
		else:
			if len(types) == 3:
				Webpage.substituteplaceholder('PLACEHOLDER_BRIGHTNESS',
									addlink2string(types[1], Web_dir + Location[1] + types[0] + '_' + types[1] + '.html'))
				Webpage.substituteplaceholder('PLACEHOLDER_TYPE_ONE',
										addlink2string(types[2].split('.')[0], Web_dir + Location[2] + Savename))

				Webpage.substituteplaceholder('PLACEHOLDER_TYPE_TWO','')
			else:
				Webpage.substituteplaceholder('PLACEHOLDER_BRIGHTNESS',
									addlink2string(types[1].split('.')[0], Web_dir + Location[1] + types[0] + '_' + types[1]))
				Webpage.substituteplaceholder('PLACEHOLDER_TYPE_ONE','')
				Webpage.substituteplaceholder('PLACEHOLDER_TYPE_TWO','')
	else:
		if len(types) == 1:
			Webpage.substituteplaceholder('PLACEHOLDER_LENGTH',
									addlink2string(types[0].split('.')[0], Web_dir + Location[0] + types[0]))
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

def Make_individual_event_page(Directory,Location,Save_dir,Web_dir):
	direc = glob(Directory + 'Figures/**/**/**/')
	direc = [ x for x in direc if "Prob" not in x ]
	direc = [ x for x in direc if "Near" not in x ]
	direc = [ x for x in direc if "In" not in x ]
	temp = glob(Directory + 'Figures/**/**/**/**/')
	if len(direc) == 1:
		direc = [direc]
	if len(temp) == 1:
		temp = [temp]
	direc.extend(temp)
	
	#direc = [item for sublist in direc for item in sublist] # wut
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
			cols2show = ['Campaign', 'EPIC', 'Event number', 'Host type', 'Start', 'Duration', 'Counts', 'Size','RA','DEC','Host', 'Channel', 'Module', 'Output', 'Rank bright',
						  'Rank duration', 'Rank mask', 'Rank host', 'Rank total', 'Zoofig']

			data = pd.read_csv(Directory + '/Events.csv')
			data = data.values
			
			row = np.where((int(EPIC) == data[:,1]) & (int(Number) == data[:,2]))

			defaultwebpagename = './default/defaultpage_K2BS_individual_event.html'
			webpage = webpageclass()
			webpage.loaddefaultpage(defaultwebpagename)
			webpage.substituteplaceholder('PLACEHOLDER_TITLE_PLACEHOLDER','K2:BS ' + event.split('ktwo')[-1])
			webpage.substituteplaceholder('PLACEHOLDER_CAMPAIGN','c'+path.split('c')[1].split('/')[0])

			webpage.substituteplaceholder('PLACEHOLDER_BACKTOMAINLINK_PLACEHOLDER',
										addlink2string('K2:BS Homepage',Web_dir + 'K2BSHomepage.html'))

			
			infotable = htmltable(20,border=1,cellspacing=0,cellpadding=2,width='200px')
			
			infotable.startrow()
			infotable.addcol('Event info',textalign='left',colspan=20,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
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

			#filler = './default/anger.jpg'
			#if len(event_pdf) == 0:
			#	event_pdf = [filler]
			#if len(event_TN) == 0:
			#	event_TN = [filler]
			#if len(event_vid) == 0:
			#	event_vid = [filler]

			event_pdf = Web_dir + 'data/' + event_pdf[0].split('data/')[-1]
			event_vid = Web_dir + 'data/' + event_vid[0].split('data/')[-1]
				
			infotable.startrow()
			s = '<embed src="' + event_pdf + '" width="500" height="400">'
			#s = imagestring4web(event_pdf[0],width=None,height='400')
			infotable.addcol(s) 
			s = vidstring4web(event_vid,width='500',height='400')
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
			webpage = Fill_subsection_links(webpage, Location, savename,Save_dir,Web_dir)
			type3 = Location[4] + data[row,0] + '-' + savename
			webpage.substituteplaceholder('PLACEHOLDER_TYPE_CAMPAIGN',
										addlink2string(data[row,0][0][0],Web_dir + type3[0][0]))
			
			today = datetime.now()
			update_date = str(today.date())
			webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
			webpage.savepage(Save_dir + Location[5] + event.split('ktwo')[-1] + '.html')


def Make_candidate_webpage(Directory, Location, Save_dir,Web_dir):
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
	direc.extend(temp)
	#direc = [item for sublist in direc for item in sublist]
	temp = [e for e in direc if 'Frame' not in e]
	direc = temp


	for path in direc:
		cols2show = ['Figure', 'Video', 'EPIC ID', 'Event #', 'Channel', 'Module']

		defaultwebpagename = './default/defaultpage_K2BS_events.html'
		webpage = webpageclass()
		webpage.loaddefaultpage(defaultwebpagename)
		webpage.substituteplaceholder('PLACEHOLDER_TITLE_PLACEHOLDER','K2:BS')
		webpage.substituteplaceholder('PLACEHOLDER_CAMPAIGN','c'+path.split('c')[-1].split('/')[0])
									
		webpage.substituteplaceholder('PLACEHOLDER_BACKTOMAINLINK_PLACEHOLDER',
									addlink2string('K2:BS Homepage',Save_dir+'K2BSHomepage.html'))


		infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')

		infotable.startrow()
		infotable.addcol('Candidates',colspan=6,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
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

			#filler = './default/anger.jpg'
			#if len(event_pdf) == 0:
			#	event_pdf = [filler]
			#if len(event_TN) == 0:
			#	event_TN = [filler]
			#if len(event_vid) == 0:
			#	event_vid = [filler]
			

			row = np.where(data[:,1] == int(event.split('_')[0].split('o')[1]))[0]
			if len(row) > 1:
				row = row[0]
			channel = data[row,11]
			if type(channel) == np.ndarray:
				channel = channel[0]			
			module = data[row,12]
			if type(module) == np.ndarray:
				module = module[0]
			
			event_TN = Web_dir + 'data/' + event_TN[0].split('data/')[-1]
			event_pdf = Web_dir + 'data/' + event_pdf[0].split('data/')[-1]
			event_vid = Web_dir + 'data/' + event_vid[0].split('data/')[-1]

			infotable.startrow()
			s = addlink2string(imagestring4web(event_TN,width=None,height='150'),event_pdf)
			infotable.addcol(s) 
			s = addlink2string(vidstring4web(event_vid,width=None,height='150'),Web_dir + event_vid)
			infotable.addcol(s)
			temp = filler
			for eve in glob(Save_dir + Location[5]+'*'):
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
		c_split = path.split('c')[-1] # This is bad code, but dunno how to fix. Change the index so that the c from c## is the cut point.

		if len(c_split.split('/')) > 6: # magic number to seperate single type objects from nested type objects
			savename = c_split.split('/')[2] + '_' +c_split.split('/')[3] + '_' +c_split.split('/')[4] + '_' +c_split.split('/')[5] +'.html'
		else:
			savename = c_split.split('/')[2] + '_' +c_split.split('/')[3] + '_' +c_split.split('/')[4] +'.html'
		webpage = Fill_subsection_links(webpage,Location,savename,Save_dir)
		
		savename = 'c'+path.split('c')[-1].split('/')[0]+ '-' + savename
		
		webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
		webpage.savepage(Save_dir + Location[4] + savename)
		
def Make_category_pages(Location,Save_dir):
    body_text = ["Events are 'probably' associated with ",
                 "Events are 'near' ",
                 "Events are 'in' "]
    body_cat = ['Prob','Near','In']

    files = glob(Save_dir + Location[4] + '*.html')

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
                                        addlink2string('K2:BS Homepage',Web_dir + 'K2BSHomepage.html'))

            infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')

            infotable.startrow()
            infotable.addcol('Campaigns',colspan=1,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
            infotable.endrow()
            for link in files:
                if name in link:
                    infotable.startrow()
                    infotable.addcol(addlink2string(link.split('-')[0].split('/')[-1],Web_dir + link)) 
                    infotable.endrow()

            webpage.substituteplaceholder('PLACEHOLDER_IMAGETABLE_PLACEHOLDER',infotable.gettable(sortable=True))
            temp = 0
            for i in range(len(body_cat)):
                if name.split('_')[2] == body_cat[i]:
                    temp = i
            body = body_text[temp] + name.split('_')[-1].split('.')[0]
            webpage.substituteplaceholder('PLACEHOLDER_BODY',body)
            webpage = Fill_subsection_links(webpage,Location,Reduce_string(name),Save_dir,Web_dir)
            today = datetime.now()
            update_date = str(today.date())
            webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
            #print(Save_dir +Location[3] + name)
            webpage.savepage(Save_dir + Location[3] + name)



    body_text = ["Events are 'probably' associated with a mask object",
                 "Events are 'near' a mask object",
                 "Events are 'in' a mask object"]

    body_cat = ['Prob','Near','In']

    files = glob(Save_dir + Location[3] + '*.html')
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
                                        addlink2string('K2:BS Homepage',Web_dir + 'K2BSHomepage.html'))
        infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')

        infotable.startrow()
        infotable.addcol('Object types',colspan=1,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
        infotable.endrow()

        for link in files:
            if name.split('.')[0] in link:
                infotable.startrow()
                infotable.addcol(addlink2string(link.split('_')[-1].split('.')[0],Web_dir + link))
                infotable.endrow()

        webpage.substituteplaceholder('PLACEHOLDER_IMAGETABLE_PLACEHOLDER',infotable.gettable(sortable=True))
        temp = 0
        for i in range(len(body_cat)):
            if name.split('_')[2].split('.')[0] == body_cat[i]:
                temp = i
        webpage.substituteplaceholder('PLACEHOLDER_BODY',body_text[temp])
        webpage = Fill_subsection_links(webpage,Location,Reduce_string(name),Save_dir,Web_dir)
        today = datetime.now()
        update_date = str(today.date())
        webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
        #print(Save_dir + Location[2] + name)
        webpage.savepage(Save_dir + Location[2] + name)


    # Now for the non mask stuff
    body_text = "Events are associated with "

    files = glob(Save_dir + Location[4] + '*.html')

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
                                            addlink2string('K2:BS Homepage',Web_dir + 'K2BSHomepage.html'))
            infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')

            infotable.startrow()
            infotable.addcol('Campaigns',colspan=1,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
            infotable.endrow()
            for link in files:
                if name in link:
                    infotable.startrow()
                    infotable.addcol(addlink2string(link.split('-')[0].split('/')[-1],Web_dir + link)) 
                    infotable.endrow()

            webpage.substituteplaceholder('PLACEHOLDER_IMAGETABLE_PLACEHOLDER',infotable.gettable(sortable=True))

            webpage.substituteplaceholder('PLACEHOLDER_BODY',body_text + name.split('_')[-1].split('.')[0])
            webpage = Fill_subsection_links(webpage,Location,Reduce_string(name),Save_dir,Web_dir)
            today = datetime.now()
            update_date = str(today.date())
            webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
            #print(name)
            webpage.savepage(Save_dir + Location[2] + name)
			
def Make_brightness_pages(Location,Save_dir,Web_dir):
	files = glob(Save_dir + Location[2] + '*.html')
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
										addlink2string('K2:BS Homepage',Web_dir+'K2BSHomepage.html'))
		infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')

		infotable.startrow()
		infotable.addcol('Object types',colspan=1,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
		infotable.endrow()

		for link in files:
			if name.split('.')[0] in link:
				infotable.startrow()
				infotable.addcol(addlink2string(link.split('_')[-1].split('.')[0],Web_dir + link))
				infotable.endrow()

		webpage.substituteplaceholder('PLACEHOLDER_IMAGETABLE_PLACEHOLDER',infotable.gettable(sortable=True))
		temp = 0
		body_text = ' events.'
		webpage.substituteplaceholder('PLACEHOLDER_BODY',name.split('_')[-1].split('.')[0] + body_text)
		webpage = Fill_subsection_links(webpage,Location,Reduce_string(name),Save_dir,Web_dir)
		today = datetime.now()
		update_date = str(today.date())
		webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
		webpage.savepage(Save_dir + Location[1] + name)
		
def Make_length_pages(Location,Save_dir,Web_dir):
	files = glob(Save_dir + Location[1] + '*.html')
	print(files)
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
										addlink2string('K2:BS Homepage',Web_dir+'K2BSHomepage.html'))
		infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')

		infotable.startrow()
		infotable.addcol('Object types',colspan=1,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
		infotable.endrow()

		for link in files:
			if name.split('.')[0] in link:
				infotable.startrow()
				infotable.addcol(addlink2string(link.split('_')[-1].split('.')[0],Web_dir + link))
				infotable.endrow()

		webpage.substituteplaceholder('PLACEHOLDER_IMAGETABLE_PLACEHOLDER',infotable.gettable(sortable=True))
		temp = 0
		body_text = ' events.'
		webpage.substituteplaceholder('PLACEHOLDER_BODY',name.split('_')[-1].split('.')[0] + body_text)
		webpage = Fill_subsection_links(webpage,Location,Reduce_string(name),Save_dir,Web_dir)
		today = datetime.now()
		update_date = str(today.date())
		webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
		webpage.savepage(Save_dir + Location[0] + name)
		
def Make_homepage(Location,Save_dir,Web_dir):
	files = glob(Save_dir + Location[0] + '*.html')
	defaultwebpagename = './default/defaultpage_K2BS_homepage.html'
	webpage = webpageclass()
	webpage.loaddefaultpage(defaultwebpagename)
	webpage.substituteplaceholder('PLACEHOLDER_TITLE_PLACEHOLDER','K2: Background Survey')
	#webpage.substituteplaceholder('PLACEHOLDER_TYPE_PLACEHOLDER', name.split('_')[-1].split('.')[0])
	infotable = htmltable(10,border=1,cellspacing=0,cellpadding=2,width='200px')
	infotable.startrow()
	infotable.addcol('Event length',colspan=1,bold=1, color = 'black', bgcolor = 'grey',fontscale="+2")
	infotable.endrow()

	for link in files:
		infotable.startrow()
		infotable.addcol(addlink2string(link.split('/')[-1].split('.')[0],Web_dir + link))
		infotable.endrow()
	webpage.substituteplaceholder('PLACEHOLDER_IMAGETABLE_PLACEHOLDER',infotable.gettable(sortable=True))		
	today = datetime.now()
	update_date = str(today.date())
	webpage.substituteplaceholder('PLACEHOLDER_LASTUPDATE_PLACEHOLDER',update_date)
	webpage.savepage(Save_dir + 'K2BSHomepage.html')



def Make_all(data_directory = '/home/ryanr/public_html/k2bs/data/',   #'/export/maipenrai2/skymap/ryanr/kepler/k2bs/',
			 location = ['length/','brightness/','category/','sub_category/','events/','event/'],
			 Save_dir = '/home/ryanr/public_html/k2bs/',
			 Web_dir = 'http://www.mso.anu.edu.au/~ryanr/k2bs/'):

	camps = glob(data_directory + 'c*/')
	for camp in camps:
		print(camp)
		Make_individual_event_page(camp,location,Save_dir,Web_dir)
		Make_candidate_webpage(camp,location,Save_dir,Web_dir)
		print("Done " + camp.split('/')[-1])
	Make_category_pages(location,Save_dir,Web_dir)
	Make_brightness_pages(location,Save_dir,Web_dir)
	Make_length_pages(location,Save_dir,Web_dir)
	Make_homepage(location,Save_dir,Web_dir)
	print('Made internet!')



if __name__ == '__main__':
	Make_all()

