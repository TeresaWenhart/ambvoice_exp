%-------------------------------
%script to create one joint condition file out of several experimental
%blocks
%-------------------------------
%-------------------------------
%it takes the files containing condition/randomisation  information of
%different experimental blocks saved in different folders and concatenates
%them by row to a joint file.

%CAVE: alle condition files have to have the same number of columns and
%same column names!
%-------------------------------

%folder of experimental block subfolders
cd C:\Users\teresa\Documents\UZH_Arbeit\Human_instrument_morphing\Experiment_trials\
filedir='C:\Users\teresa\Documents\UZH_Arbeit\Human_instrument_morphing\Experiment_trials\'

%get all subfolders
S = dir(fullfile(filedir,'*'));
N = setdiff({S([S.isdir]).name},{'.','..'}); 

%load all condition files within subfolders and append to joint table
newtable=table()
for i = 1:numel(N)
    T = dir(fullfile(filedir,N{i},'*_rand.csv')); % take csv files that specify randomised trial information
    C = {T(~[T.isdir]).name}; % files in subfolder; there should only be one condition file with extension "_rand.csv"
    for j = 1:numel(C)
        F = fullfile(filedir,N{i},C{j}) %fullpath of conditions file (j) in subfolder i
        file= readtable(F)
        C=extractBefore(char(C),'.csv')
        assignin('base', C,file)
        newtable=[newtable;file]
        % do whatever with file F.   
    end
end


%save in filedir as overall conditions file
cd C:\Users\teresa\Documents\UZH_Arbeit\Human_instrument_morphing\Experiment_trials\
writetable(newtable,'all_conditions_rand.csv', 'Delimiter',',')  



