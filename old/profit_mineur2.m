function profit=profit_mineur2(St0,Ht0,G,C,E,P,a)
    % forme explicite
    N=max(0,floor(log(G*Ht0/(C*E*St0))/log(a)));
    profit=max(-P,G*Ht0/(St0)*((a-(1/a)^N)/(a-1))-(N+1)*C*E-P);
end