function profit=profit_continu(x,C0,P0,a,R)
    profit=x*(R/x-(C0/a)*log(1+a*R/(C0*x))-P0);
end