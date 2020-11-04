% Main code for oligopolistic model

clear all 
close all


%% LOAD DATA

donnees=xlsread('database');
R=donnees(:,1);
Q=donnees(:,3);

% commented: values for parameters and dates used in the paper (in case you want to change them to make tests).

d=2091; 
f=3003;  

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
a           = 0.00247530085492*365;

% Brownian Parameters; Annual Values

alpha       = 0.458482838838;

sigma2      = 0.544398207762;

mu          = alpha+a;

r           = 0.1;

% Time-to-build
delta       = 46.5;
% Step 1: Evaluate R (reservation productivity at the final date t=T in the last iteration period)

%Evaluate the caracteristic equation of the Cauchy-Euler equation
coef            = [sigma2/2 (mu-sigma2/2) -r-a];
beta            = roots(coef);
beta            = max(beta);                                               % Positive root

P_bar           = (beta/(beta-1))*(r-alpha);

barrier         = 5.09958217873;

Cost            = barrier/((beta/(beta-1))*(r-alpha))*365*exp((r-alpha)*delta/365);


% Oligopolistic costs

for i = 2 :20
Cost_olig(i-1)            = barrier/((beta/(beta-1))*(r-alpha)*(i/(i-1)))*365;
competitors(i-1)          = i;
OPremium(i-1)             = 1/(i-1)*100;
end

% Comparison with price data

Price_Data = Price_ASICS(1);
Electicity = 16.8*0.03*365*(1-exp(-r*2.65))/r; 
figure 
hold on
area(competitors, Cost*ones(size(competitors)),'Linewidth',2,'FaceColor',[0    0.7490    0.7490])
area(competitors,Cost_olig,'Linewidth',2,'FaceColor',[0    0.4471    0.7412])
area(competitors,Price_Data.*ones(size(competitors)),'Linewidth',2,'FaceColor',[0.8510    0.3255    0.0980
])
xlabel('Number of Mining Firms')
ylabel('Revenues in $ per Th/S')
grid on
legend({'Seigniorage','Operating Costs', 'Hardware Costs'},'Fontsize',14, 'Location', 'southeast')


set(gcf,'position',[0,0,650,400])
savefig('Seignorage.fig')
print -depsc2 Seignorage.eps
