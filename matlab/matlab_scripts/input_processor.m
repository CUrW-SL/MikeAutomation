clc
clear all
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
addpath('C:\Program Files\MATLAB\R2019b\mbin');
%dfsManager()
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%MMD
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Read data file
infile = fopen('mike_dis.txt');
if infile>0
    D = textscan(infile, '%s %f', 'Delimiter',',');
    fclose(infile);
end
S = datetime(D{1}, 'InputFormat', 'yyyy-MM-dd HH:mm:ss');
R = [D{2}];
fdt = S(1);
[fy,fM,fd] = ymd(fdt);
[fh,fm,fs] = hms(fdt);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

NET.addAssembly('DHI.Generic.MikeZero.EUM');
NET.addAssembly('DHI.Generic.MikeZero.DFS');
H = NETaddDfsUtil();
import DHI.Generic.MikeZero.DFS.*;
import DHI.Generic.MikeZero.DFS.dfs123.*;
import DHI.Generic.MikeZero.*

% Flag specifying whether dfs0 file stores floats or doubles.
% MIKE Zero assumes floats, MIKE URBAN handles both.
useDouble = false;
%MMD
% Flag specifying wether to use the MatlabDfsUtil for writing, or whehter
% to use the raw DFS API routines. The latter is VERY slow, but required in
% case the MatlabDfsUtil.XXXX.dll is not available.
useUtil = ~isempty(H);

if (useDouble)
  dfsdataType = DfsSimpleType.Double;
else
  dfsdataType = DfsSimpleType.Float;
end

% Create a new dfs1 file
filename = 'input_matlab_discharge.dfs0';

% Create an empty dfs1 file object
factory = DfsFactory();
builder = DfsBuilder.Create('input_matlab_discharge','Matlab DFS',0);

builder.SetDataType(0);
builder.SetGeographicalProjection(factory.CreateProjectionGeoOrigin('UTM-33',12,54,2.6));
builder.SetTemporalAxis(factory.CreateTemporalNonEqCalendarAxis(eumUnit.eumUsec,System.DateTime(fy,fM,fd,fh,fm,fs)));

% Add items
item1 = builder.CreateDynamicItemBuilder();
item1.Set('Discharge', DHI.Generic.MikeZero.eumQuantity(eumItem.eumIDischarge,eumUnit.eumUm3PerSec), dfsdataType);
item1.SetValueType(DataValueType.Instantaneous);
item1.SetAxis(factory.CreateAxisEqD0());
builder.AddDynamicItem(item1.GetDynamicItemInfo());

% Create the file - make it ready for data
builder.CreateFile(filename);
dfs = builder.GetFile();

% Write 481 time steps to the file, preallocate vector
% for time and a matrix for data for each item.
numTimes = 481;
times = zeros(numTimes,1);
data  = zeros(numTimes,1);

% Create time vector - constant time step of 15 min here
times(:) = 900*(0:numTimes-1)';

% Create data vector, for each item
data(:,1) = R;
% Remove negative values from rain item
data(data(:,1) < 0,1) = 0;

% Put some date in the file
tic
if useUtil
  % Write to file using the MatlabDfsUtil
  MatlabDfsUtil.DfsUtil.WriteDfs0DataDouble(dfs, NET.convertArray(times), NET.convertArray(data, 'System.Double', size(data,1), size(data,2)))
else
  % Write to file using the raw .NET API (very slow)
  for i=1:numTimes
    if (useDouble)
      dfs.WriteItemTimeStepNext(times(i), NET.convertArray(data(i,1))); 
    else
      dfs.WriteItemTimeStepNext(times(i), NET.convertArray(single(data(i,1)))); 
    end
    if (mod(i,100) == 0)
      fprintf('i = %i of %i\n',i,numTimes);
    end
  end
end
toc

dfs.Close();

fprintf('\nFile created: ''%s''\n',filename);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Tide File Creation
%Read data file
infile = fopen('mike_tide.txt');
if infile>0
    D = textscan(infile, '%s %f', 'Delimiter',',');
    fclose(infile);
end
S = datetime(D{1}, 'InputFormat', 'yyyy-MM-dd HH:mm:ss');
R = [D{2}];
fdt = S(1);
[fy,fM,fd] = ymd(fdt);
[fh,fm,fs] = hms(fdt);


% Flag specifying whether dfs0 file stores floats or doubles.
% MIKE Zero assumes floats, MIKE URBAN handles both.
useDouble = false;
%MMD
% Flag specifying wether to use the MatlabDfsUtil for writing, or whehter
% to use the raw DFS API routines. The latter is VERY slow, but required in
% case the MatlabDfsUtil.XXXX.dll is not available.
useUtil = ~isempty(H);

if (useDouble)
  dfsdataType = DfsSimpleType.Double;
else
  dfsdataType = DfsSimpleType.Float;
end

% Create a new dfs1 file
filename = 'input_matlab_tide.dfs0';

% Create an empty dfs1 file object
factory = DfsFactory();
builder = DfsBuilder.Create('input_matlab_tide','Matlab DFS',0);

builder.SetDataType(0);
builder.SetGeographicalProjection(factory.CreateProjectionGeoOrigin('UTM-33',12,54,2.6));
builder.SetTemporalAxis(factory.CreateTemporalNonEqCalendarAxis(eumUnit.eumUsec,System.DateTime(fy,fM,fd,fh,fm,fs)));

% Add items
item1 = builder.CreateDynamicItemBuilder();
item1.Set('Tide', DHI.Generic.MikeZero.eumQuantity(eumItem.eumIWaterLevel,eumUnit.eumUmeter), dfsdataType);
item1.SetValueType(DataValueType.Instantaneous);
item1.SetAxis(factory.CreateAxisEqD0());
builder.AddDynamicItem(item1.GetDynamicItemInfo());

% Create the file - make it ready for data
builder.CreateFile(filename);
dfs = builder.GetFile();

% Write 121 time steps to the file, preallocate vector
% for time and a matrix for data for each item.
numTimes = 121;
times = zeros(numTimes,1);
data  = zeros(numTimes,1);

% Create time vector - constant time step of 15 min here
times(:) = 3600*(0:numTimes-1)';

% Create data vector, for each item
data(:,1) = R;
% Remove negative values from rain item
data(data(:,1) < 0,1) = 0;

% Put some date in the file
tic
if useUtil
  % Write to file using the MatlabDfsUtil
  MatlabDfsUtil.DfsUtil.WriteDfs0DataDouble(dfs, NET.convertArray(times), NET.convertArray(data, 'System.Double', size(data,1), size(data,2)))
else
  % Write to file using the raw .NET API (very slow)
  for i=1:numTimes
    if (useDouble)
      dfs.WriteItemTimeStepNext(times(i), NET.convertArray(data(i,1))); 
    else
      dfs.WriteItemTimeStepNext(times(i), NET.convertArray(single(data(i,1)))); 
    end
    if (mod(i,100) == 0)
      fprintf('i = %i of %i\n',i,numTimes);
    end
  end
end
toc

dfs.Close();

fprintf('\nFile created: ''%s''\n',filename);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Rainfall File Creation
%Read data file
infile = 'mike_rf.txt';
D = readtable(infile, 'Delimiter', ',');
S = D{:,1};
R = [D{:,2:end}; zeros(1,width(D)-1)];
Rhedings = D.Properties.VariableNames(1,2:end);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fdt = S(1);
[fy,fM,fd] = ymd(fdt);
[fh,fm,fs] = hms(fdt);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Flag specifying whether dfs0 file stores floats or doubles.
% MIKE Zero assumes floats, MIKE URBAN handles both.
useDouble = false;
%MMD
% Flag specifying wether to use the MatlabDfsUtil for writing, or whehter
% to use the raw DFS API routines. The latter is VERY slow, but required in
% case the MatlabDfsUtil.XXXX.dll is not available.
useUtil = ~isempty(H);

if (useDouble)
  dfsdataType = DfsSimpleType.Double;
else
  dfsdataType = DfsSimpleType.Float;
end

% Create a new dfs1 file
filename = 'input_matlab_rain.dfs0';

% Create an empty dfs1 file object
factory = DfsFactory();
builder = DfsBuilder.Create('input_matlab_rain','Matlab DFS',0);

builder.SetDataType(0);
builder.SetGeographicalProjection(factory.CreateProjectionGeoOrigin('UTM-33',12,54,2.6));
builder.SetTemporalAxis(factory.CreateTemporalNonEqCalendarAxis(eumUnit.eumUsec,System.DateTime(fy,fM,fd,fh,fm,fs)));

% Write 120 time steps to the file, preallocate vector
% for time and a matrix for data for each item.
numTimes = length(S)+1;
times = zeros(numTimes,1);
data  = zeros(numTimes,1);

% Add items
items = cell(width(D)-1,1);
for n = 1:width(D)-1
    ID = char(Rhedings(n));
    items{n} = builder.CreateDynamicItemBuilder();
    items{n}.Set(ID, DHI.Generic.MikeZero.eumQuantity(eumItem.eumIRainfall,eumUnit.eumUmillimeter), dfsdataType);
    items{n}.SetValueType(DataValueType.StepAccumulated);
    items{n}.SetAxis(factory.CreateAxisEqD0());
    builder.AddDynamicItem(items{n}.GetDynamicItemInfo());
    
    % Create data vector, for each item
    data(:,n) = R(:,n);
    % Remove negative values from rain item
    data(data(:,n) < 0,1) = 0;
end

% Create the file - make it ready for data
builder.CreateFile(filename);
dfs = builder.GetFile();


% Create time vector - constant time step of 1 hr here
times(:) = 900*(0:numTimes-1)';

% Put some date in the file
tic
if useUtil
  % Write to file using the MatlabDfsUtil
  MatlabDfsUtil.DfsUtil.WriteDfs0DataDouble(dfs, NET.convertArray(times), NET.convertArray(data, 'System.Double', size(data,1), size(data,2)))
else
  % Write to file using the raw .NET API (very slow)
  for i=1:numTimes
    if (useDouble)
        for j = 1:size(data,2)
            dfs.WriteItemTimeStepNext(times(i), NET.convertArray(data(i,j)));
        end
    else
        for j = 1:size(data,2)
            dfs.WriteItemTimeStepNext(times(i), NET.convertArray(single(data(i,j))));
        end
    end
    if (mod(i,100) == 0)
      fprintf('i = %i of %i\n',i,numTimes);
    end
  end
end
toc

dfs.Close();
fclose('all');
fprintf('\nFile created: ''%s''\n',filename);
%MMD
