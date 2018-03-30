% ENME 489Y: Remote Sensing
% Spring 2018
% Code reads in .txt file and plots 3D point cloud

clear all; close all; clc; format compact

% Load in (x, y, z) data

% If loading file from your local machine:
% A = importdata('Sample_range_data.txt');

% If using MATLAB via Virtual Computing Lab, identify folder on your laptop:
A = importdata('\\client\C$\Users\Steve\PycharmProjects\test1\testdataraymond\testresults.txt');

% Extract and assign data
x = A(:,1);
y = A(:,2);
z = A(:,3);

% Plot point cloud using pcshow()
figure(1)
pcshow([x ,y, z]);
title('3D Point Cloud');
xlabel('X');
ylabel('Y');
zlabel('Z');
axis equal

% Plot point cloud using plot3()
az = 0;
el = 10;
figure(2); hold on
% plot3(x ,y, z, 'b.','MarkerSize',10);
plot3(0, 0, 0,'r.','MarkerSize',40)
view(az, el);

% Color code by depth
for a = 1:length(y)
    if y(a) < 60
        plot3(x(a) ,y(a), z(a), 'r.','MarkerSize',10);
    else
        plot3(x(a) ,y(a), z(a), 'b.','MarkerSize',10);
    end
end
title('3D Point Cloud');
xlabel('X');
ylabel('Y');
zlabel('Z');
axis equal
grid on

% Animate point cloud using plot3()
az = [-90:1:90];
el = 30;

for i = 1:length(az)
    figure(3); hold on
    % pcshow([x ,y, z]);
    plot3(x ,y, z, 'b.','MarkerSize',10);
    plot3(0, 0, 0,'r.','MarkerSize',40)
    view(az(i), el);
    title('3D Point Cloud');
    xlabel('X');
    ylabel('Y');
    zlabel('Z');
    axis equal
    grid on
    pause(0.25)
end
