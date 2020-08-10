% Main code for problem with onvex constraint

clear all 
close all

%% LOAD DATA

donnees=xlsread('database');
R=donnees(:,1);
Q=donnees(:,3);

Baseline_table = readtable('modele_base_bulle.csv');
Time_vec = datetime(Baseline_table.dates);

Baseline = xlsread('modele_base_bulle');
Q_baseline = Baseline(:,1);

% commented: values for parameters and dates used in the paper (in case you want to change them to make tests).

d=2091; %812 
f=3750; %1483 
f=3850;

% Price data
d_asics         = 1787;
Dates_ASICS     = d_asics +[0, 121, 212, 304, 396, 639, 974, 1492, 1696, 1996];
Price_ASICS     = [1666.6666666666667, 2260.0, 866.2131519274376, 700.0,...
                    321.7391304347826, 375.10288065843616, 171.42857142857142,...
                    369.92857142857144, 60.60606060606061, 30.208333333333332];
start_ASICS = find(Dates_ASICS>=d,1);
if max(Dates_ASICS)<f
    end_ASICS = length(Dates_ASICS)+1;
else
    end_ASICS   = find(Dates_ASICS>f,1);
end
Dates_ASICS = Dates_ASICS(start_ASICS:end_ASICS-1);
Price_ASICS = Price_ASICS(start_ASICS:end_ASICS-1);

%% 


% Guessed parameters; Annual values
a           = 0.6788; %0.0032334 
a           =0.678797073130826; %0.0032334 
a           = 0.6551;
%a           = 0.75695760353470187;

eta         = 10;
eta         = 39.565526624179483;
eta         = 14.1990;

scale       = 1;

% Brownian Parameters; Annual Values

alpha       = 0.91582303693997913; %0.0065322 
alpha       = 0.88631325975190067;
%alpha       = 0.45848283883821289;

sigma2      = 0.696228159836; %0.0053494 
sigma2      = 0.70327416999862602;
%sigma2      = 0.54439820776179915;

mu          = alpha+a;

r           = 0.1;


% Step 1: Evaluate R (reservation productivity at the final date t=T in the last iteration period)

%Evaluate the caracteristic equation of the Cauchy-Euler equation
coef            = [sigma2/2 (mu-sigma2/2) -r-a];
beta            = roots(coef);
beta            = max(beta);                                               % Positive root

P_bar             = (beta/(beta-1))*(r-alpha);

% Time unit
length_time       = 0.413624030936984;
length_time       = 0.2501;

param_init=[length_time,a,eta,scale];
tic 
[Pmesh, policy, cutoff]=Simu_policy_constrained_v1(param_init,alpha,sigma2,r);
toc
figure
plot(Pmesh(1:100),policy(1:100),'Linewidth',2)
xlabel('$x$','Interpreter','Latex')
ylabel('$q$','Interpreter','Latex')
grid on
axis tight

% Barrier

barrier_guess   = 4.1344525933912921;
Cost_guess      = barrier_guess/cutoff;
    
options         = optimset('tolX',1.0e-5,'tolFun',1.0e-3,'MaxIter',200);
distance_fun    = @(Cost)distance_constrained(Pmesh, policy, cutoff, Cost, length_time, a, Q, R, d, f);
[cost_opt, fval]= fminsearch(distance_fun,Cost_guess,options);

Daily_cost      = cost_opt*365*length_time
Baseline_cost   = barrier_guess/((beta/(beta-1))*(r-alpha))*365
Ratio_cost      = ((beta/(beta-1))*(r-alpha))/cutoff*length_time

Q0=Q(d-1);

Q_sim    = simulation_Q_constrained(Pmesh, policy, cutoff, cost_opt, length_time, a, Q0, R, d, f);
Cost_sim = simulation_Cost_constrained(Pmesh, policy, cutoff, cost_opt, length_time, a, Q0, R, d, f,eta);

% Costs ASICS
I_d  = Price_ASICS(1)*exp(a*(Dates_ASICS(1)-d));
Cr_d = Daily_cost-I_d;
Det_Price_ASICS = Price_ASICS.*exp(a*(Dates_ASICS-Dates_ASICS(1))/365);    
I_t = Cost_sim - Cr_d;

b_tilde = (1/length_time);
b       = ((Cr_d(1)+I_d(1))*(1+eta)/I_d(1))^(-1/eta)*b_tilde


figure('Units','points','position',[10,10,650,400],'PaperPositionMode','auto')

subplot(2,1,1)
plot(Time_vec,log(Q(d:f)),'Linewidth',3)
hold on
plot(Time_vec,log(Q_sim),'--','Linewidth',3)
plot(Time_vec,Q_baseline,'-.','Linewidth',3)
grid on
xlim([735866.48,737650.52])
xlabel('Time','Interpreter','Latex','Fontsize',12)
ylabel('log $Q$','Interpreter','Latex','Fontsize',12)
leg1=legend('DATA','CONVEX COSTS MODEL ', 'BASELINE MODEL', 'Location','northwest')
leg1.FontSize = 11;

subplot(2,1,2)
plot(Time_vec,I_t,'Linewidth',3)
hold on
plot(Time_vec(Dates_ASICS+1-d),Det_Price_ASICS,'d','Linewidth',4)
grid on
xlim([735866.48,737650.52])
xlabel('Time','Interpreter','Latex','Fontsize',12)
ylabel('Investment Costs','Interpreter','Latex','Fontsize',12)
leg2=legend('CONVEX COSTS MODEL','ONLINE DATA','Location','northwest')
leg2.FontSize = 11;

savefig('Fig_bubble_constrained.fig')
print -depsc2 Fig_bubble_constrained.eps


% %% Estimation
% 
% % grid search
% 
% length_vec = 1/8:1/8:3/4;
% a_vec      = a-.2:.1:a+.2;
% Distance_mat = NaN(length(length_vec),length(a_vec));
% 
% for i=1:length(length_vec)
%     parfor j=1:length(a_vec)
%         param_init =[length_vec(i),a_vec(j)]
%         Distance_mat(i,j)=estimation_parametres_objectif_constrained(param_init,eta,scale,R,Q,d,f,alpha,sigma2,r);
%     end
% end
% 
% [min_val,idx]=min(Distance_mat(:));
% [row,col]=ind2sub(size(Distance_mat),idx);
% 
% options=optimset('display','iter-detailed','tolX',1.0e-5,'tolFun',1.0e-3,'MaxIter',200);
% objectif=@(param)estimation_parametres_objectif_constrained(param,eta,scale,R,Q,d,f,alpha,sigma2,r);
% param_init=[length_time,a];
% arg=fminsearch(objectif,param_init,options);
%     
% 
% return


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
