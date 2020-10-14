%create conditions file for auditory experiment

%folder of stimuli
cd 'C:\Users\teresa\Documents\UZH_Arbeit\Human_instrument_morphing\Experiment_trials\Gender_task'
filedir='C:\Users\teresa\Documents\UZH_Arbeit\Human_instrument_morphing\Experiment_trials\Gender_task'
condition_dir='..\Experiment_trials\Gender_task\'
filelist=dir('*.wav')
addpath('C:\Users\teresa\Documents\MATLAB\toolboxes')


trialnr=[1:1:4*24]'
trial=[1:1:24]'
morphrate1=cell(24,1)
morphrate2=cell(24,1)
Block=cell(24,1)
Category1=cell(24,1)
Category2=cell(24,1)
Prototype1=cell(24,1)
Prototype2=cell(24,1)
names=cell(24,1)
directory=cell(24,1)


for i=1:24
    filename=filelist(i,1).name
    names{i,:}=[condition_dir,filename]
    Block{i,:}="Gen"
    Stimulus=filename(1:17)
    Category1{i,:} = Stimulus(1:3)
    Prototype1{i,:} = Stimulus(4)
    Category2{i,:} = Stimulus(6:8)
    Prototype2{i,:} = Stimulus(9)
    morphrate1{i,:}= Stimulus(11:13)
    morphrate2{i,:}= Stimulus(15:17)
end


mytable=table(trial, Block, Category1, Prototype1, Category2, Prototype2, morphrate1, morphrate2, names)
mytable=repmat(mytable, [4 1])

%--------------------
%try to find a random order, where neighboring rows do not have the same
%instruments/voices
%--------------------

%initial new order
randtrials= randperm(96)
newtable=mytable(randtrials,:)

%find inidces of rows i, that contain the same sounds as the row i-1
indices=[]
for i=2:96
                A=char(table2cell(newtable(i,4)))
                B=char(table2cell(newtable(i-1,4)))
                if A=='1'
                    indices=[indices,i]
                    i=i+1
                else
                    i=i+1
                end
end

%----create two tables, for prototype 1 vs. prototype 2 trials
T1=newtable
T1(indices,:)=[]
T2=newtable(indices,:)
%----interleave tables to one new table
newtable=interleave(1,T1,T2)
 
mytable = addvars(mytable,trialnr,'Before','trial');
writetable(mytable,'conditions_Gender.csv', 'Delimiter',',') 
newtable = addvars(newtable,trialnr,'Before','trial');
writetable(newtable,'conditions_Gender_rand.csv', 'Delimiter',',')  

clear
clc
