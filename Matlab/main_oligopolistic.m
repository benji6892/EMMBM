% Main code for problem with onvex constraint

clear all 
close all

%% LOAD DATA

donnees=xlsread('database');
R=donnees(:,1);
Q=donnees(:,3);

% commented: values for parameters and dates used in the paper (in case you want to change them to make tests).

d=2091; %812 
f=3750; %1483 

% Price data
d_asics         = 1787;
Dates_ASICS     = d_asics +[0, 121, 212, 304, 396, 639, 974, 1492, 1696, 1996];
Price_ASICS     = [1666.6666666666667, 2260.0, 866.2131519274376, 700.0,...
                    321.7391304347826, 375.10288065843616, 171.42857142857142,...
                    369.92857142857144, 60.60606060606061, 30.208333333333332];
start_ASICS = find(Dates_ASICS>=d,1);
end_ASICS   = find(Dates_ASICS>f,1);
Dates_ASICS = Dates_ASICS(start_ASICS:end_ASICS-1);
Price_ASICS = Price_ASICS(start_ASICS:end_ASICS-1);

%% 

% Guessed parameters; Annual values
a           = 0.6788; %0.0032334 
a           =0.678797073130826; %0.0032334 
a           = 0.6551;

% Brownian Parameters; Annual Values

alpha       =0.91582303693997913; %0.0065322 
%alpha       = 0.5179;
sigma2      =0.696228159836; %0.0053494 
%sigma2      =0.523;
mu          = alpha+a;

r           = 0.1;


% Step 1: Evaluate R (reservation productivity at the final date t=T in the last iteration period)

%Evaluate the caracteristic equation of the Cauchy-Euler equation
coef            = [sigma2/2 (mu-sigma2/2) -r-a];
beta            = roots(coef);
beta            = max(beta);                                               % Positive root

P_bar           = (beta/(beta-1))*(r-alpha);

barrier         = 4.1344525933912921;

Cost            = barrier/((beta/(beta-1))*(r-alpha))*365;


% Oligopolistic costs

for i = 2 :20
Cost_olig(i-1)            = barrier/((beta/(beta-1))*(r-alpha)*(i/(i-1)))*365;
competitors(i-1)          = i;
OPremium(i-1)             = 1/(i-1)*100;
end

figure
plot(competitors,Cost_olig,'--','Linewidth',2)
hold on
line(competitors, Cost*ones(size(competitors)),'Linewidth',2)
xlabel('Number of Mining Firms')
ylabel('Cost of Entry')
axis tight

figure
plot(competitors,OPremium,'--','Linewidth',2)
xlabel('Number of Mining Firms')
ylabel('Option Premium in %')



%% Profits distribution

gamma          = 2*(mu-sigma2/2)/sigma2;

ergodic_CDF    = @(x) (x/barrier).^gamma;

ergodic_dens    = @(x) (gamma./x).*(x/barrier).^gamma;

esperance_dens  = @(x) x.*ergodic_dens(x);

Average_revenues = integral(esperance_dens,0,barrier);

x_vec =linspace(.01,barrier,100);

for i=1:length(x_vec)
    CDF(i)   = integral(ergodic_dens ,0,x_vec(i),'ArrayValued',1);
end

figure
plot(x_vec,CDF)

ergodic_Q_dens      = @(Q) -gamma*P_bar^(-(gamma)).*Q^(-gamma-1);

Qlow                = 1/P_bar;

x_vec =linspace(Qlow,10,100);


for i=1:length(x_vec)
CDF_Q(i)   = integral(ergodic_Q_dens ,x_vec(i),Qlow,'ArrayValued',1);
end

figure
plot(x_vec,CDF_Q)

esperance_Q_dens  = @(x) x.*ergodic_Q_dens(x);

Average_Q = integral(esperance_Q_dens,10,Qlow,'ArrayValued',1);

%% Comparative Statics on Average Q

% Prog Tech

a_vec = linspace(0.3,a,10);

for i = 1:length(a_vec)
    mu_a   = alpha+a_vec(i);
    gamma  = 2*(mu_a-sigma2/2)/sigma2;
    
    %Evaluate the caracteristic equation of the Cauchy-Euler equation
    coef            = [sigma2/2 (mu_a-sigma2/2) -r-a_vec(i)];
    beta            = roots(coef);
    beta            = max(beta);                                               % Positive root

    P_bar_a(i)     = (beta/(beta-1))*(r-alpha);

    barrier_a(i)    = Cost*P_bar_a(i)/365;
    barrier         = barrier_a(i);
    Qlow_a(i)       = 1/P_bar_a(i);
    
    ergodic_Q_dens    = @(Q) -gamma*P_bar_a(i)^(-(gamma)).*Q^(-gamma-1);
    esperance_Q_dens  = @(x) x.*ergodic_Q_dens(x);
    %Average_Q_a(i)    = integral(esperance_Q_dens,100,Qlow_a(i),'ArrayValued',1);
    Average_Q_a(i)     = (gamma/(gamma-1))*(1/P_bar_a(i));
    
    Average_Q_a(i)    = Average_Q_a(i)/Average_Q;
    Qlow_a(i)       = Qlow_a(i)/Average_Q;

end


sigma2_vec = linspace(0.1,sigma2,10);

for i = 1:length(sigma2_vec)
    mu_sigma   = alpha+a;
    gamma      = 2*(mu_sigma-sigma2_vec(i)/2)/sigma2_vec(i);
    
    %Evaluate the caracteristic equation of the Cauchy-Euler equation
    coef            = [sigma2_vec(i)/2 (mu_sigma-sigma2_vec(i)/2) -r-a];
    beta            = roots(coef);
    beta            = max(beta);                                               % Positive root

    P_bar_sigma(i)     = (beta/(beta-1))*(r-alpha);

    barrier_sigma(i)    = Cost*P_bar_sigma(i)/365;
    barrier             = barrier_sigma(i);
    Qlow_sigma(i)       = 1/P_bar_sigma(i);
    
    ergodic_Q_dens    = @(Q) -gamma*P_bar_sigma(i)^(-(gamma)).*Q^(-gamma-1);
    esperance_Q_dens  = @(x) x.*ergodic_Q_dens(x);
    %Average_Q_sigma(i)= integral(esperance_Q_dens,100,Qlow_sigma(i),'ArrayValued',1);
    Average_Q_sigma(i)= (gamma/(gamma-1))*(1/P_bar_sigma(i));
   
    
    Average_Q_sigma(i) = Average_Q_sigma(i)/Average_Q;
    Qlow_sigma(i)       = Qlow_sigma(i)/Average_Q;
    
end


alpha_vec = linspace(0.25,alpha,10);

for i = 1:length(alpha_vec)
    mu_alpha   = alpha_vec(i)+a;
    gamma      = 2*(mu_alpha-sigma2/2)/sigma2;
    
    %Evaluate the caracteristic equation of the Cauchy-Euler equation
    coef            = [sigma2/2 (mu_alpha-sigma2/2) -r-a];
    beta            = roots(coef);
    beta            = max(beta);                                               % Positive root

    P_bar_alpha(i)     = (beta/(beta-1))*(r-alpha);

    barrier_alpha(i)    = Cost*P_bar_alpha(i)/365;
    barrier             = barrier_alpha(i);
    Qlow_alpha(i)       = 1/P_bar_alpha(i);

    ergodic_Q_dens    = @(Q) -gamma*P_bar_alpha(i)^(-(gamma)).*Q^(-gamma-1);
    esperance_Q_dens  = @(x) x.*ergodic_Q_dens(x);
    %Average_Q_alpha(i)= integral(esperance_Q_dens,100,Qlow_alpha(i),'ArrayValued',1);
    Average_Q_alpha(i)     = (gamma/(gamma-1))*(1/P_bar_alpha(i));
    
    Average_Q_alpha(i) = Average_Q_alpha(i)/Average_Q;
    Qlow_alpha(i)       = Qlow_alpha(i)/Average_Q;

end

cost_vec = linspace(0.7,1,10);

for i = 1:length(cost_vec)
    mu         = alpha+a;
    gamma      = 2*(mu-sigma2/2)/sigma2;
    
    %Evaluate the caracteristic equation of the Cauchy-Euler equation
    coef            = [sigma2/2 (mu-sigma2/2) -r-a];
    beta            = roots(coef);
    beta            = max(beta);                                               % Positive root

    P_bar_cost(i)     = cost_vec(i).*(beta/(beta-1))*(r-alpha);

    barrier_cost(i)    = Cost*cost_vec(i)*P_bar_cost(i)/365;
    barrier             = barrier_cost(i);
    Qlow_cost(i)       = 1/P_bar_cost(i);

    ergodic_Q_dens    = @(Q) -gamma*P_bar_cost(i)^(-(gamma)).*Q^(-gamma-1);
    esperance_Q_dens  = @(x) x.*ergodic_Q_dens(x);
    %Average_Q_cost(i)= integral(esperance_Q_dens,100,Qlow_cost(i),'ArrayValued',1);
    Average_Q_cost(i)     = (gamma/(gamma-1))*(1/P_bar_cost(i));
    
    Average_Q_cost(i) = Average_Q_cost(i)/Average_Q;
    Qlow_cost(i)       = Qlow_cost(i)/Average_Q;

end

figure('Units','points','position',[10,10,600,450],'PaperPositionMode','auto')

subplot(2,2,1)
plot(a_vec,Qlow_a,'Linewidth',2)
hold on
plot(a_vec,Average_Q_a,'--','Linewidth',2)
axis tight
grid on
xlabel('a','interpreter','latex','FontSize',14,'FontWeight','bold','FontName','Times')
ylabel('Q','interpreter','latex','FontSize',12,'FontWeight','bold','FontName','Times')
leg=legend('Entry Barrier','Long-Run Average','location','northeast')
leg.FontSize = 11;

subplot(2,2,2)
plot(alpha_vec,Qlow_alpha,'Linewidth',2)
hold on
plot(alpha_vec,Average_Q_alpha,'--','Linewidth',2)
axis tight
grid on
xlabel('$\alpha$','interpreter','latex','FontSize',14,'FontWeight','bold','FontName','Times')
ylabel('Q','interpreter','latex','FontSize',12,'FontWeight','bold','FontName','Times')

subplot(2,2,3)
plot(sigma2_vec,Qlow_sigma,'Linewidth',2)
hold on
plot(sigma2_vec,Average_Q_sigma,'--','Linewidth',2)
axis tight
grid on
xlabel('$\sigma$','interpreter','latex','FontSize',14,'FontWeight','bold','FontName','Times')
ylabel('Q','interpreter','latex','FontSize',12,'FontWeight','bold','FontName','Times')

subplot(2,2,4)
plot(cost_vec*100,Qlow_cost,'Linewidth',2)
hold on
plot(cost_vec*100,Average_Q_cost,'--','Linewidth',2)
axis tight
grid on
xlabel('$I ~ in ~ \%$','interpreter','latex','FontSize',14,'FontWeight','bold','FontName','Times')
ylabel('Q','interpreter','latex','FontSize',12,'FontWeight','bold','FontName','Times')

savefig('Fig_Q_comp_stats.fig')
print -depsc2 Fig_Q_comp_stats.eps