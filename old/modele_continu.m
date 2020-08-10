
P0=143;
C0=0.00134;
a=0.00002; %0.000007
%exp(105192*a)
R=15000;

H0=newton_raphson_continu(C0,P0,a,R)

S0=H0*R/(a*R+H0*C0)
N=(1/a)*log(R/(C0*S0))
%N/(6*24*365.25)

S0*P0/2
s=-(1/a)*log(0.5*(1+exp(-a*N)))
H0*(R*(s+(exp(-a*s)-1)/a)/(a*S0)-C0*s^2/2-s*P0)

epsilon=-R/2
eas=(S0*(1+epsilon/R)+exp(-a*N)*H0/a)/(S0+exp(-a*N)*H0/a)
log(eas)/a


plage_temps=1:N;
duree=length(plage_temps);
resultat=zeros(1,duree);
for t=1:duree
    resultat(t)=profit_temps(t,C0,P0,a,R,S0);
end
plot(plage_temps,resultat)
    


    
    