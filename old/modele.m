%t=1 mois
B=1000; %cours du bitcoin
R=0; %récompense en bitcoins
F=1; %frais de transaction par bloc en bitcoin
pool=0.02; %part que prend le pool

Ht0=14; % TH/s
G=B*(R+F)*(1-pool)*4392; %4392*10 min en 1 mois recompense totale des mineurs par mois.
C=1.375; %consommation de l'ASIC en kW
E=0.05*24*30.5; %0.15 euros/kWh prix d'un kWmois. 
P=2000; % prix de l'ASIC
a=1.07; %1.0293^24=2$. Loi de Moore %1.123: x4 par an 
St0=1; %Th/s 2763318.772

profit_mineur2(St0,Ht0,G,C,E,P,a)
profit_mineur(St0,Ht0,G,C,E,P,a)

Newton_Raphson(St0,Ht0,G,C,E,P,a) % donne St0 pour que le profit soit nul.
Newton_Raphson(St0,Ht0,G,C,E,P,a)/Ht0 %nombre de mineurs
P*Newton_Raphson(St0,Ht0,G,C,E,P,a)/(2*Ht0) %investissement pour falsifier des blocs


P0=143;
C0=0.00134;
a=0.0000066;
R=1;

Profit=H0*(R/H_0-(C_0/a)*log(1+a*r/(C0*H0))-P0)
S0=H0*R/(a*R+H0*C0)
(1/a)*log(R/(C0*S0))
