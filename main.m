close all;
format long % Matlab as a great decimal precision

% Software Name: main.m
% SPDX-FileCopyrightText: Copyright (c) 2023 Universidad de Cantabria
% SPDX-License-Identifier: LGPL-3.0 
%
% This software is distributed under the LGPL-3.0 license;
% see the LICENSE file for more details.
%
% Author: Laura MARTIN <lmartin@tlmat.unican.es> et al.

%% READ VALUES FROM FILES
accuracy_requesting = zeros(10000,12); accuracy_processing = zeros(10000,12); accuracy_total= zeros(10000,12);
completeness_requesting = zeros(10000,12); completeness_processing = zeros(10000,12); completeness_total= zeros(10000,12);
precision_requesting = zeros(10000,12); precision_processing = zeros(10000,12); precision_total= zeros(10000,12);
timeliness_requesting = zeros(10000,12); timeliness_processing = zeros(10000,12); timeliness_total= zeros(10000,12);
for i = 0:60
    column = i+1;
  
    % Accuracy
    aux_array=readmatrix('simulations/sim'+string(i)+'/accuracy.csv');
    accuracy_requesting(:,column) = aux_array(2:end,2);
    accuracy_processing(:,column) = aux_array(2:end,3);
    accuracy_total(:,column) = accuracy_requesting(:,column) + accuracy_processing(:,column);
    
    % Completeness
    aux_array=readmatrix('simulations/sim'+string(i)+'/completeness.csv');
    completeness_requesting(:,column) = aux_array(2:end,2);
    completeness_processing(:,column) = aux_array(2:end,3);
    completeness_total(:,column) = completeness_requesting(:,column) + completeness_processing(:,column);
    
    % Precision
    aux_array=readmatrix('simulations/sim'+string(i)+'/precision.csv');
    precision_requesting(:,column) = aux_array(2:end,2);
    precision_processing(:,column) = aux_array(2:end,3);
    precision_total(:,column) = precision_requesting(:,column) + precision_processing(:,column);
    
    % Timeliness
    aux_array=readmatrix('simulations/sim'+string(i)+'/timeliness.csv');
    timeliness_requesting(:,column) = aux_array(2:end,2);
    timeliness_processing(:,column) = aux_array(2:end,3);
    timeliness_total(:,column) = timeliness_requesting(:,column) + timeliness_processing(:,column);
end


%% CALCULATE METRICS

% ACCURACY
accuracy_requesting_average = mean(accuracy_requesting,2); 
accuracy_processing_average = mean(accuracy_processing,2); 
accuracy_total_average = mean(accuracy_total,2);
% Average
accuracy_requesting_average_mean = mean(accuracy_requesting_average);
accuracy_processing_average_mean = mean(accuracy_processing_average);
accuracy_total_average_mean = mean(accuracy_total_average);
% Standard Deviation
accuracy_requesting_average_std = std(accuracy_requesting_average);
accuracy_processing_average_std = std(accuracy_processing_average);
accuracy_total_average_std = std(accuracy_total_average);

% COMPLETENESS
completeness_requesting_average = mean(completeness_requesting,2);
completeness_processing_average = mean(completeness_processing,2);
completeness_total_average = mean(completeness_total,2);
% Average
completeness_requesting_average_mean = mean(completeness_requesting_average(6000:end,:));
completeness_processing_average_mean = mean(completeness_processing_average(6000:end,:));
completeness_total_average_mean = mean(completeness_total_average(6000:end,:));
% Standard Deviation
completeness_requesting_average_std = std(completeness_requesting_average(6000:end,:));
completeness_processing_average_std = std(completeness_processing_average(6000:end,:));
completeness_total_average_std = std(completeness_total_average(6000:end,:));

% PRECISION
precision_requesting_average = mean(precision_requesting,2);
precision_processing_average = mean(precision_processing,2);
precision_total_average = mean(precision_total,2);
% Average
precision_requesting_average_mean = mean(precision_requesting_average(100:end,:));
precision_processing_average_mean = mean(precision_processing_average(100:end,:));
precision_total_average_mean = mean(precision_total_average(100:end,:));
% Standard Deviation
precision_requesting_average_std = std(precision_requesting_average(100:end,:));
precision_processing_average_std = std(precision_processing_average(100:end,:));
precision_total_average_std = std(precision_total_average(100:end,:));

% TIMELINESS
timeliness_requesting_average = mean(timeliness_requesting,2);
timeliness_processing_average = mean(timeliness_processing,2);
timeliness_total_average = mean(timeliness_total,2);
% Average
timeliness_requesting_average_mean = mean(timeliness_requesting_average(100:end,:));
timeliness_processing_average_mean = mean(timeliness_processing_average(100:end,:));
timeliness_total_average_mean = mean(timeliness_total_average(100:end,:)); 
% Standard Deviation
timeliness_requesting_average_std = std(timeliness_requesting_average(100:end,:));
timeliness_processing_average_std = std(timeliness_processing_average(100:end,:));
timeliness_total_average_std = std(timeliness_total_average(100:end,:)); 

% COMPLETE PIPELINE
requesting_total_mean = accuracy_requesting_average_mean + completeness_requesting_average_mean + precision_requesting_average_mean + timeliness_requesting_average_mean;
requesting_total_std = accuracy_requesting_average_std + completeness_requesting_average_std + precision_requesting_average_std + timeliness_requesting_average_std;
processing_total_mean = accuracy_processing_average_mean + completeness_processing_average_mean + precision_processing_average_mean + timeliness_processing_average_mean;
processing_total_std = accuracy_processing_average_std + completeness_processing_average_std + precision_processing_average_std + timeliness_processing_average_std;


%% OBTAIN DATA TO PLOT (median values)
% ACCURACY
accuracy_median = zeros(10000,3);
accuracy_median(:, 1) = median(accuracy_requesting,2);
accuracy_median(:, 2) = median(accuracy_processing,2);
accuracy_median(:, 3) = median(accuracy_total,2);
aux = array2table(accuracy_median);
aux.Properties.VariableNames(1:3) = {'requesting','processing','total'};
writetable(aux,'simulations/median_values/accuracy_median.csv', 'Delimiter',';')

% COMPLETENESS
completeness_median = zeros(10000,3);
completeness_median(:, 1) = median(completeness_requesting,2);
completeness_median(:, 2) = median(completeness_processing,2);
completeness_median(:, 3) = median(completeness_total,2);
aux = array2table(completeness_median);
aux.Properties.VariableNames(1:3) = {'requesting','processing','total'};
writetable(aux,'simulations/median_values/completeness_median.csv', 'Delimiter',';')

% PRECISION
precision_median = zeros(10000,3);
precision_median(:, 1) = median(precision_requesting,2);
precision_median(:, 2) = median(precision_processing,2);
precision_median(:, 3) = median(precision_total,2);
aux = array2table(precision_median);
aux.Properties.VariableNames(1:3) = {'requesting','processing','total'};
writetable(aux,'simulations/median_values/precision_median.csv', 'Delimiter',';')

% TIMELINESS
timeliness_median = zeros(10000,3);
timeliness_median(:, 1) = median(timeliness_requesting,2);
timeliness_median(:, 2) = median(timeliness_processing,2);
timeliness_median(:, 3) = median(timeliness_total,2);
aux = array2table(timeliness_median);
aux.Properties.VariableNames(1:3) = {'requesting','processing','total'};
writetable(aux,'simulations/median_values/timeliness_median.csv', 'Delimiter',';')