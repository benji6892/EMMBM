% code principal pour l'horizon fini

donnees=xlsread('database');
R=donnees(:,1);
Q=donnees(:,3);

% commented: values for parameters and dates used in the paper (in case you want to change them to make tests).

d=812; %812 
f=1483; %1483 
h=1419; %1419 
Q0=Q(d-1);

a=0.0032334; %0.0032334 
I=5593929; %5593929 
alpha=0.0065322; %0.0065322 
sigma2=0.0053494; %0.0053494 
precision=20; % y aller molo avec la premiere periode: ca prend 3 plombes.
precision2=100;

r=0.1/365;

param_init=[a,I];

param=estimation_parametres_hf(param_init,R,Q,d,f,h,alpha,sigma2,r,precision);
a=param(1) % a=0.0035 
I=param(2) % I=5268500 

% Q_sim=simulation_Q_hf(R,Q0,d,f,h,a,r,I,alpha,sigma2,precision);
% figure
% plot(d:f,Q_sim,d:f,Q(d:f))
% figure
% plot(d:f,log(Q_sim),d:f,log(Q(d:f)))

mat=simulation_Q_hf_Bt(R,Q0,d,f,h,a,r,I,alpha,sigma2,precision2); 
% regroupe Q_sim et Bt pour exporter

xlswrite('periode1',mat)
fileID = fopen('param1.txt','w');
fprintf(fileID,'%e %e\n',a,I)

%***********************************************
% deuxieme periode
%***********************************************

donnees=xlsread('database');
R=donnees(:,1);
Q=donnees(:,3);

d=2091; %2091
f=3003; %3003
h=2738; %2738
Q0=Q(d-1);

a=0.0020738; %0.0020738
I=1825; %1825
alpha=0.00125612; %0.00125612
sigma2=0.0014915; %0.0014915
precision=20; % y aller molo avec la premiere periode: ca prend 3 plombes.
precision2=100;

r=0.1/365;

param_init=[a,I];

param=estimation_parametres_hf(param_init,R,Q,d,f,h,alpha,sigma2,r,precision);
a=param(1) % a=0.0023
I=param(2) % I=1655.2

% Q_sim=simulation_Q_hf(R,Q0,d,f,h,a,r,I,alpha,sigma2,precision);
% figure
% plot(d:f,Q_sim,d:f,Q(d:f))
% figure
% plot(d:f,log(Q_sim),d:f,log(Q(d:f)))

mat=simulation_Q_hf_Bt(R,Q0,d,f,h,a,r,I,alpha,sigma2,precision2); 
% regroupe Q_sim et Bt pour exporter

xlswrite('periode2',mat)
fileID = fopen('param2.txt','w');
fprintf(fileID,'%e %e\n',a,I)

