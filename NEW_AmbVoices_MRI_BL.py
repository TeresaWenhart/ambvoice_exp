
# conditions file and variables
#---------------------------------------------      

#arrays for variables of conditions file, read into data frame

ExpConditions = pd.read_csv(".\\Experiment_trials\\Baseline\\conditions_Baseline_rand.csv") 
ExpConditions.head()

#select columns via: ExpConditions.'columnname'

#-----------------------------------
####################################
#experimental task (according to selection in GUI ("Ins", "Gen", "Tim", "Voc"))
####################################
#-----------------------------------

#prepare to start trials

thistask 			= 'Bas' # current block
thistrials 			= ExpConditions #trials for this block
thisinstruction 	= instructions# instruction for this block
thisimage           = images#set instruction image for block
thisN 				= Ntrials #number of trials for this block
#creating a series of ISI; this is done once before to have the same total ISI time per participant and hence the same total length of the block
reps                = thisN/6
thisISI             = numpy.repeat(ISI_range,reps)
thisISI_jitter 		= numpy.random.choice(thisISI, thisN, replace=False) #equally distributed ISI
thisSound 			= sound.Sound('A', secs=10) #initialise sound
kb 					= keyboard.Keyboard() #initialise keyboard 
kb.keys 			= []
kb.rt 				= []



#block instruction
#------------------------------------------------

instr_thisblock = visual.TextStim(win=mywin, ori=0, name='instr_voice',
    					text=thisinstruction,    font='Arial',
   						pos=[0, 0], height=0.06, wrapWidth=None,
    					color='white', colorSpace='rgb', opacity=1,
    					depth=0.0)

instr_thistask = visual.TextStim(win=mywin, ori=0, name='instr_voice',
    					text=thistask,    font='Arial',
    					pos=[0, 0], height=0.1, wrapWidth=None,
    					color='white', colorSpace='rgb', opacity=1,
    					depth=0.0)

instr_wait = visual.TextStim(win=mywin, ori=0, name='instr_wait',
    					text="Waiting for scanner ...",    font='Arial',
    					pos=[0, -0.6], height=0.06, wrapWidth=None,
    					color='white', colorSpace='rgb', opacity=1,
    					depth=0.0)

instr_prepare = visual.TextStim(win=mywin, ori=0, name='instr_wait',
    					text="experiment starts in 20 seconds ",    font='Arial',
    					pos=[0, -0.6], height=0.06, wrapWidth=None,
    					color='white', colorSpace='rgb', opacity=1,
    					depth=0.0)

screen_endTHX = visual.TextStim(win=mywin, ori=0, name='endpage',
    					text=endTHX,    font='Arial',
    					pos=[0, 0], height=0.1, wrapWidth=None,
    					color='white', colorSpace='rgb', opacity=3,
    					depth=0.0)


instr_thisblock.setAutoDraw(True)
thisimage.setAutoDraw(True)

mywin.flip()

end = True
while end:
    for key in event.getKeys():
        if key in ['escape']: 
            mywin.close()
            core.quit()
        if key in ['t']:#trigger from Scanner to start experiment
            scannerClock.reset() #reset and start time measurement of scanner
            instr_wait.setAutoDraw(False) 
            end = False
        if key in ['space']:#instruction clear
            instr_thisblock.setAutoDraw(False)
            instr_wait.setAutoDraw(True)
            mywin.flip()

instr_thisblock.setAutoDraw(False)
instr_prepare.setAutoDraw(True) 
mywin.flip()
core.wait(25)
instr_prepare.setAutoDraw(False)

#start of trials

trial_num = 0
end = True
#key2 = event.BuilderKeyResponse() 
#instruction of block


#blank period between  isntruction and trials

mywin.flip()
while end:
    # exit if trial limit reached
    if trial_num >= (thisN-1):
        thisSound.stop()
        end = False
    if trial_num >= 0:
        # start time measurement
        trialClock.reset()
        kb.clock.reset()
        kb.keys = []
        kb.rt = []
        #draw button press instruction to screen
        
        
        
        #select and start sound
        thisSound.setSound(thistrials.iloc[trial_num, 9])
        thisSound.play()
        thistrial_time = scannerClock.getTime()
        mywin.flip()
        # send trigger by sound
        if useTrigger:
            Trigger().send('sound')
        
        # set conditions
        
        trial_finished = 0
        while trial_finished == 0:
            t = trialClock.getTime()
            keys = kb.getKeys(['b','g','r', 'z','escape'])
            
            # end trial if duration > 6s + thisISI_jitter
            if t >= (0.6+thisISI_jitter[trial_num]):
                thisSound.stop()
                trial_finished = 1
                #mywin.flip()
                
            # trigger events for escape key
            for key in keys:
                if key in ['escape']: 
                    thisSound.stop()
                    mywin.close()
                    core.quit() 
            if len(keys):
                #if useTrigger:
                #    Trigger().send('key')
                key2= keys[0]  # at least one key was pressed 
                kb.keys = key2.name  # just the last key pressed
                kb.rt = round(key2.rt,5)        
        
        # write trial data to csv
        thisExp.addData('trialnr', thistrials.iloc[trial_num, 0])
        thisExp.addData('trial', thistrials.iloc[trial_num, 1])
        thisExp.addData('Block', thistrials.iloc[trial_num, 2])
        thisExp.addData('Category1', thistrials.iloc[trial_num, 3])
        thisExp.addData('Prototype1', thistrials.iloc[trial_num, 4])
        thisExp.addData('Category2', thistrials.iloc[trial_num, 5])
        thisExp.addData('Prototype2', thistrials.iloc[trial_num, 6])
        thisExp.addData('morphrate1', thistrials.iloc[trial_num, 7])
        thisExp.addData('morphrate2', thistrials.iloc[trial_num, 8])
        thisExp.addData('names', thistrials.iloc[trial_num, 9])
        thisExp.addData('ISI_jitter', str(thisISI_jitter[trial_num]))
        if kb.keys in ['', [], None]:  # No response was made
            kb.keys = None
        thisExp.addData('key',kb.keys)
        
        thisExp.addData('rt', kb.rt)
        print('#################################')
        print('Trial ',thistrials.iloc[trial_num, 2],' ',thistrials.iloc[trial_num, 0], ':')
        print(thistrials.iloc[trial_num, 3], ' ',thistrials.iloc[trial_num, 7], ' / ',thistrials.iloc[trial_num, 5],' ', thistrials.iloc[trial_num, 8])
        print('Response: ',kb.keys,' RT: ', kb.rt)
        #save information if sound was sucessfully played in data file
        if thisSound.status == NOT_STARTED:
            play=0
        elif thisSound.status == STARTED:
            play = 1
        elif thisSound.status == FINISHED:
            play = 2
            
        thisExp.addData('play', play)
        thisExp.addData('onset', thistrial_time)
        thisExp.nextEntry()
        trial_num += 1
#---------------------------------------------


#cleanup
thisimage.setAutoDraw(False)
screen_endTHX.setAutoDraw(True)
mywin.flip()
core.wait(10)
screen_endTHX.setAutoDraw(False)
scannerClock.getTime()
mywin.close()
core.quit()
