% main code for estimating model with finite horizon

%***********************************************
% first period
%***********************************************

donnees=xlsread('database');
R=donnees(:,1);
Q=donnees(:,3);

d=812;  
f=1483;  
h=1419; 
Q0=Q(d-1);

a=0.0032334; 
I=5593929;  
alpha=0.0065322; 
sigma2=0.0053494;  
precision=20; 
precision2=100;

r=0.1/365;

param_init=[a,I];

param=estimation_parametres_hf(param_init,R,Q,d,f,h,alpha,sigma2,r,precision);
a=param(1) % a=0.0035 
I=param(2) % I=5268500 

mat=simulation_Q_hf_Bt(R,Q0,d,f,h,a,r,I,alpha,sigma2,precision2); 
% regroupe Q_sim et Bt pour exporter

xlswrite('periode1',mat)
fileID = fopen('param1.txt','w');
fprintf(fileID,'%e %e\n',a,I)

%***********************************************
% second period
%***********************************************

donnees=xlsread('database');
R=donnees(:,1);
Q=donnees(:,3);

d=2091; 
f=3003; 
h=2738; 
Q0=Q(d-1);

a=0.0020738; 
I=1825; 
alpha=0.00125612; 
sigma2=0.0014915; 
precision=20; 
precision2=100;

r=0.1/365;

param_init=[a,I];

param=estimation_parametres_hf(param_init,R,Q,d,f,h,alpha,sigma2,r,precision);
a=param(1) % a=0.0023
I=param(2) % I=1655.2


mat=simulation_Q_hf_Bt(R,Q0,d,f,h,a,r,I,alpha,sigma2,precision2); 
% regroupe Q_sim et Bt pour exporter

xlswrite('periode2',mat)
fileID = fopen('param2.txt','w');
fprintf(fileID,'%e %e\n',a,I)

