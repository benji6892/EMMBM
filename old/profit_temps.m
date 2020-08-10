function y=profit_temps(t,C0,P0,a,R,S0)
    y=R*(1-exp(-a*t))/(a*S0)-t*C0-P0*(t>0);
end