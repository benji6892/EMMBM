% Main code for problem with onvex constraint
clear all 
close all


donnees=xlsread('database');
R=donnees(:,1);
Q=donnees(:,3);


% 

% Guessed parameters; Annual values

a           =0.69594537446421012; %0.0032334 
%a           =0.7665; %0.0032334 

eta         = 2;
scale       = 0.4;

% Brownian Parameters; Annual Values

alpha       =0.91582303693997913; %0.0065322 
%alpha       = 0.5179;
sigma2      =0.696228159836; %0.0053494 
%sigma2      =0.523;
mu          = alpha+a;

r           =0.1;


% Step 1: Evaluate R (reservation productivity at the final date t=T in the last iteration period)

%Evaluate the caracteristic equation of the Cauchy-Euler equation
coef            = [sigma2/2 (mu-sigma2/2) -r-a];
beta            = roots(coef);
beta            = max(beta);                                               % Positive root

P_bar             = (beta/(beta-1))*(r-alpha);

% Time unit
length_time       = 1;

param_init=[length_time,a,eta,scale];

[Pmesh, policy, cutoff]=Simu_policy_constrained_v0(param_init,alpha,sigma2,r);

figure
plot(Pmesh,policy,'Linewidth',2)
xlabel('P')
ylabel('Policy')
axis tight

% Barrier

barrier_guess   = 4.1344525933912921;
barrier_guess   = 4;

Cost_guess      = barrier_guess/cutoff;
Daily_cost      = Cost_guess*365*length_time
Baseline_cost   = barrier_guess/((beta/(beta-1))*(r-alpha))*365
Ratio_cost      = ((beta/(beta-1))*(r-alpha))/cutoff*length_time

% commented: values for parameters and dates used in the paper (in case you want to change them to make tests).

d=2091; %812 
f=3750; %1483 

Q0=Q(d-1);

Q_sim = simulation_Q_constrained(Pmesh, policy, cutoff, Cost_guess, length_time, a, Q0, R, d, f);

figure
plot(d:f,log(Q_sim))
hold on
plot(d:f,log(Q(d:f)))


return


% 
% a=param(1) % a=0.0035 
% I=param(2) % I=5268500 
% 
% % Q_sim=simulation_Q_hf(R,Q0,d,f,h,a,r,I,alpha,sigma2,precision);
% % figure
% % plot(d:f,Q_sim,d:f,Q(d:f))
% % figure
% % plot(d:f,log(Q_sim),d:f,log(Q(d:f)))
% 
% mat=simulation_Q_hf_Bt(R,Q0,d,f,h,a,r,I,alpha,sigma2,precision2); 
% % regroupe Q_sim et Bt pour exporter
% 
% xlswrite('periode1',mat)
% fileID = fopen('param1.txt','w');
% fprintf(fileID,'%e %e\n',a,I)
% 
% %***********************************************
% % deuxieme periode
% %***********************************************
% 
% donnees=xlsread('database');
% R=donnees(:,1);
% Q=donnees(:,3);
% 
% d=2091; %2091
% f=3003; %3003
% h=2738; %2738
% Q0=Q(d-1);
% 
% a=0.0020738; %0.0020738
% I=1825; %1825
% alpha=0.00125612; %0.00125612
% sigma2=0.0014915; %0.0014915
% precision=20; % y aller molo avec la premiere periode: ca prend 3 plombes.
% precision2=100;
% 
% r=0.1/365;
% 
% param_init=[a,I];
% 
% param=estimation_parametres_hf(param_init,R,Q,d,f,h,alpha,sigma2,r,precision);
% a=param(1) % a=0.0023
% I=param(2) % I=1655.2
% 
% % Q_sim=simulation_Q_hf(R,Q0,d,f,h,a,r,I,alpha,sigma2,precision);
% % figure
% % plot(d:f,Q_sim,d:f,Q(d:f))
% % figure
% % plot(d:f,log(Q_sim),d:f,log(Q(d:f)))
% 
% mat=simulation_Q_hf_Bt(R,Q0,d,f,h,a,r,I,alpha,sigma2,precision2); 
% % regroupe Q_sim et Bt pour exporter
% 
% xlswrite('periode2',mat)
% fileID = fopen('param2.txt','w');
% fprintf(fileID,'%e %e\n',a,I)
% 
% barrier_guess = 4.1344525933912921;
