import os, re
import bs4,time
import requests
from plyer import notification
##def getscore():
##	url = "http://www.espncricinfo.com/icc-cricket-world-cup-2015/engine/match/656493.json"
##	r = requests.get(url)
##	while r.status_code is not 200:
##		r = requests.get(url)
##	data = json.loads(r.text)
##	player_status = data['match']['current_summary'].strip()
##	team1_name = data['other_scores']['international'][0]['team1_name'].strip()
##	team1_score = data['other_scores']['international'][0]['team1_desc'].replace('&nbsp;ov',' ov').strip()
##	team2_name = data['other_scores']['international'][0]['team2_name'].strip()
##	team2_score = data['other_scores']['international'][0]['team2_desc'].replace('&nbsp;ov',' ov').strip()
##	if not team1_score:
class Score(object):
    alert={}
    titles = ['FOUR',' out ','SIX','runs','!!']
    def __init__(self):

        #will be using it for enhancements
        pass
    @staticmethod
    def getMatch():
        url='http://www.cricbuzz.com/api/html/matches-menu'
        response = requests.get(url,
                                headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                       '6.2; WOW64) AppleWebKit/'
                                                       '537.36 (KHTML, like '
                                                       'Gecko) Chrome/37.0.2062.'
                                                       '120 Safari/537.36'})
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        optionlist={}
        status={}
        global mstatus
        for count,tag in enumerate (soup.find_all('li',{'class':re.compile('cb-lst-mtch')})):
            count+=1
            print ("Enter '{}' for '{}' ".format(count,tag.a['title']))
            optionlist[count] = tag.a['href']
            status[count]=tag.a['title']
        choice = int(raw_input("\n>Enter Your Option here: "))
        if choice in optionlist:
           mstatus=status[choice]
           return Score.getScore('http://www.cricbuzz.com'+optionlist[choice],mstatus)           
        else:
            print'Wrong Option,Select again'
            Score.getMatch()
    @staticmethod
    def getScore(url,mstatus):
        while True:
            response = requests.get(url,
                                    headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                           '6.2; WOW64) AppleWebKit/'
                                                           '537.36 (KHTML, like '
                                                           'Gecko) Chrome/37.0.2062.'
                                                           '120 Safari/537.36'})
            soup = bs4.BeautifulSoup(response.content, "html.parser")
            print '\n'+soup.title.text+'\n'
            print '#'*30+mstatus.rsplit(',', 1)[0]+'#'*30+'\n'
            print soup.find('div',{'class':re.compile('cb-nav-subhdr')} ).text.strip()+'\n'
            if mstatus.rsplit(None, 1)[-1] == 'Live' :
                print soup.find('div',{'class':re.compile('cb-mini-col')} ).text.strip()+'\n'
                match='live'
            else:
                match='past'
            duplicate=''#remove duplicate entries
            for tag in soup.find_all(re.compile('.')):
                try:
                    if match == 'live':
                         print tag.div.find('div',{'class':re.compile('.*cb-ovr-num')}).text+' '+tag.p.text
                         update = [x for x in Score.titles if x in tag.p.text]
##                         if Score.titles in tag.p.text:
                         if update:
                             Score.rknotify(update[0],comm=tag.p.text,ovr=tag.div.find('div',{'class':re.compile('.*cb-ovr-num')}).text)
                    elif match == 'past':
                        if len(tag.p.text) == duplicate:
                            continue
                        else:
                            print tag.p.text+'\n'
                            duplicate=len(tag.p.text)                            
                except Exception as e:
                    pass
            if match == 'past':
                break
            else:
                time.sleep(12)
                print "\n" *40
    @staticmethod
    def rknotify(update,comm,ovr):
        if ovr in Score.alert:
            pass
        else:
           notification.notify(
            title=update,
            message=("{} {}".format(ovr,comm)),
            app_name='Cricbuzz',
            app_icon='1.ico',
            )
           Score.alert[ovr]=comm
while True:
    print "\n" * 500
    Score.getMatch()
    print '#'*30+mstatus.rsplit(',', 1)[0]+'#'*30+'\n'
    print 'Match:'+mstatus+'\n'
    print 'Match Status:'+mstatus.rsplit('-', 1)[-1]+'\n'        
    raw_input("Press Any Key Continue  or CTRL+C to exit!...")

